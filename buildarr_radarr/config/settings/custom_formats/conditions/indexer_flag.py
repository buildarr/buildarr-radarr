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
from __future__ import annotations

from typing import Any, Dict, List, Literal, cast

import radarr

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr

from .base import Condition


class IndexerFlagCondition(Condition):
    """ """

    type: Literal["indexer-flag", "indexer_flag"] = "indexer-flag"
    """ """

    flag: NonEmptyStr
    """If str, check against API. Otherwise, use integer value directly."""

    _implementation: Literal["IndexerFlagSpecification"] = "IndexerFlagSpecification"

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
    def _flag_parse(cls, value: str) -> str:
        # Results:
        #   1. G Freeleech -> g-freeleech
        #   2. G_FREELEECH -> g-freeleech
        return value.lower().replace("_", "-").replace(" ", "-")

    @classmethod
    def _flag_decode(
        cls,
        api_schema: radarr.CustomFormatSpecificationSchema,
        value: int,
    ) -> str:
        field: radarr.Field = next(f for f in api_schema.fields if f.name == "value")
        for o in field.select_options:
            option = cast(radarr.SelectOption, o)
            if option.value == value:
                return cls._flag_parse(option.name)
        supported_flags = ", ".join(f"{o.name} ({o.value})" for o in field.select_options)
        raise ValueError(
            f"Invalid custom format flag value {value} during decoding"
            f", supported flags are: {supported_flags}",
        )

    @classmethod
    def _flag_encode(cls, api_schema_dict: Dict[str, Any], value: str) -> str:
        field: radarr.Field = next(f for f in api_schema_dict["fields"] if f["name"] == "value")
        for o in field.select_options:
            option = cast(radarr.SelectOption, o)
            if cls._flag_parse(option.name) == value:
                return option.value
        supported_flags = ", ".join(
            (f"{o.name} ({cls._flag_parse(o.name)})" for o in field.select_options),
        )
        raise ValueError(
            f"Invalid or unsupported custom format flag name '{value}'"
            f", supported flags are: {supported_flags}",
        )
