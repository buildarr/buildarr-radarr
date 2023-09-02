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
Radarr plugin Usenet indexers configuration.
"""


from __future__ import annotations

from typing import List, Literal, Optional, Set

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr, Password
from pydantic import AnyHttpUrl

from ..util import NabCategory
from .base import UsenetIndexer


class NewznabIndexer(UsenetIndexer):
    """
    An indexer for monitoring a Newznab-compliant Usenet indexing site.
    """

    type: Literal["newznab"] = "newznab"
    """
    Type value associated with this kind of indexer.
    """

    url: AnyHttpUrl
    """
    URL of the Newznab-compatible indexing site.
    """

    api_path: NonEmptyStr = "/api"  # type: ignore[assignment]
    """
    Newznab API endpoint. Usually `/api`.
    """

    api_key: Password
    """
    API key for use with the Newznab API.
    """

    categories: Set[NabCategory] = {
        NabCategory.MOVIES_FOREIGN,
        NabCategory.MOVIES_OTHER,
        NabCategory.MOVIES_SD,
        NabCategory.MOVIES_HD,
        NabCategory.MOVIES_UHD,
        NabCategory.MOVIES_BLURAY,
        NabCategory.MOVIES_3D,
    }
    """
    Categories to monitor for release.
    Define as empty to disable.

    Values:

    * `Movies-Foreign`
    * `Movies-Other`
    * `Movies-SD`
    * `Movies-HD`
    * `Movies-UHD`
    * `Movies-Bluray`
    * `Movies-3D`
    """

    anime_categories: Set[NabCategory] = set()
    """
    Categories to monitor for anime.
    Define as empty to disable.

    Values:

    * `TV-WEBDL`
    * `TV-Foreign`
    * `TV-SD`
    * `TV-HD`
    * `TV-UHD`
    * `TV-Other`
    * `TV-Sports`
    * `TV-Anime`
    * `TV-Documentary`
    """

    anime_standard_format_search: bool = False
    """
    Also search for anime using the standard numbering. Only applies for Anime series types.
    """

    additional_parameters: Optional[str] = None
    """
    Additional Newznab API parameters.
    """

    # TODO: Add support for presets.

    _implementation = "Newznab"
    _remote_map: List[RemoteMapEntry] = [
        ("url", "baseUrl", {"is_field": True}),
        ("api_path", "apiPath", {"is_field": True}),
        ("api_key", "apiKey", {"is_field": True}),
        (
            "categories",
            "categories",
            {"is_field": True, "encoder": lambda v: sorted(c.value for c in v)},
        ),
        (
            "anime_categories",
            "animeCategories",
            {"is_field": True, "encoder": lambda v: sorted(c.value for c in v)},
        ),
        ("anime_standard_format_search", "animeStandardFormatSearch", {"is_field": True}),
        (
            "additional_parameters",
            "additionalParameters",
            {"is_field": True, "field_default": None, "decoder": lambda v: v or None},
        ),
    ]