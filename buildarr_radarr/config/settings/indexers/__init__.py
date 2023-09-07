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
Indexer settings configuration.
"""


from __future__ import annotations

from logging import getLogger
from typing import Dict, List, Union

import radarr

from buildarr.config import RemoteMapEntry
from pydantic import Field
from typing_extensions import Annotated, Self

from ....api import radarr_api_client
from ....secrets import RadarrSecrets
from ...types import RadarrConfigBase
from .torrent.filelist import FilelistIndexer
from .torrent.hdbits import HdbitsIndexer
from .torrent.iptorrents import IptorrentsIndexer
from .torrent.nyaa import NyaaIndexer
from .torrent.passthepopcorn import PassthepopcornIndexer
from .torrent.rss import TorrentRssIndexer
from .torrent.torrentpotato import TorrentpotatoIndexer
from .torrent.torznab import TorznabIndexer
from .usenet.newznab import NewznabIndexer

logger = getLogger(__name__)

INDEXER_TYPE_MAP = {
    indexer_type._implementation: indexer_type  # type: ignore[attr-defined]
    for indexer_type in (
        FilelistIndexer,
        HdbitsIndexer,
        IptorrentsIndexer,
        NewznabIndexer,
        NyaaIndexer,
        PassthepopcornIndexer,
        TorrentRssIndexer,
        TorrentpotatoIndexer,
        TorznabIndexer,
    )
}

IndexerType = Union[
    FilelistIndexer,
    HdbitsIndexer,
    IptorrentsIndexer,
    NewznabIndexer,
    NyaaIndexer,
    PassthepopcornIndexer,
    TorrentRssIndexer,
    TorrentpotatoIndexer,
    TorznabIndexer,
]


class RadarrIndexersSettings(RadarrConfigBase):
    """

    !!! note

        Instead of manually configuring indexers for each of your Radarr instances,
        it is highly recommended to setup a [Prowlarr](https://prowlarr.com)
        indexer manager, and manage it using the
        [Prowlarr plugin for Buildarr](https://buildarr.github.io/plugins/prowlarr).

        This is particularly convenient when managing more than one Radarr instance.

        When managing indexers using Prowlarr, do not add any indexer definitions
        to this Radarr instance in Buildarr, and ensure `delete_unmanaged` is set to `false`.

    Indexers are used to monitor for new releases of media on external trackers.
    When a suitable release has been found, Radarr registers it for download
    on one of the configured download clients.

    ```yaml
    radarr:
      settings:
        indexers:
          minimum_age: 0  # minutes
          retention: 0  # days
          maximum_size: 0  # MB
          rss_sync_interval: 15  # minutes
          delete_unmanaged: false  # Better to leave off for the most part.
          definitions:
            Nyaa:  # Indexer name
              type: nyaa  # Type of indexer
              enable_rss: true
              enable_automatic_search: true
              enable_interactive_search: true
              indexer_priority: 25
              download_client: null
              website_url: https://example.com
              tags:
                - anime-movies
    ```

    The following parameters are available for configuring indexers and
    how they are handled by Radarr.

    For more information on how Radarr finds movies, refer to the FAQ on
    [WikiArr](https://wiki.servarr.com/radarr/faq#how-does-radarr-work).
    """

    minimum_age: int = Field(0, ge=0)  # minutes
    """
    Minimum age (in minutes) of NZBs before they are grabbed. Applies to Usenet only.

    Use this to give new releases time to propagate to your Usenet provider.
    """

    retention: int = Field(0, ge=0)  # days
    """
    Retention of releases (in days). Applies to Usenet only.

    Set to `0` for unlimited retention.
    """

    # Set to 0 for unlimited
    maximum_size: int = Field(0, ge=0)  # MB
    """
    Maximum size for a release to be grabbed, in megabytes (MB).

    Set to `0` to set for unlimited size.
    """

    rss_sync_interval: int = Field(15, ge=0)  # minutes
    """
    Interval (in minutes) to sync RSS feeds with indexers.

    Set to `0` to disable syncing. **WARNING: This also disables automatic release grabbing.**
    """

    delete_unmanaged: bool = False
    """
    Automatically delete indexers not configured by Buildarr.

    Take care when enabling this option, as it will also delete indexers
    created by external applications such as Prowlarr.

    If unsure, leave set at the default of `false`.
    """

    definitions: Dict[str, Annotated[IndexerType, Field(discriminator="type")]] = {}
    """
    Indexers to manage via Buildarr are defined here.
    """

    _remote_map: List[RemoteMapEntry] = [
        ("minimum_age", "minimumAge", {}),
        ("retention", "retention", {}),
        ("maximum_size", "maximumSize", {}),
        ("rss_sync_interval", "rssSyncInterval", {}),
    ]

    @classmethod
    def from_remote(cls, secrets: RadarrSecrets) -> Self:
        with radarr_api_client(secrets=secrets) as api_client:
            api_indexer_config = radarr.IndexerConfigApi(api_client).get_indexer_config()
            indexer_api = radarr.IndexerApi(api_client)
            api_indexer_schemas: Dict[str, radarr.IndexerResource] = {
                api_schema.implementation: api_schema
                for api_schema in indexer_api.list_indexer_schema()
            }
            api_indexers: Dict[str, radarr.IndexerResource] = {
                api_indexer.name: api_indexer for api_indexer in indexer_api.list_indexer()
            }
            downloadclient_ids: Dict[str, int] = (
                {dc.name: dc.id for dc in radarr.DownloadClientApi().list_download_client()}
                if any(api_indexer.download_client_id for api_indexer in api_indexers.values())
                else {}
            )
            tag_ids: Dict[str, int] = (
                {tag.label: tag.id for tag in radarr.TagApi(api_client).list_tag()}
                if any(api_indexer.tags for api_indexer in api_indexers.values())
                else {}
            )
        return cls(
            **cls.get_local_attrs(cls._remote_map, api_indexer_config.to_dict()),
            definitions={
                indexer_name: INDEXER_TYPE_MAP[  # type: ignore[attr-defined]
                    api_indexer.implementation
                ]._from_remote(
                    api_schema=api_indexer_schemas[api_indexer.implementation],
                    downloadclient_ids=downloadclient_ids,
                    tag_ids=tag_ids,
                    api_indexer=api_indexer,
                )
                for indexer_name, api_indexer in api_indexers.items()
            },
        )

    def update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        updated = False
        with radarr_api_client(secrets=secrets) as api_client:
            api_indexer_config = radarr.IndexerConfigApi(api_client).get_indexer_config()
            indexer_api = radarr.IndexerApi(api_client)
            api_indexer_schemas: Dict[str, radarr.IndexerResource] = {
                api_schema.implementation: api_schema
                for api_schema in indexer_api.list_indexer_schema()
            }
            api_indexers: Dict[str, radarr.IndexerResource] = {
                api_indexer.name: api_indexer for api_indexer in indexer_api.list_indexer()
            }
            downloadclient_ids: Dict[str, int] = (
                {dc.name: dc.id for dc in radarr.DownloadClientApi().list_download_client()}
                if any(indexer.download_client for indexer in self.definitions.values())
                or any(indexer.download_client for indexer in remote.definitions.values())
                else {}
            )
            tag_ids: Dict[str, int] = (
                {tag.label: tag.id for tag in radarr.TagApi(api_client).list_tag()}
                if any(indexer.tags for indexer in self.definitions.values())
                or any(indexer.tags for indexer in remote.definitions.values())
                else {}
            )
        config_updated, config_updated_attrs = self.get_update_remote_attrs(
            tree,
            remote,
            self._remote_map,
            check_unmanaged=check_unmanaged,
            set_unchanged=True,
        )
        if config_updated:
            with radarr_api_client(secrets=secrets) as api_client:
                radarr.IndexerConfigApi(api_client).update_indexer_config(
                    str(api_indexer_config.id),
                    {**api_indexer_config.to_dict(), **config_updated_attrs},
                )
            updated = True
        for indexer_name, indexer in self.definitions.items():
            indexer_tree = f"{tree}.definitions[{indexer_name!r}]"
            api_schema = api_indexer_schemas[indexer._implementation]
            if indexer_name not in remote.definitions:
                indexer._create_remote(
                    tree=indexer_tree,
                    secrets=secrets,
                    api_schema=api_schema,
                    downloadclient_ids=downloadclient_ids,
                    tag_ids=tag_ids,
                    indexer_name=indexer_name,
                )
                updated = True
            elif indexer._update_remote(
                tree=indexer_tree,
                secrets=secrets,
                api_schema=api_schema,
                remote=remote.definitions[indexer_name],  # type: ignore[arg-type]
                downloadclient_ids=downloadclient_ids,
                tag_ids=tag_ids,
                api_indexer=api_indexers[indexer_name],
            ):
                updated = True
        return updated

    def delete_remote(self, tree: str, secrets: RadarrSecrets, remote: Self) -> bool:
        updated = False
        with radarr_api_client(secrets=secrets) as api_client:
            indexer_ids: Dict[str, int] = {
                api_indexer.name: api_indexer.id
                for api_indexer in radarr.IndexerApi(api_client).list_indexer()
            }
        for indexer_name, indexer in remote.definitions.items():
            if indexer_name not in self.definitions:
                indexer_tree = f"{tree}.definitions[{indexer_name!r}]"
                if self.delete_unmanaged:
                    logger.info("%s: (...) -> (deleted)", indexer_tree)
                    indexer._delete_remote(
                        secrets=secrets,
                        indexer_id=indexer_ids[indexer_name],
                    )
                    updated = True
                else:
                    logger.debug("%s: (...) (unmanaged)", indexer_tree)
        return updated
