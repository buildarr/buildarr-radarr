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
Trakt user import list configuration.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum

from .base import TraktImportList


class TraktUserListType(BaseEnum):
    """
    Types of user list in Trakt.
    """

    user_watch_list = 0
    user_watched_list = 1
    user_collection_list = 2


class TraktUserImportList(TraktImportList):
    """
    Import a user-level list from Trakt.
    """

    type: Literal["trakt-user"] = "trakt-user"
    """
    Type value associated with this kind of import list.
    """

    list_type: TraktUserListType = TraktUserListType.user_watch_list
    """
    User list type to import.

    Values:

    * `user_watch_list`
    * `user_watched_list`
    * `user_collection_list`
    """

    _implementation: str = "TraktUserImport"
    _remote_map: List[RemoteMapEntry] = [("list_type", "traktListType", {"is_field": True})]
