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
Custom format settings configuration.
"""


from __future__ import annotations

from logging import getLogger
from typing import Any, Dict

import radarr

from typing_extensions import Self

from ....api import api_get, radarr_api_client
from ....secrets import RadarrSecrets
from ...types import RadarrConfigBase
from .custom_format import CustomFormat

logger = getLogger(__name__)


class RadarrCustomFormatsSettings(RadarrConfigBase):
    # Custom format settings configuration.

    delete_unmanaged: bool = False
    """
    Automatically delete custom formats not defined in Buildarr.
    """

    definitions: Dict[str, CustomFormat] = {}
    """
    Define download clients under this attribute.
    """

    def uses_trash_metadata(self) -> bool:
        for customformat in self.definitions.values():
            if customformat.uses_trash_metadata():
                return True
        return False

    def _post_init_render(self, secrets: RadarrSecrets) -> None:
        with radarr_api_client(secrets=secrets) as api_client:
            radarr.CustomFormatApi(api_client)
            # TODO: Replace with CustomFormatApi.get_custom_format_schama when fixed.
            # https://github.com/devopsarr/radarr-py/issues/36
            api_condition_schema_dicts: Dict[str, Dict[str, Any]] = {
                api_schema_dict["implementation"]: api_schema_dict
                for api_schema_dict in api_get(secrets, "/api/v3/customformat/schema")
            }
        for customformat in self.definitions.values():
            if customformat.uses_trash_metadata():
                customformat._post_init_render(api_condition_schema_dicts)

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
            customformat_tree = f"{tree}.definitions[{customformat_name!r}]"
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
                customformat_tree = f"{tree}.definitions[{customformat_name!r}]"
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
