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

from typing import List, Literal, Mapping, Optional, Set

import radarr

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr, Password
from pydantic import AnyHttpUrl, validator

from ....util import language_parse
from ..util import NabCategory
from .base import TorrentIndexer


class TorznabIndexer(TorrentIndexer):
    """
    Monitor and search for new releases on a Torznab-compliant torrent indexing site.
    """

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
    Tornab API endpoint. Usually `/api`.
    """

    api_key: Password
    """
    API key for use with the Torznab API.
    """

    multi_languages: Set[NonEmptyStr] = set()
    """
    The list of languages normally found on a multi-release grabbed from this indexer.

    The special value `original` can also be specified,
    to include the original language of the media.
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
    Categories to monitor for standard/daily shows.
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

    additional_parameters: Optional[str] = None
    """
    Additional Torznab API parameters.
    """

    _implementation = "Torznab"

    @classmethod
    def _get_remote_map(
        cls,
        api_schema: radarr.IndexerResource,
        downloadclient_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
    ) -> List[RemoteMapEntry]:
        return [
            ("base_url", "baseUrl", {"is_field": True}),
            ("api_path", "apiPath", {"is_field": True}),
            ("api_key", "apiKey", {"is_field": True}),
            (
                "multi_languages",
                "multiLanguages",
                {
                    "decoder": lambda v: set(cls._language_decode(api_schema, la) for la in v),
                    "encoder": lambda v: sorted(cls._language_encode(api_schema, la) for la in v),
                    "is_field": True,
                },
            ),
            ("categories", "categories", {"is_field": True}),
            (
                "additional_parameters",
                "additionalParameters",
                {"is_field": True, "field_default": None, "decoder": lambda v: v or None},
            ),
        ]

    @classmethod
    def _language_parse(cls, value: str) -> str:
        # Results:
        #   1. English -> english
        #   2. english -> english
        #   3. ENGLISH -> english
        #   4. Portuguese (Brazil) -> portuguese-brazil
        #   5. portuguese_brazil -> portuguese-brazil
        #   6. PORTUGUESE-BRAZIL -> portuguese-brazil
        return "-".join(value.lower().replace("_", "-").replace("()", "").split(" "))

    @validator("multi_languages")
    def validate_language(cls, value: Set[str]) -> Set[str]:
        return set(language_parse(language) for language in value)

    @classmethod
    def _language_decode(cls, api_schema: radarr.IndexerResource, value: str) -> str:
        field: radarr.Field = next(f for f in api_schema.fields if f.name == "multiLanguages")
        select_options: List[radarr.SelectOption] = field.select_options
        for option in select_options:
            option_name: str = option.name
            option_value: int = option.value
            if option_value == value:
                return option_name.lower()
        supported_languages = ", ".join(f"{o.name.lower()} ({o.value})" for o in select_options)
        raise ValueError(
            f"Invalid custom format quality language value {value} during decoding"
            f", supported quality languages are: {supported_languages}",
        )

    @classmethod
    def _language_encode(cls, api_schema: radarr.IndexerResource, value: str) -> int:
        field: radarr.Field = next(f for f in api_schema.fields if f.name == "multiLanguages")
        select_options: List[radarr.SelectOption] = field.select_options
        for option in select_options:
            option_name: str = option.name
            option_value: int = option.value
            if option_name.lower() == value:
                return option_value
        supported_languages = ", ".join(o.name.lower() for o in select_options)
        raise ValueError(
            f"Invalid or unsupported custom format language name '{value}'"
            f", supported languages are: {supported_languages}",
        )
