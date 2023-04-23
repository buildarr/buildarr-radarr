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
Radarr plugin indexers settings configuration.
"""


from __future__ import annotations

from logging import getLogger
from typing import Any, Dict, Iterable, List, Mapping, Optional

import radarr

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr
from pydantic import Field
from typing_extensions import Self

from ....api import radarr_api_client
from ....secrets import RadarrSecrets
from ...types import RadarrConfigBase

logger = getLogger(__name__)


class NabCategory(BaseEnum):
    """
    Newznab/Torznab category enumeration.
    """

    TV_WEBDL = 5010
    TV_FOREIGN = 5020
    TV_SD = 5030
    TV_HD = 5040
    TV_UHD = 5045
    TV_OTHER = 5050
    TV_SPORTS = 5060
    TV_ANIME = 5070
    TV_DOCUMENTARY = 5080

    # TODO: Make the enum also accept these values.
    # TV_WEBDL = "TV/WEB-DL"
    # TV_FOREIGN = "TV/Foreign"
    # TV_SD = "TV/SD"
    # TV_HD = "TV/HD"
    # TV_UHD = "TV/UHD"
    # TV_OTHER = "TV/Other"
    # TV_SPORTS = "TV/Sports"
    # TV_ANIME = "TV/Anime"
    # TV_DOCUMENTARY = "TV/Documentary"


class Indexer(RadarrConfigBase):
    """
    Here is an example of an indexer being configured in the `indexers` configuration
    block in Buildarr.

    ```yaml
    ...
      indexers:
        definitions:
          Nyaa: # Indexer name
            type: "nyaa" # Type of indexer
            # Configuration common to all indexers
            enable_rss: true
            enable_automatic_search: true
            enable_interactive_search: true
            anime_standard_format_search: true
            indexer_priority: 25
            download_client: null
            tags:
              - "example"
            # Nyaa-specific configuration
            website_url: "https://example.com"
          # Define more indexers here.
    ```

    There are configuration parameters common to all indexer types,
    and parameters common to only specific types of indexers.

    The following configuration attributes can be defined on all indexer types.
    """

    enable_rss: bool = True
    """
    If enabled, use this indexer to watch for files that are wanted and missing
    or have not yet reached their cutoff.
    """

    enable_automatic_search: bool = True
    """
    If enabled, use this indexer for automatic searches, including Search on Add.
    """

    enable_interactive_search: bool = True
    """
    If enabled, use this indexer for manual interactive searches.
    """

    priority: int = Field(25, ge=1, le=50, alias="indexer_priority")
    """
    Priority of this indexer to prefer one indexer over another in release tiebreaker scenarios.

    1 is highest priority and 50 is lowest priority.

    *Changed in version 0.4.1*: Renamed from `indexer_priority` to `priority`.
    The original name is still available as an alias.
    """

    download_client: Optional[NonEmptyStr] = None
    """
    The name of the download client to use for grabs from this indexer.
    """

    tags: List[NonEmptyStr] = []
    """
    Only use this indexer for series with at least one matching tag.
    Leave blank to use with all series.
    """

    _implementation: str
    _remote_map: List[RemoteMapEntry]

    @classmethod
    def _get_base_remote_map(
        cls,
        downloadclient_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
    ) -> List[RemoteMapEntry]:
        return [
            ("enable_rss", "enableRss", {}),
            ("enable_automatic_search", "enableAutomaticSearch", {}),
            ("enable_interactive_search", "enableInteractiveSearch", {}),
            ("priority", "priority", {}),
            (
                "download_client",
                "downloadClientId",
                {
                    "decoder": lambda v: (
                        [dc for dc, dc_id in downloadclient_ids.items() if dc_id == v][0]
                        if v
                        else None
                    ),
                    "encoder": lambda v: downloadclient_ids[v] if v else 0,
                },
            ),
            (
                "tags",
                "tags",
                {
                    "decoder": lambda v: [tag for tag, tag_id in tag_ids.items() if tag_id in v],
                    "encoder": lambda v: [tag_ids[tag] for tag in v],
                },
            ),
        ]

    @classmethod
    def _from_remote(
        cls,
        downloadclient_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
        remote_attrs: Mapping[str, Any],
    ) -> Self:
        return cls(
            **cls.get_local_attrs(
                cls._get_base_remote_map(downloadclient_ids, tag_ids) + cls._remote_map,
                remote_attrs,
            ),
        )

    def _get_api_schema(self, schemas: Iterable[radarr.IndexerResource]) -> Dict[str, Any]:
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
        api_indexer_schemas: Iterable[radarr.IndexerResource],
        downloadclient_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
        indexer_name: str,
    ) -> None:
        api_schema = self._get_api_schema(api_indexer_schemas)
        set_attrs = self.get_create_remote_attrs(
            tree=tree,
            remote_map=self._get_base_remote_map(downloadclient_ids, tag_ids) + self._remote_map,
        )
        field_values: Dict[str, Any] = {
            field["name"]: field["value"] for field in set_attrs["fields"]
        }
        set_attrs["fields"] = [
            ({**f, "value": field_values[f["name"]]} if f["name"] in field_values else f)
            for f in api_schema["fields"]
        ]
        remote_attrs = {"name": indexer_name, **api_schema, **set_attrs}
        with radarr_api_client(secrets=secrets) as api_client:
            radarr.IndexerApi(api_client).create_indexer(
                indexer_resource=radarr.IndexerResource.from_dict(remote_attrs),
            )

    def _update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        downloadclient_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
        api_indexer: radarr.IndexerResource,
    ) -> bool:
        updated, updated_attrs = self.get_update_remote_attrs(
            tree=tree,
            remote=remote,
            remote_map=self._get_base_remote_map(downloadclient_ids, tag_ids) + self._remote_map,
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
                    for f in api_indexer.to_dict()["fields"]
                ]
            remote_attrs = {**api_indexer.to_dict(), **updated_attrs}
            with radarr_api_client(secrets=secrets) as api_client:
                radarr.IndexerApi(api_client).update_indexer(
                    id=str(api_indexer.id),
                    indexer_resource=radarr.IndexerResource.from_dict(remote_attrs),
                )
            return True
        return False

    def _delete_remote(self, secrets: RadarrSecrets, indexer_id: int) -> None:
        with radarr_api_client(secrets=secrets) as api_client:
            radarr.IndexerApi(api_client).delete_indexer(id=indexer_id)
