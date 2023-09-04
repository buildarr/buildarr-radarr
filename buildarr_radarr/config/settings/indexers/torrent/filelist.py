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
    # TODO: Use post_init_render to read the values from Radarr API.
    MOVIES_SD = "Movies SD"
    MOVIES_DVD = "Movies DVD"
    MOVIES_DVD_RO = "Movies DVD-RO"
    MOVIES_HD = "Movies HD"
    MOVIES_HD_RO = "Movies HD-RO"
    MOVIES_4K = "Movies 4K"
    MOVIES_BLURAY = "Movies Blu-Ray"
    MOVIES_4K_BLURAY = "Movies 4K Blu-Ray"
    MOVIES_3D = "Movies 3D"
    XXX = "XXX"


class FilelistIndexer(TorrentIndexer):
    # Monitor for new releases on FileList.io.

    type: Literal["filelist"] = "filelist"
    """
    Type value associated with this kind of indexer.
    """

    base_url: AnyHttpUrl = "https://filelist.io"  # type: ignore[assignment]
    """
    FileList API URL.

    Do not change this unless you know what you're doing,
    as your API key will be sent to this host.
    """

    username: NonEmptyStr
    """
    FileList username.
    """

    passkey: Password
    """
    FileList account API key.
    """

    categories: Set[FilelistCategory] = {
        FilelistCategory.MOVIES_HD,
        FilelistCategory.MOVIES_SD,
        FilelistCategory.MOVIES_4K,
    }
    """
    Categories to monitor for standard/daily show new releases.

    Set to an empty list to not monitor for standard/daily shows.

    Values:

    * `Movies SD`
    * `Movies DVD`
    * `Movies DVD-RO`
    * `Movies HD`
    * `Movies HD-RO`
    * `Movies 4K`
    * `Movies Blu-Ray`
    * `Movies 4K Blu-Ray`
    * `Movies 3D`
    * `XXX`
    """

    _implementation = "FileList"
    _remote_map: List[RemoteMapEntry] = [
        ("base_url", "baseUrl", {"is_field": True}),
        ("username", "username", {"is_field": True}),
        ("passkey", "passKey", {"is_field": True}),
        ("categories", "categories", {"is_field": True}),
    ]
