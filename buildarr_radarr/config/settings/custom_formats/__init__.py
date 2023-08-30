# Copyright (C) 2023 Callum Dickinson
#
# Buildarr is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# Buildarr is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Buildarr.
# If not, see <https://www.gnu.org/licenses/>.


from __future__ import annotations

from logging import getLogger
from typing import Any, Dict, List, Union, cast

import radarr

from buildarr.config import RemoteMapEntry
from pydantic import Field
from typing_extensions import Annotated, Self

from ....api import api_get, radarr_api_client
from ....secrets import RadarrSecrets
from ...types import RadarrConfigBase
from .conditions.edition import EditionCondition
from .conditions.indexer_flag import IndexerFlagCondition
from .conditions.language import LanguageCondition
from .conditions.quality_modifier import QualityModifierCondition
from .conditions.release_group import ReleaseGroupCondition
from .conditions.release_title import ReleaseTitleCondition
from .conditions.resolution import ResolutionCondition
from .conditions.size import SizeCondition
from .conditions.source import SourceCondition

logger = getLogger(__name__)

ConditionType = Union[
    EditionCondition,
    IndexerFlagCondition,
    LanguageCondition,
    QualityModifierCondition,
    ReleaseGroupCondition,
    ReleaseTitleCondition,
    ResolutionCondition,
    SizeCondition,
    SourceCondition,
]

CONDITION_TYPE_MAP = {
    condition_type._implementation: condition_type  # type: ignore[attr-defined]
    for condition_type in (
        EditionCondition,
        IndexerFlagCondition,
        LanguageCondition,
        QualityModifierCondition,
        ReleaseGroupCondition,
        ReleaseTitleCondition,
        ResolutionCondition,
        SizeCondition,
        SourceCondition,
    )
}


class CustomFormat(RadarrConfigBase):
    """ """

    include_when_renaming: bool = False
    """
    Make available in the `{Custom Formats}` template when renaming media titles.
    """

    delete_unmanaged_conditions: bool = False
    """ """

    conditions: Dict[str, Annotated[ConditionType, Field(discriminator="type")]] = {}
    """ """

    _remote_map: List[RemoteMapEntry] = [
        ("include_when_renaming", "includeCustomFormatWhenRenaming", {}),
    ]

    @classmethod
    def _from_remote(
        cls,
        secrets: RadarrSecrets,
        api_condition_schema_dicts: Dict[str, Dict[str, Any]],
        api_customformat: radarr.CustomFormatResource,
    ) -> CustomFormat:
        return cls(
            **cls.get_local_attrs(
                remote_map=cls._remote_map,
                remote_attrs=api_customformat.to_dict(),
            ),
            conditions={
                api_condition.name: CONDITION_TYPE_MAP[  # type: ignore[attr-defined]
                    api_condition.implementation
                ]._from_remote(
                    api_schema_dict=api_condition_schema_dicts[api_condition.implementation],
                    api_condition=api_condition,
                )
                for api_condition in cast(
                    List[radarr.CustomFormatSpecificationSchema],
                    api_customformat.specifications,
                )
            },
        )

    def _create_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        api_condition_schema_dicts: Dict[str, Dict[str, Any]],
        customformat_name: str,
    ) -> None:
        with radarr_api_client(secrets=secrets) as api_client:
            radarr.CustomFormatApi(api_client).create_custom_format(
                custom_format_resource=radarr.CustomFormatResource.from_dict(
                    {
                        "name": customformat_name,
                        **self.get_create_remote_attrs(tree=tree, remote_map=self._remote_map),
                        "specifications": [
                            condition._create_remote(
                                tree=f"{tree}.conditions[{repr(condition_name)}]",
                                api_schema_dict=api_condition_schema_dicts[
                                    condition._implementation
                                ],
                                condition_name=condition_name,
                            )
                            for condition_name, condition in sorted(
                                self.conditions.items(),
                                key=lambda k: k[0],
                            )
                        ],
                    },
                ),
            )

    def _update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        api_condition_schema_dicts: Dict[str, Dict[str, Any]],
        api_customformat: radarr.CustomFormatResource,
    ) -> bool:
        api_conditions: Dict[str, radarr.CustomFormatSpecificationSchema] = {
            api_condition.name: api_condition for api_condition in api_customformat.specifications
        }
        changed, config_attrs = self.get_update_remote_attrs(
            tree=tree,
            remote=remote,
            remote_map=self._remote_map,
            set_unchanged=True,
        )
        api_condition_dicts: List[Dict[str, Any]] = []
        for condition_name, condition in self.conditions.items():
            condition_tree = f"{tree}.conditions[{repr(condition_name)}]"
            if condition_name not in remote.conditions:
                api_condition_dicts.append(
                    condition._create_remote(
                        tree=condition_tree,
                        api_schema_dict=api_condition_schema_dicts[condition._implementation],
                        condition_name=condition_name,
                    ),
                )
                changed = True
            else:
                condition_changed, api_condition_dict = condition._update_remote(
                    tree=condition_tree,
                    api_schema_dict=api_condition_schema_dicts[condition._implementation],
                    remote=remote.conditions[condition_name],  # type: ignore[arg-type]
                    api_condition=api_conditions[condition_name],
                )
                api_condition_dicts.append(api_condition_dict)
                if condition_changed:
                    changed = True
        for condition_name in remote.conditions.keys():
            if condition_name not in self.conditions:
                condition_tree = f"{tree}.conditions[{repr(condition_name)}]"
                if self.delete_unmanaged_conditions:
                    logger.info("%s: (...) -> (deleted)", condition_tree)
                    changed = True
                else:
                    logger.debug("%s: (...) (unmanaged)", condition_tree)
                    api_condition_dicts.append(api_conditions[condition_name].to_dict())
        if changed:
            with radarr_api_client(secrets=secrets) as api_client:
                radarr.CustomFormatApi(api_client).update_custom_format(
                    id=str(api_customformat.id),
                    custom_format_resource=radarr.CustomFormatResource.from_dict(
                        {
                            **api_customformat.to_dict(),
                            **config_attrs,
                            "specifications": [
                                api_condition_dict
                                for api_condition_dict in sorted(
                                    api_condition_dicts,
                                    key=lambda k: k["name"],
                                )
                            ],
                        },
                    ),
                )
            return True
        return False

    def _delete_remote(self, secrets: RadarrSecrets, customformat_id: int) -> None:
        with radarr_api_client(secrets=secrets) as api_client:
            radarr.CustomFormatApi(api_client).delete_custom_format(id=customformat_id)


