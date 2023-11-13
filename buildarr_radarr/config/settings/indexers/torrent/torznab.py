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
Torznab indexer configuration.
"""


from __future__ import annotations

from typing import Iterable, List, Literal, Optional, Set, Union

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr, Password
from pydantic import AnyHttpUrl, validator

from ..util import NabCategory
from .base import TorrentIndexer


class TorznabIndexer(TorrentIndexer):
    # Monitor and search for new releases on a Torznab-compliant torrent indexing site.

    type: Literal["torznab"] = "torznab"
    """
    Type value associated with this kind of indexer.
    """

    base_url: AnyHttpUrl
    """
    URL of the Torznab-compatible indexing site.
    """

    api_path: NonEmptyStr = "/api"  # type: ignore[assignment]
    """
    Torznab API endpoint. Usually `/api`.
    """

    api_key: Password
    """
    API key for use with the Torznab API.
    """

    categories: Set[Union[NabCategory, int]] = {
        NabCategory.MOVIES_FOREIGN,
        NabCategory.MOVIES_OTHER,
        NabCategory.MOVIES_SD,
        NabCategory.MOVIES_HD,
        NabCategory.MOVIES_UHD,
        NabCategory.MOVIES_BLURAY,
        NabCategory.MOVIES_3D,
    }
    """
    Categories to monitor for standard/daily shows.
    Define as empty to disable.

    Values:

    * `Movies`
    * `Movies/Foreign`
    * `Movies/Other`
    * `Movies/SD`
    * `Movies/HD`
    * `Movies/UHD`
    * `Movies/BluRay`
    * `Movies/3D`
    * `Movies/DVD`
    * `Movies/WEB-DL`
    * `Movies/x265`
    """

    remove_year: bool = False
    """
    When set to `true`, excludes the release year of the media when searching the indexer.
    """

    additional_parameters: Optional[str] = None
    """
    Additional Torznab API parameters.
    """

    _implementation = "Torznab"
    _remote_map: List[RemoteMapEntry] = [
        ("base_url", "baseUrl", {"is_field": True}),
        ("api_path", "apiPath", {"is_field": True}),
        ("api_key", "apiKey", {"is_field": True}),
        (
            "categories",
            "categories",
            {"is_field": True, "encoder": lambda v: sorted(NabCategory.encode(c) for c in v)},
        ),
        ("remove_year", "removeYear", {"is_field": True}),
        (
            "additional_parameters",
            "additionalParameters",
            {"is_field": True, "field_default": None, "decoder": lambda v: v or None},
        ),
    ]

    @validator("categories")
    def validate_categories(
        cls,
        value: Iterable[Union[NabCategory, int]],
    ) -> Set[Union[NabCategory, int]]:
        return set(
            NabCategory.decode(category) if isinstance(category, int) else category
            for category in value
        )
