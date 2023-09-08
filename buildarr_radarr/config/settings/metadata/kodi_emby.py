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
Kodi (XBMC) / Emby metadata configuration.
"""


from __future__ import annotations

from typing import List, cast

import radarr

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr
from pydantic import validator

from ...util import language_parse
from .base import Metadata


class KodiEmbyMetadata(Metadata):
    # Output metadata files in a format suitable for Kodi (XBMC) or Emby.

    movie_metadata: bool = True
    """
    Create metadata file.
    """

    movie_metadata_url: bool = False
    """
    Add the TMDB/IMDB URL to the written metadata file.

    No effect if `movie_metadata` is `false`.
    """

    movie_metadata_language: NonEmptyStr = "english"  # type: ignore[assignment]
    """
    Write the metadata in the selected language (if available).

    When using a dialect of a language (e.g. Brazilian Portuguese),
    add the dialect type to the end, separated with a hypen, e.g. `portuguese-brazil`.

    `original` can be selected to use the original language of the media.
    """

    movie_images: bool = False
    """
    Save movie images.
    """

    use_movie_nfo: bool = False
    """
    Write movie metadata to `movie.nfo`, instead of the default `<movie-filename>.nfo`.
    """

    add_collection_name: bool = False
    """
    Write the collection name to the movie metadata.
    """

    _implementation: str = "XbmcMetadata"

    @validator("movie_metadata_language")
    def validate_movie_metadata_language(cls, value: str) -> str:
        return language_parse(value)

    @classmethod
    def _get_remote_map(cls, api_schema: radarr.MetadataResource) -> List[RemoteMapEntry]:
        return [
            ("movie_metadata", "movieMetadata", {"is_field": True}),
            ("movie_metadata_url", "movieMetadataURL", {"is_field": True}),
            (
                "movie_metadata_language",
                "movieMetadataLanguage",
                {
                    "decoder": lambda v: cls._movie_metadata_language_decode(api_schema, v),
                    "encoder": lambda v: cls._movie_metadata_language_encode(api_schema, v),
                    "is_field": True,
                },
            ),
            ("movie_images", "movieImages", {"is_field": True}),
            ("use_movie_nfo", "useMovieNfo", {"is_field": True}),
            ("add_collection_name", "addCollectionName", {"is_field": True}),
        ]

    @classmethod
    def _movie_metadata_language_decode(
        cls,
        api_schema: radarr.CustomFormatSpecificationSchema,
        value: int,
    ) -> str:
        field: radarr.Field = next(
            (f for f in api_schema.fields if f.name == "movieMetadataLanguage"),
        )
        for o in field.select_options:
            option = cast(radarr.SelectOption, o)
            if option.value == value:
                return language_parse(option.name)
        supported_languages = ", ".join(f"{o.name} ({o.value})" for o in field.select_options)
        raise ValueError(
            f"Invalid movie metadata language value {value} during decoding"
            f", supported languages are: {supported_languages}",
        )

    @classmethod
    def _movie_metadata_language_encode(
        cls,
        api_schema: radarr.CustomFormatSpecificationSchema,
        value: str,
    ) -> str:
        field: radarr.Field = next(
            (f for f in api_schema.fields if f.name == "movieMetadataLanguage"),
        )
        for o in field.select_options:
            option = cast(radarr.SelectOption, o)
            if language_parse(option.name) == value:
                return option.value
        supported_languages = ", ".join(
            (f"{o.name} ({language_parse(o.name)})" for o in field.select_options),
        )
        raise ValueError(
            f"Invalid or unsupported movie metadata language name '{value}'"
            f", supported languages are: {supported_languages}",
        )
