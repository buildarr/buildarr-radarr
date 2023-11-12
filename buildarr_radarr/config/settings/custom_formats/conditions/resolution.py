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
Custom format condition for matching based on media resolution.
"""


from __future__ import annotations

from typing import Any, Dict, List, Literal, cast

from buildarr.config import RemoteMapEntry
from buildarr.types import LowerCaseNonEmptyStr

from .base import Condition


class ResolutionCondition(Condition):
    # Custom format condition for matching based on media resolution.

    type: Literal["resolution"] = "resolution"
    """
    Buildarr type keyword associated with this condition type.
    """

    # TODO: Support integer resolutions using post_init_render.

    resolution: LowerCaseNonEmptyStr
    """
    The resolution to match against.

    All values supported by your Radarr instance version can be defined.
    As of Radarr v4.7.5, the following resolutions are available:

    * `r360p` (360p)
    * `r480p` (480p)
    * `r576p` (576p)
    * `r720p` (720p)
    * `r1080p` (1080p HD)
    * `r2160p` (2160p Ultra-HD)
    """

    _implementation: Literal["ResolutionSpecification"] = "ResolutionSpecification"

    @classmethod
    def _get_remote_map(cls, api_schema_dict: Dict[str, Any]) -> List[RemoteMapEntry]:
        return [
            (
                "resolution",
                "value",
                {
                    "decoder": lambda v: cls._resolution_decode(api_schema_dict, v),
                    "encoder": lambda v: cls._resolution_encode(api_schema_dict, v),
                    "is_field": True,
                },
            ),
        ]

    @classmethod
    def _resolution_decode(cls, api_schema_dict: Dict[str, Any], value: int) -> str:
        field: Dict[str, Any] = next(f for f in api_schema_dict["fields"] if f["name"] == "value")
        select_options = cast(List[Dict[str, Any]], field["selectOptions"])
        for o in select_options:
            option = cast(Dict[str, Any], o)
            option_name = cast(str, option["name"])
            option_value = cast(int, option["value"])
            if option_value == value:
                return option_name.lower()
        supported_resolutions = ", ".join(
            (f"{o['name'].lower()} ({o['value']})" for o in select_options),
        )
        raise ValueError(
            f"Invalid custom format quality resolution value {value} during decoding"
            f", supported quality resolutions are: {supported_resolutions}",
        )

    @classmethod
    def _resolution_encode(cls, api_schema_dict: Dict[str, Any], value: str) -> int:
        field: Dict[str, Any] = next(f for f in api_schema_dict["fields"] if f["name"] == "value")
        select_options = cast(List[Dict[str, Any]], field["selectOptions"])
        for o in select_options:
            option = cast(Dict[str, Any], o)
            option_name = cast(str, option["name"])
            option_value = cast(int, option["value"])
            if option_name.lower() == value:
                return option_value
        supported_resolutions = ", ".join(o["name"].lower() for o in select_options)
        raise ValueError(
            f"Invalid or unsupported custom format resolution name '{value}'"
            f", supported resolutions are: {supported_resolutions}",
        )
