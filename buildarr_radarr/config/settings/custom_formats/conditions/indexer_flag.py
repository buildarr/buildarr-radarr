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
Custom format condition for matching based on indexer flags.
"""


from __future__ import annotations

from typing import Any, Dict, List, Literal, cast

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr
from pydantic import validator

from .base import Condition


class IndexerFlagCondition(Condition):
    # Custom format condition for matching based on indexer flags.

    type: Literal["indexer-flag", "indexer_flag", "indexerflag"] = "indexer-flag"
    """
    Buildarr type keywords associated with this condition type.
    """

    flag: NonEmptyStr
    """
    The indexer flag to match against.

    All values supported by your Radarr instance version can be defined.
    As of Radarr v4.7.5, the following flags are available:

    * `g-freeleech`
    * `g-halfleech`
    * `g-doubleupload`
    * `ptp-golden`
    * `ptp-approved`
    * `hdb-internal`
    * `ahd-internal`
    * `g-scene`
    * `g-freeleech75`
    * `g-freeleech25`
    * `ahd-userrelease`
    """

    _implementation: Literal["IndexerFlagSpecification"] = "IndexerFlagSpecification"

    @classmethod
    def _flag_parse(cls, value: str) -> str:
        # Results:
        #   1. G Freeleech -> g-freeleech
        #   2. G_FREELEECH -> g-freeleech
        return value.lower().replace("_", "-").replace(" ", "-")

    @validator("flag")
    def validate_flag(cls, value: str) -> str:
        return cls._flag_parse(value)

    @classmethod
    def _get_remote_map(cls, api_schema_dict: Dict[str, Any]) -> List[RemoteMapEntry]:
        return [
            (
                "flag",
                "value",
                {
                    "decoder": lambda v: cls._flag_decode(api_schema_dict, v),
                    "encoder": lambda v: cls._flag_encode(api_schema_dict, v),
                    "is_field": True,
                },
            ),
        ]

    @classmethod
    def _flag_decode(cls, api_schema_dict: Dict[str, Any], value: int) -> str:
        field: Dict[str, Any] = next(f for f in api_schema_dict["fields"] if f["name"] == "value")
        select_options = cast(List[Dict[str, Any]], field["selectOptions"])
        for o in select_options:
            option = cast(Dict[str, Any], o)
            option_name = cast(str, option["name"])
            option_value = cast(int, option["value"])
            if option_value == value:
                return cls._flag_parse(option_name)
        supported_flags = ", ".join(
            (f"{cls._flag_parse(o['name'])} ({o['value']})" for o in select_options),
        )
        raise ValueError(
            f"Invalid custom format quality flag value {value} during decoding"
            f", supported quality flags are: {supported_flags}",
        )

    @classmethod
    def _flag_encode(cls, api_schema_dict: Dict[str, Any], value: str) -> int:
        field: Dict[str, Any] = next(f for f in api_schema_dict["fields"] if f["name"] == "value")
        select_options = cast(List[Dict[str, Any]], field["selectOptions"])
        for o in select_options:
            option = cast(Dict[str, Any], o)
            option_name = cast(str, option["name"])
            option_value = cast(int, option["value"])
            if cls._flag_parse(option_name) == value:
                return option_value
        supported_flags = ", ".join(cls._flag_parse(o["name"]) for o in select_options)
        raise ValueError(
            f"Invalid or unsupported custom format flag name '{value}'"
            f", supported flags are: {supported_flags}",
        )
