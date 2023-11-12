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
Custom format condition for matching based on quality modifiers.
"""


from __future__ import annotations

from typing import Any, Dict, List, Literal, cast

from buildarr.config import RemoteMapEntry
from buildarr.types import UpperCaseNonEmptyStr

from .base import Condition


class QualityModifierCondition(Condition):
    # Custom format condition for matching based on quality modifiers.

    type: Literal[
        "quality-modifier",
        "quality_modifier",
        "qualitymodifier",
        "quality",
    ] = "quality-modifier"
    """
    Buildarr type keywords associated with this condition type.
    """

    modifier: UpperCaseNonEmptyStr
    """
    The modifier to match against.

    All values supported by your Radarr instance version can be defined.
    As of Radarr v4.7.5, the following modifiers are available:

    * `NONE`
    * `REGIONAL`
    * `SCREENER`
    * `RAWHD`
    * `BRDISK`
    * `REMUX`
    """

    # TODO: Support presets.
    # preset: Optional[str] = None
    # """Template preset from the Radarr API."""

    _implementation: Literal["QualityModifierSpecification"] = "QualityModifierSpecification"

    @classmethod
    def _get_remote_map(cls, api_schema_dict: Dict[str, Any]) -> List[RemoteMapEntry]:
        return [
            (
                "modifier",
                "value",
                {
                    "decoder": lambda v: cls._modifier_decode(api_schema_dict, v),
                    "encoder": lambda v: cls._modifier_encode(api_schema_dict, v),
                    "is_field": True,
                },
            ),
        ]

    @classmethod
    def _modifier_decode(cls, api_schema_dict: Dict[str, Any], value: int) -> str:
        field: Dict[str, Any] = next(f for f in api_schema_dict["fields"] if f["name"] == "value")
        select_options = cast(List[Dict[str, Any]], field["selectOptions"])
        for o in select_options:
            option = cast(Dict[str, Any], o)
            option_name = cast(str, option["name"])
            option_value = cast(int, option["value"])
            if option_value == value:
                return option_name.upper()
        supported_modifiers = ", ".join(
            (f"{o['name'].upper()} ({o['value']})" for o in select_options),
        )
        raise ValueError(
            f"Invalid custom format quality modifier value {value} during decoding"
            f", supported quality modifiers are: {supported_modifiers}",
        )

    @classmethod
    def _modifier_encode(cls, api_schema_dict: Dict[str, Any], value: str) -> int:
        field: Dict[str, Any] = next(f for f in api_schema_dict["fields"] if f["name"] == "value")
        select_options = cast(List[Dict[str, Any]], field["selectOptions"])
        for o in select_options:
            option = cast(Dict[str, Any], o)
            option_name = cast(str, option["name"])
            option_value = cast(int, option["value"])
            if option_name.upper() == value:
                return option_value
        supported_modifiers = ", ".join(o["name"].upper() for o in select_options)
        raise ValueError(
            f"Invalid or unsupported custom format modifier name '{value}'"
            f", supported modifiers are: {supported_modifiers}",
        )
