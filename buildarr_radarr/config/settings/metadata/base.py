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
Metadata configuration base class.
"""


from __future__ import annotations

from typing import Any, Dict, List

import radarr

from buildarr.config import RemoteMapEntry
from typing_extensions import Self

from ....api import radarr_api_client
from ....secrets import RadarrSecrets
from ...types import RadarrConfigBase


class Metadata(RadarrConfigBase):
    # Metadata definition base class.

    enable: bool = False
    """
    When set to `true`, enables creating metadata files in this format.
    """

    _implementation: str
    _base_remote_map: List[RemoteMapEntry] = [("enable", "enable", {})]
    _remote_map: List[RemoteMapEntry] = []

    @classmethod
    def _get_remote_map(cls, api_schema: radarr.MetadataResource) -> List[RemoteMapEntry]:
        return []

    @classmethod
    def _from_remote(
        cls,
        api_schema: radarr.MetadataResource,
        api_metadata: radarr.MetadataResource,
    ) -> Self:
        return cls(
            **cls.get_local_attrs(
                remote_map=(
                    cls._base_remote_map
                    + cls._remote_map
                    + cls._get_remote_map(api_schema=api_schema)
                ),
                remote_attrs=api_metadata.to_dict(),
            ),
        )

    def _update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        api_schema: radarr.MetadataResource,
        api_metadata: radarr.MetadataResource,
        check_unmanaged: bool,
    ) -> bool:
        changed, changed_attrs = self.get_update_remote_attrs(
            tree=tree,
            remote=remote,
            remote_map=(
                self._base_remote_map
                + self._remote_map
                + self._get_remote_map(api_schema=api_schema)
            ),
            check_unmanaged=check_unmanaged,
        )
        if changed:
            remote_attrs = api_metadata.to_dict()
            if "fields" in changed_attrs:
                changed_fields: Dict[str, Any] = {
                    field["name"]: field["value"] for field in changed_attrs["fields"]
                }
                changed_attrs["fields"] = [
                    (
                        {**f, "value": changed_fields[f["name"]]}
                        if f["name"] in changed_fields
                        else f
                    )
                    for f in remote_attrs["fields"]
                ]
            with radarr_api_client(secrets=secrets) as api_client:
                radarr.MetadataApi(api_client).update_metadata(
                    id=api_metadata.id,
                    metadata_resource=radarr.MetadataResource.from_dict(
                        {**remote_attrs, **changed_attrs},
                    ),
                )
            return True
        return False
