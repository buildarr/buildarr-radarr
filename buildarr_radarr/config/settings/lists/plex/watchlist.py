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
Plex watchlist import list configuration.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry
from buildarr.types import Password

from .base import PlexImportList


class PlexWatchlistImportList(PlexImportList):
    """
    Import items from a Plex watchlist.
    """

    type: Literal["plex-watchlist"] = "plex-watchlist"
    """
    Type value associated with this kind of import list.
    """

    access_token: Password
    """
    Plex authentication token.

    If unsure on where to find this token,
    [follow this guide from Plex.tv][PATH].
    [PATH]: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token
    """

    _implementation_name: str = "Plex Watchlist"
    _implementation: str = "PlexImport"
    _config_contract: str = "PlexListSettings"
    _remote_map: List[RemoteMapEntry] = [("access_token", "accessToken", {"is_field": True})]
