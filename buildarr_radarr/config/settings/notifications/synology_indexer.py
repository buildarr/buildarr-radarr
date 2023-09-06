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
SynologyIndexer notification connection configuration.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry

from .base import Notification


class SynologyIndexerNotification(Notification):
    """
    Send media update and health alert push notifications to a Synology Indexer.
    """

    type: Literal["synology-indexer", "synology"] = "synology-indexer"
    """
    Type values associated with this kind of connection.
    """

    update_library: bool = False
    """
    Call `synoindex` on `localhost` to update library files.
    """

    _implementation: str = "MediaBrowser"
    _remote_map: List[RemoteMapEntry] = [("update_library", "updateLibrary", {"is_field": True})]
