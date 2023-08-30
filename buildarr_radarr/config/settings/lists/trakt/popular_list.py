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
Trakt popular list import list configuration.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum

from .base import TraktImportList


class TraktPopularListType(BaseEnum):
    """
    Types of popularity list in Trakt.
    """

    trending = 0
    popular = 1
    anticipated = 2
    top_watched_by_week = 3
    top_watched_by_month = 4
    top_watched_by_year = 5
    top_watched_by_alltime = 6
    recommended_by_week = 7
    recommended_by_month = 8
    recommended_by_year = 9
    recommended_by_alltime = 10


class TraktPopularListImportList(TraktImportList):
    """
    Import media according to popularity-based lists on Trakt.
    """

    type: Literal["trakt-popular-list", "trakt-popularlist"] = "trakt-popular-list"
    """
    Type value associated with this kind of import list.
    """

    list_type: TraktPopularListType = TraktPopularListType.popular
    """
    Popularity-based list to import.

    Values:

    * `trending`
    * `popular`
    * `anticipated`
    * `top_watched_by_week`
    * `top_watched_by_month`
    * `top_watched_by_year`
    * `top_watched_by_alltime`
    * `recommended_by_week`
    * `recommended_by_month`
    * `recommended_by_year`
    * `recommended_by_alltime`
    """

    _implementation: str = "TraktPopularImport"
    _remote_map: List[RemoteMapEntry] = [("list_type", "traktListType", {"is_field": True})]
