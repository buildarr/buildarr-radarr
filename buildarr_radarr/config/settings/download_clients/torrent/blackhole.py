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
Torrent Blackhole download client configuration.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr

from .base import TorrentDownloadClient


class TorrentBlackholeDownloadClient(TorrentDownloadClient):
    # Torrent Blackhole download client.

    type: Literal["torrent-blackhole"] = "torrent-blackhole"
    """
    Type value associated with this kind of download client.
    """

    torrent_folder: NonEmptyStr
    """
    Folder in which Radarr will store `.torrent` files.
    """

    watch_folder: NonEmptyStr
    """
    Folder from which Radarr should import completed downloads.
    """

    save_magnet_files: bool = False
    """
    Save the magnet link if no `.torrent` file is available.

    Only useful if the download client supports magnets saved to a file.
    """

    magnet_file_extension: NonEmptyStr = ".magnet"  # type: ignore[assignment]
    """
    Extension to use for magnet links.
    """

    read_only: bool = True
    """
    When set to `true`, this instructs Radarr to copy or hard link
    completed downloads to their final directory, instead of moving them.

    To allow torrents to continue seeding after download, this should be enabled.
    """

    _implementation: str = "TorrentBlackhole"
    _remote_map: List[RemoteMapEntry] = [
        ("torrent_folder", "torrentFolder", {"is_field": True}),
        ("watch_folder", "watchFolder", {"is_field": True}),
        ("save_magnet_files", "saveMagnetFiles", {"is_field": True}),
        ("magnet_file_extension", "magnetFileExtension", {"is_field": True}),
        ("read_only", "readOnly", {"is_field": True}),
    ]
