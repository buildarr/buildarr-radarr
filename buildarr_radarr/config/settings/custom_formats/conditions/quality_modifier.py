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

from typing import List, Literal, cast

import radarr

from buildarr.config import RemoteMapEntry

from .....types import UpperCaseNonEmptyStr
from .base import Condition


class QualityModifierCondition(Condition):
    """ """

    type: Literal["quality-modifier", "quality_modifier"] = "quality-modifier"
    """ """

    modifier: UpperCaseNonEmptyStr
    """Evaluate against available modifiers in Radarr API."""

    _implementation: Literal["QualityModifierSpecification"] = "QualityModifierSpecification"

    @classmethod
    def _get_remote_map(
        cls,
        api_schema: radarr.CustomFormatSpecificationSchema,
    ) -> List[RemoteMapEntry]:
        return [
            (
                "modifier",
                "value",
                {
                    "decoder": lambda v: cls._modifier_decode(api_schema, v),
                    "encoder": lambda v: cls._modifier_encode(api_schema, v),
                    "is_field": True,
                },
            ),
        ]

    @classmethod
    def _modifier_decode(
        cls,
        api_schema: radarr.CustomFormatSpecificationSchema,
        value: int,
    ) -> str:
        field: radarr.Field = next(f for f in api_schema.fields if f.name == "value")
        for o in field.select_options:
            option = cast(radarr.SelectOption, o)
            if option.value == value:
                return option.name.upper()
        supported_modifiers = ", ".join(
            (f"{o.name.upper()} ({o.value})" for o in field.select_options),
        )
        raise ValueError(
            f"Invalid custom format quality modifier value {value} during decoding"
            f", supported quality modifiers are: {supported_modifiers}",
        )

    @classmethod
    def _modifier_encode(
        cls,
        api_schema: radarr.CustomFormatSpecificationSchema,
        value: str,
    ) -> str:
        field: radarr.Field = next(f for f in api_schema.fields if f.name == "value")
        for o in field.select_options:
            option = cast(radarr.SelectOption, o)
            if option.name.upper() == value:
                return option.value
        supported_modifiers = ", ".join(o.name.upper() for o in field.select_options)
        raise ValueError(
            f"Invalid or unsupported custom format modifier name '{value}'"
            f", supported modifiers are: {supported_modifiers}",
        )
