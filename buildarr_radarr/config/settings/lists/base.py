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
Import list settings configuration.
"""


from __future__ import annotations

from logging import getLogger
from typing import Any, Dict, Iterable, List, Mapping, Set

import radarr

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr
from typing_extensions import Self

from ....api import radarr_api_client
from ....secrets import RadarrSecrets
from ...types import RadarrConfigBase

logger = getLogger(__name__)


class Monitor(BaseEnum):
    movie_only = "movieOnly"
    movie_and_collection = "movieAndCollection"
    none = "none"


class MinimumAvailability(BaseEnum):
    announced = "announced"
    in_cinemas = "inCinemas"
    released = "released"


class ImportList(RadarrConfigBase):
    """
    For more information on how an import list should be setup,
    refer to this guide on [WikiArr](https://wiki.servarr.com/radarr/settings#import-lists).

    All import list types can have the following attributes configured.
    """

    enable: bool = False
    """ """

    enable_automatic_add: bool = True
    """
    Automatically add series to Radarr upon syncing.
    """

    monitor: Monitor = Monitor.movie_only
    """
    Define how Radarr should monitor existing and new movies.

    Values:

    * `movie-only`
    * `movie-and-collection`
    * `none`
    """

    search_on_add: bool = False
    """
    Search for movies on this list when added to the library.
    """

    minimum_availability: MinimumAvailability = MinimumAvailability.announced
    """ """

    quality_profile: NonEmptyStr
    """
    The name of the quality profile list items will be added with.

    This attribute is required.
    """

    root_folder: NonEmptyStr
    """
    The root folder to add list items to.

    This attribute is required.
    """

    # tags
    tags: Set[NonEmptyStr] = set()
    """
    Tags to assign to items imported from this import list.
    """

    _implementation: str
    _remote_map: List[RemoteMapEntry]

    @classmethod
    def _get_base_remote_map(
        cls,
        quality_profile_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
    ) -> List[RemoteMapEntry]:
        return [
            ("enable", "enable", {}),
            ("enable_automatic_add", "enableAuto", {}),
            ("monitor", "monitor", {}),
            ("search_on_add", "searchOnAdd", {}),
            ("mininum_availability", "minimumAvailability", {}),
            (
                "quality_profile",
                "qualityProfileId",
                {
                    "decoder": lambda v: next(
                        (ind for ind, ind_id in quality_profile_ids.items() if ind_id == v),
                    ),
                    "encoder": lambda v: quality_profile_ids[v],
                },
            ),
            (
                "root_folder",
                "rootFolderPath",
                {"decoder": lambda v: v or None, "encoder": lambda v: v or ""},
            ),
            (
                "tags",
                "tags",
                {
                    "decoder": lambda v: set(
                        (tag for tag, tag_id in tag_ids.items() if tag_id in v),
                    ),
                    "encoder": lambda v: sorted(tag_ids[tag] for tag in v),
                },
            ),
        ]

    @classmethod
    def _from_remote(
        cls,
        quality_profile_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
        remote_attrs: Mapping[str, Any],
    ) -> Self:
        return cls(
            **cls.get_local_attrs(
                (cls._get_base_remote_map(quality_profile_ids, tag_ids) + cls._remote_map),
                remote_attrs,
            ),
        )

    def _get_api_schema(self, schemas: Iterable[radarr.ImportListResource]) -> Dict[str, Any]:
        return {
            k: v
            for k, v in next(
                s for s in schemas if s.implementation.lower() == self._implementation.lower()
            )
            .to_dict()
            .items()
            if k not in ["id", "name"]
        }

    def _create_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        api_importlist_schemas: Iterable[radarr.ImportListResource],
        quality_profile_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
        importlist_name: str,
    ) -> None:
        api_schema = self._get_api_schema(api_importlist_schemas)
        set_attrs = self.get_create_remote_attrs(
            tree=tree,
            remote_map=self._get_base_remote_map(quality_profile_ids, tag_ids) + self._remote_map,
        )
        field_values: Dict[str, Any] = {
            field["name"]: field["value"] for field in set_attrs["fields"]
        }
        set_attrs["fields"] = [
            ({**f, "value": field_values[f["name"]]} if f["name"] in field_values else f)
            for f in api_schema["fields"]
        ]
        remote_attrs = {"name": importlist_name, **api_schema, **set_attrs}
        with radarr_api_client(secrets=secrets) as api_client:
            radarr.ImportListApi(api_client).create_import_list(
                import_list_resource=radarr.ImportListResource.from_dict(remote_attrs),
            )

    def _update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        quality_profile_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
        api_importlist: radarr.ImportListResource,
    ) -> bool:
        updated, updated_attrs = self.get_update_remote_attrs(
            tree,
            remote,
            self._get_base_remote_map(quality_profile_ids, tag_ids) + self._remote_map,
            check_unmanaged=True,
            set_unchanged=True,
        )
        if updated:
            if "fields" in updated_attrs:
                updated_fields: Dict[str, Any] = {
                    field["name"]: field["value"] for field in updated_attrs["fields"]
                }
                updated_attrs["fields"] = [
                    (
                        {**f, "value": updated_fields[f["name"]]}
                        if f["name"] in updated_fields
                        else f
                    )
                    for f in api_importlist.to_dict()["fields"]
                ]
            remote_attrs = {**api_importlist.to_dict(), **updated_attrs}
            with radarr_api_client(secrets=secrets) as api_client:
                radarr.ImportListApi(api_client).update_import_list(
                    id=str(api_importlist.id),
                    import_list_resource=radarr.ImportListResource.from_dict(remote_attrs),
                )
            return True
        return False

    def _delete_remote(self, secrets: RadarrSecrets, importlist_id: int) -> None:
        with radarr_api_client(secrets=secrets) as api_client:
            radarr.ImportListApi(api_client).delete_import_list(id=importlist_id)
