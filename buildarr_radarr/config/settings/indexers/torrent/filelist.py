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
FileList.io indexer configuration.
"""


from __future__ import annotations

from typing import List, Literal, Set

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr, Password
from pydantic import AnyHttpUrl

from .base import TorrentIndexer


class FilelistCategory(BaseEnum):
    """
    Filelist category enumeration.
    """

    ANIME = "Anime"
    ANIMATION = "Animation"
    TV_4K = "TV 4K"
    TV_HD = "TV HD"
    TV_SD = "TV SD"
    SPORT = "Sport"


class FilelistIndexer(TorrentIndexer):
    """
    Monitor for new releases on FileList.io.
    """

    type: Literal["filelist"] = "filelist"
    """
    Type value associated with this kind of indexer.
    """

    username: NonEmptyStr
    """
    FileList username.
    """

    passkey: Password
    """
    FileList account API key.
    """

    api_url: AnyHttpUrl = "https://filelist.io"  # type: ignore[assignment]
    """
    FileList API URL.

    Do not change this unless you know what you're doing,
    as your API key will be sent to this host.
    """

    categories: Set[FilelistCategory] = {
        FilelistCategory.TV_SD,
        FilelistCategory.TV_HD,
        FilelistCategory.TV_4K,
    }
    """
    Categories to monitor for standard/daily show new releases.

    Set to an empty list to not monitor for standard/daily shows.

    Values:

    * `Anime`
    * `Animation`
    * `TV 4K`
    * `TV HD`
    * `TV SD`
    * `Sport`
    """

    anime_categories: Set[FilelistCategory] = set()
    """
    Categories to monitor for anime new releases.

    Leave empty to not monitor for anime.

    Values:

    * `Anime`
    * `Animation`
    * `TV 4K`
    * `TV HD`
    * `TV SD`
    * `Sport`
    """

    _implementation = "FileList"
    _remote_map: List[RemoteMapEntry] = [
        ("username", "username", {"is_field": True}),
        ("passkey", "passKey", {"is_field": True}),
        ("api_url", "apiUrl", {"is_field": True}),
        (
            "categories",
            "categories",
            {"is_field": True, "encoder": lambda v: sorted(c.value for c in v)},
        ),
        (
            "anime_categories",
            "animeCategories",
            {"is_field": True, "encoder": lambda v: sorted(c.value for c in v)},
        ),
    ]