class RadarrCustomFormatsSettings(RadarrConfigBase):
    """ """

    delete_unmanaged: bool = False
    """
    Automatically delete custom formats not defined in Buildarr.
    """

    definitions: Dict[str, CustomFormat] = {}
    """
    Define download clients under this attribute.
    """

    @classmethod
    def from_remote(cls, secrets: RadarrSecrets) -> Self:
        with radarr_api_client(secrets=secrets) as api_client:
            customformat_api = radarr.CustomFormatApi(api_client)
            # TODO: Replace with CustomFormatApi.get_custom_format_schama when fixed.
            # https://github.com/devopsarr/radarr-py/issues/36
            api_condition_schema_dicts: Dict[str, Dict[str, Any]] = {
                api_schema_dict["implementation"]: api_schema_dict
                for api_schema_dict in api_get(secrets, "/api/v3/customformat/schema")
            }
            return cls(
                definitions={
                    api_customformat.name: CustomFormat._from_remote(
                        secrets=secrets,
                        api_condition_schema_dicts=api_condition_schema_dicts,
                        api_customformat=api_customformat,
                    )
                    for api_customformat in customformat_api.list_custom_format()
                },
            )

    def update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        # Track whether or not any changes have been made on the remote instance.
        changed = False
        # Pull API objects and metadata required during the update operation.
        with radarr_api_client(secrets=secrets) as api_client:
            customformat_api = radarr.CustomFormatApi(api_client)
            # TODO: Replace with CustomFormatApi.get_custom_format_schama when fixed.
            # https://github.com/devopsarr/radarr-py/issues/36
            api_condition_schema_dicts: Dict[str, Dict[str, Any]] = {
                api_schema_dict["implementation"]: api_schema_dict
                for api_schema_dict in api_get(secrets, "/api/v3/customformat/schema")
            }
            api_customformats: Dict[str, radarr.CustomFormatResource] = {
                api_customformat.name: api_customformat
                for api_customformat in customformat_api.list_custom_format()
            }
        # Compare local definitions to their remote equivalent.
        # If a local definition does not exist on the remote, create it.
        # If it does exist on the remote, attempt an an in-place modification,
        # and set the `changed` flag if modifications were made.
        for customformat_name, customformat in self.definitions.items():
            customformat_tree = f"{tree}.definitions[{repr(customformat_name)}]"
            if customformat_name not in remote.definitions:
                customformat._create_remote(
                    tree=customformat_tree,
                    secrets=secrets,
                    api_condition_schema_dicts=api_condition_schema_dicts,
                    customformat_name=customformat_name,
                )
                changed = True
            elif customformat._update_remote(
                tree=customformat_tree,
                secrets=secrets,
                remote=remote.definitions[customformat_name],  # type: ignore[arg-type]
                api_condition_schema_dicts=api_condition_schema_dicts,
                api_customformat=api_customformats[customformat_name],
            ):
                changed = True
        # Return whether or not the remote instance was changed.
        return changed

    def delete_remote(self, tree: str, secrets: RadarrSecrets, remote: Self) -> bool:
        # Track whether or not any changes have been made on the remote instance.
        changed = False
        # Pull API objects and metadata required during the update operation.
        with radarr_api_client(secrets=secrets) as api_client:
            customformat_ids: Dict[str, int] = {
                api_customformat.name: api_customformat.id
                for api_customformat in radarr.CustomFormatApi(api_client).list_custom_format()
            }
        # Traverse the remote definitions, and see if there are any remote definitions
        # that do not exist in the local configuration.
        # If `delete_unmanaged` is enabled, delete it from the remote.
        # If `delete_unmanaged` is disabled, just add a log entry acknowledging
        # the existence of the unmanaged definition.
        for customformat_name, customformat in remote.definitions.items():
            if customformat_name not in self.definitions:
                customformat_tree = f"{tree}.definitions[{repr(customformat_name)}]"
                if self.delete_unmanaged:
                    logger.info("%s: (...) -> (deleted)", customformat_tree)
                    customformat._delete_remote(
                        secrets=secrets,
                        customformat_id=customformat_ids[customformat_name],
                    )
                    changed = True
                else:
                    logger.debug("%s: (...) (unmanaged)", customformat_tree)
        # Return whether or not the remote instance was changed.
        return changed
