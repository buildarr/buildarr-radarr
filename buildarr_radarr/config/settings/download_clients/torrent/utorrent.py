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
uTorrent download client configuration.
"""


from __future__ import annotations

from typing import List, Literal, Optional

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr, Password, Port

from .base import TorrentDownloadClient


class UtorrentPriority(BaseEnum):
    last = 0
    first = 1


class UtorrentState(BaseEnum):
    start = 0
    force_start = 1
    pause = 2
    stop = 3


class UtorrentDownloadClient(TorrentDownloadClient):
    # uTorrent download client.

    type: Literal["utorrent"] = "utorrent"
    """
    Type value associated with this kind of download client.
    """

    hostname: NonEmptyStr
    """
    uTorrent host name.
    """

    port: Port = 8080  # type: ignore[assignment]
    """
    Download client access port.
    """

    use_ssl: bool = False
    """
    Use a secure connection when connecting to the download client.
    """

    url_base: Optional[str] = None
    """
    Adds a prefix to the uTorrent URL, e.g. `http://[host]:[port]/[url_base]/api`.
    """

    username: NonEmptyStr
    """
    User name to use when authenticating with the download client.
    """

    password: Password
    """
    Password to use to authenticate the download client user.
    """

    category: Optional[str] = "radarr"
    """
    Associate media from Radarr with a category.

    Adding a category specific to Radarr avoids conflicts with unrelated non-Radarr downloads.
    Using a category is optional, but strongly recommended.
    """

    postimport_category: Optional[str] = "radarr"
    """
    Category for Radarr to set after it has imported the download.
    Radarr will not remove the torrent if seeding has finished.

    Leave blank to keep the same category as set in `category`.
    """

    recent_priority: UtorrentPriority = UtorrentPriority.last
    """
    Priority to use when grabbing media that released within the last 21 days.

    Values:

    * `last`
    * `first`
    """

    older_priority: UtorrentPriority = UtorrentPriority.last
    """
    Priority to use when grabbing media that released over 21 days ago.

    Values:

    * `last`
    * `first`
    """

    initial_state: UtorrentState = UtorrentState.start
    """
    Initial state for torrents added to uTorrent.
    """

    _implementation: str = "UTorrent"
    _remote_map: List[RemoteMapEntry] = [
        ("hostname", "host", {"is_field": True}),
        ("port", "port", {"is_field": True}),
        ("use_ssl", "useSsl", {"is_field": True}),
        (
            "url_base",
            "urlBase",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        ("username", "username", {"is_field": True}),
        ("password", "password", {"is_field": True}),
        (
            "category",
            "movieCategory",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        (
            "postimport_category",
            "movieImportedCategory",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        ("recent_priority", "recentMoviePriority", {"is_field": True}),
        ("older_priority", "olderMoviePriority", {"is_field": True}),
        ("initial_state", "initialState", {"is_field": True}),
    ]
