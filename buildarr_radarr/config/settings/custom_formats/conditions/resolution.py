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

from .....types import LowerCaseNonEmptyStr
from .base import Condition


class ResolutionCondition(Condition):
    """ """

    type: Literal["resolution"] = "resolution"
    """ """

    resolution: LowerCaseNonEmptyStr
    """Evaluate against available resolutions in Radarr API."""

    _implementation: Literal["ResolutionSpecification"] = "ResolutionSpecification"

    @classmethod
    def _get_remote_map(
        cls,
        api_schema: radarr.CustomFormatSpecificationSchema,
    ) -> List[RemoteMapEntry]:
        return [
            (
                "resolution",
                "value",
                {
                    "decoder": lambda v: cls._resolution_decode(api_schema, v),
                    "encoder": lambda v: cls._resolution_encode(api_schema, v),
                    "is_field": True,
                },
            ),
        ]

    @classmethod
    def _resolution_decode(
        cls,
        api_schema: radarr.CustomFormatSpecificationSchema,
        value: int,
    ) -> str:
        field: radarr.Field = next(f for f in api_schema.fields if f.name == "value")
        for o in field.select_options:
            option = cast(radarr.SelectOption, o)
            if option.value == value:
                return option.name.lower()
        supported_resolutions = ", ".join(
            (f"{o.name.lower()} ({o.value})" for o in field.select_options),
        )
        raise ValueError(
            f"Invalid custom format quality resolution value {value} during decoding"
            f", supported quality resolutions are: {supported_resolutions}",
        )

    @classmethod
    def _resolution_encode(
        cls,
        api_schema: radarr.CustomFormatSpecificationSchema,
        value: str,
    ) -> str:
        field: radarr.Field = next((f for f in api_schema.fields if f.name.lower == "value"))
        for o in field.select_options:
            option = cast(radarr.SelectOption, o)
            if option.name.lower() == value:
                return option.value
        supported_resolutions = ", ".join(o.name.lower() for o in field.select_options)
        raise ValueError(
            f"Invalid or unsupported custom format resolution name '{value}'"
            f", supported resolutions are: {supported_resolutions}",
        )
