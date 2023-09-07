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
Download Station torrent download client configuration.
"""


from __future__ import annotations

from typing import List, Literal, Optional

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr, Password, Port

from .base import TorrentDownloadClient


class DownloadstationTorrentDownloadClient(TorrentDownloadClient):
    # Download client which uses torrents via Download Station.

    type: Literal["downloadstation-torrent"] = "downloadstation-torrent"
    """
    Type value associated with this kind of download client.
    """

    hostname: NonEmptyStr
    """
    Download Station host name.
    """

    port: Port = 5000  # type: ignore[assignment]
    """
    Download client access port.
    """

    use_ssl: bool = False
    """
    Use a secure connection when connecting to the download client.
    """

    username: NonEmptyStr
    """
    User name to use when authenticating with the download client.
    """

    password: Password
    """
    Password to use to authenticate the download client user.
    """

    category: Optional[str] = None
    """
    Associate media from Radarr with a category.
    Creates a `[category]` subdirectory in the output directory.

    Adding a category specific to Radarr avoids conflicts with unrelated non-Radarr downloads.
    Using a category is optional, but strongly recommended.
    """

    directory: Optional[str] = None
    """
    Optional shared folder to put downloads into.

    Leave blank, set to `null` or undefined to use the default download client location.
    """

    _implementation: str = "TorrentDownloadStation"
    _remote_map: List[RemoteMapEntry] = [
        ("hostname", "host", {"is_field": True}),
        ("port", "port", {"is_field": True}),
        ("use_ssl", "useSsl", {"is_field": True}),
        ("username", "username", {"is_field": True}),
        ("password", "password", {"is_field": True}),
        (
            "category",
            "tvCategory",  # Yes, this is supposed to be `tvCategory`.
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        (
            "directory",
            "tvDirectory",  # Yes, this is supposed to be `tvDirectory`.
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
    ]
