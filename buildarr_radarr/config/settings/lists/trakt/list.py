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
Trakt list import list configuration.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr

from .base import TraktImportList


class TraktListImportList(TraktImportList):
    """
    Import an arbitrary list from Trakt into Radarr.
    """

    type: Literal["trakt-list"] = "trakt-list"
    """
    Type value associated with this kind of import list.
    """

    list_name: NonEmptyStr
    """
    Name of the list to import.

    The list must be public, or you must have access to the list.
    """

    _implementation: str = "TraktListImport"
    _remote_map: List[RemoteMapEntry] = [("list_name", "listName", {"is_field": True})]
