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
from typing import Dict, List, Tuple, Type, Union

import radarr

from buildarr.config import RemoteMapEntry
from pydantic import Field
from typing_extensions import Annotated, Self

from ....api import radarr_api_client
from ....secrets import RadarrSecrets
from ...types import RadarrConfigBase
from .advanced import CustomlistImportist, RssImportList, StevenluCustomImportList
from .base import ImportList
from .exclusions import ListExclusionsSettings
from .other import ImdbListImportList, StevenluListImportList
from .plex import PlexWatchlistImportList
from .program import CouchpotatoImportList, RadarrImportList
from .tmdb import (
    TmdbCompanyImportList,
    TmdbKeywordImportList,
    TmdbListImportList,
    TmdbPersonImportList,
    TmdbPopularImportList,
    TmdbUserImportList,
)
from .trakt import TraktListImportList, TraktPopularlistImportList, TraktUserImportList

logger = getLogger(__name__)


IMPORTLIST_TYPES: Tuple[Type[ImportList], ...] = (
    CouchpotatoImportList,
    RadarrImportList,
    TmdbCompanyImportList,
    TmdbKeywordImportList,
    TmdbListImportList,
    TmdbPersonImportList,
    TmdbPopularImportList,
    TmdbUserImportList,
    TraktListImportList,
    TraktPopularlistImportList,
    TraktUserImportList,
    PlexWatchlistImportList,
    ImdbListImportList,
    StevenluListImportList,
    CustomlistImportist,
    RssImportList,
    StevenluCustomImportList,
)

IMPORTLIST_TYPE_MAP: Dict[str, Type[ImportList]] = {
    importlist_type._implementation.lower(): importlist_type for importlist_type in IMPORTLIST_TYPES
}

ImportListType = Union[
    CouchpotatoImportList,
    RadarrImportList,
    TmdbCompanyImportList,
    TmdbKeywordImportList,
    TmdbListImportList,
    TmdbPersonImportList,
    TmdbPopularImportList,
    TmdbUserImportList,
    TraktListImportList,
    TraktPopularlistImportList,
    TraktUserImportList,
    PlexWatchlistImportList,
    ImdbListImportList,
    StevenluListImportList,
    CustomlistImportist,
    RssImportList,
    StevenluCustomImportList,
]


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

    _remote_map: List[RemoteMapEntry] = [
        ("list_update_interval", "importListSyncInterval", {}),
        ("clean_library_level", "listSyncLevel", {}),
    ]

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
                api_importlist.name: IMPORTLIST_TYPE_MAP[
                    api_importlist.implementation.lower()
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
        # Flag for whether or not the import list configuration was updated or not.
        changed = False
        # Get required resource ID references from the remote Radarr instance.
        importlist_ids: Dict[str, int] = {
            importlist_json["name"]: importlist_json["id"]
            for importlist_json in api_get(secrets, "/api/v3/importlist")
        }
        quality_profile_ids: Dict[str, int] = {
            pro["name"]: pro["id"] for pro in api_get(secrets, "/api/v3/qualityprofile")
        }
        language_profile_ids: Dict[str, int] = {
            pro["name"]: pro["id"] for pro in api_get(secrets, "/api/v3/languageprofile")
        }
        tag_ids: Dict[str, int] = {
            tag["label"]: tag["id"] for tag in api_get(secrets, "/api/v3/tag")
        }
        # Evaluate locally defined import lists against the currently active ones
        # on the remote instance.
        for importlist_name, importlist in self.definitions.items():
            importlist = importlist._resolve(importlist_name)  # noqa: PLW2901
            importlist_tree = f"{tree}.definitions[{repr(importlist_name)}]"
            # If a locally defined import list does not exist on the remote, create it.
            if importlist_name not in remote.definitions:
                importlist._create_remote(
                    tree=importlist_tree,
                    secrets=secrets,
                    quality_profile_ids=quality_profile_ids,
                    language_profile_ids=language_profile_ids,
                    tag_ids=tag_ids,
                    importlist_name=importlist_name,
                )
                changed = True
            # Since there is an import list with the same name on the remote,
            # update it in-place.
            elif importlist._update_remote(
                tree=importlist_tree,
                secrets=secrets,
                remote=remote.definitions[importlist_name]._resolve_from_local(
                    name=importlist_name,
                    local=importlist,  # type: ignore[arg-type]
                    ignore_nonexistent_ids=True,
                ),
                quality_profile_ids=quality_profile_ids,
                language_profile_ids=language_profile_ids,
                tag_ids=tag_ids,
                importlist_id=importlist_ids[importlist_name],
                importlist_name=importlist_name,
            ):
                changed = True
        # We're done!
        return changed

    def delete_remote(self, tree: str, secrets: RadarrSecrets, remote: Self) -> bool:
        changed = False
        importlist_ids: Dict[str, int] = {
            importlist_json["name"]: importlist_json["id"]
            for importlist_json in api_get(secrets, "/api/v3/importlist")
        }
        for importlist_name, importlist in remote.definitions.items():
            if importlist_name not in self.definitions:
                importlist_tree = f"{tree}.definitions[{repr(importlist_name)}]"
                if self.delete_unmanaged:
                    logger.info("%s: (...) -> (deleted)", importlist_tree)
                    importlist._delete_remote(
                        secrets=secrets,
                        importlist_id=importlist_ids[importlist_name],
                    )
                    changed = True
                else:
                    logger.debug("%s: (...) (unmanaged)", importlist_tree)
        return changed
