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
Custom format condition for matching based on media language.
"""


from __future__ import annotations

from typing import Any, Dict, List, Literal, cast

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr
from pydantic import validator

from ....util import language_parse
from .base import Condition


class LanguageCondition(Condition):
    # Custom format condition for matching based on media language.

    type: Literal["language"] = "language"
    """
    Buildarr type keyword associated with this condition type.
    """

    language: NonEmptyStr
    """
    The language to match against, written in English.

    Use the `any` keyword to match any language.
    Use the `original` keyword to match for the original language of the media.

    All languages supported by your Radarr instance version can be defined
    in this condition.

    Examples:

    * `english`
    * `portuguese-brazil`
    """

    _implementation: Literal["LanguageSpecification"] = "LanguageSpecification"

    @validator("language")
    def validate_language(cls, value: str) -> str:
        return language_parse(value)

    @classmethod
    def _get_remote_map(cls, api_schema_dict: Dict[str, Any]) -> List[RemoteMapEntry]:
        return [
            (
                "language",
                "value",
                {
                    "decoder": lambda v: cls._language_decode(api_schema_dict, v),
                    "encoder": lambda v: cls._language_encode(api_schema_dict, v),
                    "is_field": True,
                },
            ),
        ]

    @classmethod
    def _language_decode(cls, api_schema_dict: Dict[str, Any], value: int) -> str:
        field: Dict[str, Any] = next(f for f in api_schema_dict["fields"] if f["name"] == "value")
        select_options = cast(List[Dict[str, Any]], field["selectOptions"])
        for o in select_options:
            option = cast(Dict[str, Any], o)
            option_name = cast(str, option["name"])
            option_value = cast(int, option["value"])
            if option_value == value:
                return option_name.lower()
        supported_languages = ", ".join(
            (f"{o['name'].lower()} ({o['value']})" for o in select_options),
        )
        raise ValueError(
            f"Invalid custom format quality language value {value} during decoding"
            f", supported quality languages are: {supported_languages}",
        )

    @classmethod
    def _language_encode(cls, api_schema_dict: Dict[str, Any], value: str) -> int:
        field: Dict[str, Any] = next(f for f in api_schema_dict["fields"] if f["name"] == "value")
        select_options = cast(List[Dict[str, Any]], field["selectOptions"])
        for o in select_options:
            option = cast(Dict[str, Any], o)
            option_name = cast(str, option["name"])
            option_value = cast(int, option["value"])
            if option_name.lower() == value:
                return option_value
        supported_languages = ", ".join(o["name"].lower() for o in select_options)
        raise ValueError(
            f"Invalid or unsupported custom format language name '{value}'"
            f", supported languages are: {supported_languages}",
        )
