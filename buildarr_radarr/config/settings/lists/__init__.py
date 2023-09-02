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
Radarr plugin import list settings configuration.
"""


from __future__ import annotations

from logging import getLogger
from typing import Dict, List, Union

import radarr

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum
from pydantic import Field
from typing_extensions import Annotated, Self

from ....api import radarr_api_client
from ....secrets import RadarrSecrets
from ...types import RadarrConfigBase
from .couchpotato import CouchpotatoImportList
from .exclusions import ListExclusionsSettings
from .plex.watchlist import PlexWatchlistImportList
from .radarr_import import RadarrImportList
from .trakt.list import TraktListImportList
from .trakt.popular_list import TraktPopularListImportList
from .trakt.user import TraktUserImportList

logger = getLogger(__name__)

IMPORTLIST_TYPE_MAP = {
    importlist_type._implementation: importlist_type  # type: ignore[attr-defined]
    for importlist_type in (
        CouchpotatoImportList,
        RadarrImportList,
        # TmdbCompanyImportList,
        # TmdbKeywordImportList,
        # TmdbListImportList,
        # TmdbPersonImportList,
        # TmdbPopularImportList,
        # TmdbUserImportList,
        TraktListImportList,
        TraktPopularListImportList,
        TraktUserImportList,
        PlexWatchlistImportList,
        # ImdbListImportList,
        # StevenluListImportList,
        # CustomlistImportist,
        # RssImportList,
        # StevenluCustomImportList,
    )
}

ImportListType = Union[
    CouchpotatoImportList,
    RadarrImportList,
    # TmdbCompanyImportList,
    # TmdbKeywordImportList,
    # TmdbListImportList,
    # TmdbPersonImportList,
    # TmdbPopularImportList,
    # TmdbUserImportList,
    TraktListImportList,
    TraktPopularListImportList,
    TraktUserImportList,
    PlexWatchlistImportList,
    # ImdbListImportList,
    # StevenluListImportList,
    # CustomlistImportist,
    # RssImportList,
    # StevenluCustomImportList,
]


class CleanLibraryLevel(BaseEnum):
    disabled = "disabled"
    log_only = "logOnly"
    keep_and_unmonitor = "keepAndUnmonitor"
    remove_and_keep = "removeAndKeep"
    remove_and_delete = "removeAndDelete"


class RadarrListsSettings(RadarrConfigBase):
    """
    Using import lists, Radarr can monitor and import episodes from external sources.

    ```yaml
    radarr:
      settings:
        import_lists:
          delete_unmanaged: False # Default is `false`
          delete_unmanaged_exclusions: true # Default is `false`
          definitions:
            Plex: # Name of import list definition
              type: "plex-watchlist" # Type of import list to use
              # Attributes common to all watch list types
              enable_automatic_add: true
              monitor: "all-episodes"
              series_type: "standard"
              season_folder: true
              tags:
                - "example"
              # Plex-specific attributes
              access_token: "..."
            # Add more import lists here.
          exclusions:
            72662: "Teletubbies" # TVDB ID is key, set an artibrary title as value
    ```

    Media can be queued on the source, and Radarr will automatically import them,
    look for suitable releases, and download them.

    Media that you don't want to import can be ignored using the `exclusions`
    attribute.
    """

    clean_library_level: CleanLibraryLevel = CleanLibraryLevel.disabled
    """ """

    exclusions: ListExclusionsSettings = ListExclusionsSettings()
    """ """

    delete_unmanaged: bool = False
    """
    Automatically delete import lists not defined in Buildarr.
    """

    definitions: Dict[str, Annotated[ImportListType, Field(discriminator="type")]] = {}
    """
    Import list definitions go here.
    """

    _remote_map: List[RemoteMapEntry] = [("clean_library_level", "listSyncLevel", {})]

    @classmethod
    def from_remote(cls, secrets: RadarrSecrets) -> Self:
        with radarr_api_client(secrets=secrets) as api_client:
            api_importlist_config = radarr.ImportListConfigApi(api_client).get_import_list_config()
            api_importlists = radarr.ImportListApi(api_client).list_import_list()
            quality_profile_ids: Dict[str, int] = (
                {
                    profile.name: profile.id
                    for profile in radarr.QualityProfileApi().list_quality_profile()
                }
                if any(api_importlist.quality_profile_id for api_importlist in api_importlists)
                else {}
            )
            tag_ids: Dict[str, int] = (
                {tag.label: tag.id for tag in radarr.TagApi(api_client).list_tag()}
                if any(api_importlist.tags for api_importlist in api_importlists)
                else {}
            )
        api_importlist_config_dict = api_importlist_config.to_dict()
        return cls(
            **cls.get_local_attrs(cls._remote_map, api_importlist_config_dict),
            exclusions=ListExclusionsSettings.from_remote(secrets),
            definitions={
                api_importlist.name: IMPORTLIST_TYPE_MAP[  # type: ignore[attr-defined]
                    api_importlist.implementation
                ]._from_remote(
                    quality_profile_ids=quality_profile_ids,
                    tag_ids=tag_ids,
                    remote_attrs=api_importlist.to_dict(),
                )
                for api_importlist in api_importlists
            },
        )

    def update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        return any(
            [
                self._update_remote_config(
                    tree=tree,
                    secrets=secrets,
                    remote=remote,
                    check_unmanaged=check_unmanaged,
                ),
                self.exclusions.update_remote(
                    tree=f"{tree}.exclusions",
                    secrets=secrets,
                    remote=remote.exclusions,
                    check_unmanaged=check_unmanaged,
                ),
                self._update_remote_definitions(
                    tree=tree,
                    secrets=secrets,
                    remote=remote,
                    check_unmanaged=check_unmanaged,
                ),
            ],
        )

    def _update_remote_config(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        updated, remote_attrs = self.get_update_remote_attrs(
            tree=tree,
            remote=remote,
            remote_map=self._remote_map,
            check_unmanaged=check_unmanaged,
            set_unchanged=True,
        )
        if updated:
            with radarr_api_client(secrets=secrets) as api_client:
                importlist_config_api = radarr.ImportListConfigApi(api_client)
                api_importlist_config = importlist_config_api.get_import_list_config()
                importlist_config_api.update_import_list_config(
                    id=str(api_importlist_config.id),
                    import_list_config_resource=radarr.ImportListConfigResource.from_dict(
                        {**api_importlist_config.to_dict(), **remote_attrs},
                    ),
                )
            return True
        return False

    def _update_remote_definitions(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        changed = False
        with radarr_api_client(secrets=secrets) as api_client:
            importlist_api = radarr.ImportListApi(api_client)
            api_importlist_schemas = importlist_api.list_import_list_schema()
            api_importlists: Dict[str, radarr.ImportListResource] = {
                api_importlist.name: api_importlist
                for api_importlist in importlist_api.list_import_list()
            }
            quality_profile_ids: Dict[str, int] = {
                profile.name: profile.id
                for profile in radarr.QualityProfileApi(api_client).list_quality_profile()
            }
            tag_ids: Dict[str, int] = (
                {tag.label: tag.id for tag in radarr.TagApi(api_client).list_tag()}
                if any(importlist.tags for importlist in self.definitions.values())
                or any(importlist.tags for importlist in remote.definitions.values())
                else {}
            )
        for importlist_name, importlist in self.definitions.items():
            importlist_tree = f"{tree}.definitions[{importlist_name!r}]"
            if importlist_name not in remote.definitions:
                importlist._create_remote(
                    tree=importlist_tree,
                    secrets=secrets,
                    api_importlist_schemas=api_importlist_schemas,
                    quality_profile_ids=quality_profile_ids,
                    tag_ids=tag_ids,
                    importlist_name=importlist_name,
                )
                changed = True
            elif importlist._update_remote(
                tree=importlist_tree,
                secrets=secrets,
                remote=remote.definitions[importlist_name],  # type: ignore[arg-type]
                # remote=remote.definitions[importlist_name]._resolve_from_local(
                #     name=importlist_name,
                #     local=importlist,  # type: ignore[arg-type]
                #     ignore_nonexistent_ids=True,
                # ),
                quality_profile_ids=quality_profile_ids,
                tag_ids=tag_ids,
                api_importlist=api_importlists[importlist_name],
            ):
                changed = True
        return changed

    def delete_remote(self, tree: str, secrets: RadarrSecrets, remote: Self) -> bool:
        updated = False
        with radarr_api_client(secrets=secrets) as api_client:
            importlist_ids: Dict[str, int] = {
                api_importlist.name: api_importlist.id
                for api_importlist in radarr.ImportListApi(api_client).list_import_list()
            }
        for importlist_name, importlist in remote.definitions.items():
            if importlist_name not in self.definitions:
                importlist_tree = f"{tree}.definitions[{importlist_name!r}]"
                if self.delete_unmanaged:
                    logger.info("%s: (...) -> (deleted)", importlist_tree)
                    importlist._delete_remote(
                        secrets=secrets,
                        importlist_id=importlist_ids[importlist_name],
                    )
                    updated = True
                else:
                    logger.debug("%s: (...) (unmanaged)", importlist_tree)
        if self.exclusions.delete_remote(
            tree=f"{tree}.exclusions",
            secrets=secrets,
            remote=remote.exclusions,
        ):
            updated = True
        return updated
