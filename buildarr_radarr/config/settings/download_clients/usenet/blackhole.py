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
Usenet Blackhole download client configuration.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr

from .base import UsenetDownloadClient


class UsenetBlackholeDownloadClient(UsenetDownloadClient):
    # Usenet Blackhole download client.

    type: Literal["usenet-blackhole"] = "usenet-blackhole"
    """
    Type value associated with this kind of download client.
    """

    nzb_folder: NonEmptyStr
    """
    Folder in which Radarr will store `.nzb` files.
    """

    watch_folder: NonEmptyStr
    """
    Folder from which Radarr should import completed downloads.
    """

    _implementation: str = "UsenetBlackhole"
    _remote_map: List[RemoteMapEntry] = [
        ("nzb_folder", "nzbFolder", {"is_field": True}),
        ("watch_folder", "watchFolder", {"is_field": True}),
    ]
