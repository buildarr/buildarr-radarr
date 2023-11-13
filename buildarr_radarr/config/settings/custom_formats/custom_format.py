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


"""
Custom format definition configuration.
"""


from __future__ import annotations

import json

from logging import getLogger
from typing import Any, Dict, List, Optional, Union, cast

import radarr

from buildarr.config import ConfigTrashIDNotFoundError, RemoteMapEntry
from buildarr.state import state
from buildarr.types import TrashID
from pydantic import Field
from typing_extensions import Annotated, Self

from ....api import radarr_api_client
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
    # Custom format definition configuration.

    trash_id: Optional[TrashID] = None
    """
    Trash ID of the TRaSH-Guides custom format profile to load default values from.

    If there is an update in the profile, the custom format conditions will be updated accordingly.

    If a condition that is explicitly defined on this custom format in Buildarr has the same name
    as a condition in the TRaSH-Guides profile, the explicitly defined condition takes precedence.
    """

    default_score: Optional[int] = None
    """
    The default score assigned to this custom format when it is assigned to a quality profile.

    If this attribute is explicitly defined on the custom format, the defined value will always
    be used as the default score.

    If `default_score` is not defined, the default value used by Buildarr depends on the
    type of custom format:

    * If this is a custom format imported from a Trash ID, this will default to the default
      score TRaSH-Guides has assigned this custom format (`trash_scores.default` in the metadata).
      If the custom format does not have a default score defined, the default score will be 0.
    * If this is a manually defined custom format, the default score will be 0.
    """

    include_when_renaming: bool = False
    """
    Make the custom format available in the `{Custom Formats}` template when renaming media titles.
    """

    delete_unmanaged_conditions: bool = True
    """
    Delete conditions defined on this custom format on the remote instance
    not managed by Buildarr.

    It is recommended to keep this option enabled, particularly for
    custom formats imported from TRaSH-Guides.
    """

    conditions: Dict[str, Annotated[ConditionType, Field(discriminator="type")]] = {}
    """
    A list of conditions that will cause the custom format to be applied to a release
    if matches are found.

    By default, only one of the defined conditions need to match for the custom format
    to be applied. If one or more conditions have `required` set to `true`, those conditions
    must **all** match in order for the custom format to be applied.
    """

    # Radarr/Sonarr Custom Format JSON specification:
    # https://github.com/TRaSH-Guides/Guides/blob/master/CONTRIBUTING.md#radarrsonarr-custom-format-json

    # TODO: Validate conditions not empty if `trash_id` is not defined.

    _remote_map: List[RemoteMapEntry] = [
        ("include_when_renaming", "includeCustomFormatWhenRenaming", {}),
    ]

    def uses_trash_metadata(self) -> bool:
        return bool(self.trash_id)

    def _post_init_render(self, api_condition_schema_dicts: Dict[str, Dict[str, Any]]) -> None:
        if not self.trash_id:
            return
        for customformat_file in (
            state.trash_metadata_dir / "docs" / "json" / "radarr" / "cf"
        ).iterdir():
            with customformat_file.open() as f:
                trash_customformat = json.load(f)
                if cast(str, trash_customformat["trash_id"]).lower() == self.trash_id:
                    if "default_score" not in self.__fields_set__:
                        try:
                            self.default_score = trash_customformat.get("trash_scores", {})[
                                "default"
                            ]
                        except KeyError:
                            pass
                    for trash_condition in trash_customformat["specifications"]:
                        condition_name = trash_condition["name"]
                        if condition_name not in self.conditions:
                            api_condition_dict: Dict[str, Any] = {
                                **trash_condition,
                                "fields": [
                                    {"name": name, "value": value}
                                    for name, value in trash_condition["fields"].items()
                                ],
                            }
                            self.conditions[
                                condition_name
                            ] = CONDITION_TYPE_MAP[  # type: ignore[attr-defined]
                                api_condition_dict["implementation"]
                            ]._from_remote(
                                api_schema_dict=api_condition_schema_dicts[
                                    api_condition_dict["implementation"]
                                ],
                                api_condition=radarr.CustomFormatSpecificationSchema.from_dict(
                                    api_condition_dict,
                                ),
                            )
                    self.delete_unmanaged_conditions = True
                    return
        raise ConfigTrashIDNotFoundError(
            f"Unable to find Radarr custom format profile with trash ID '{self.trash_id}'",
        )

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
                                tree=f"{tree}.conditions[{condition_name!r}]",
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
            condition_tree = f"{tree}.conditions[{condition_name!r}]"
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
                condition_tree = f"{tree}.conditions[{condition_name!r}]"
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
