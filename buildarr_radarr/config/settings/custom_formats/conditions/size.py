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
Custom format condition for matching based on media file size.
"""


from __future__ import annotations

from typing import Any, List, Literal, Mapping

from buildarr.config import RemoteMapEntry
from pydantic import Field, validator

from .base import Condition


class SizeCondition(Condition):
    # Custom format condition for matching based on media file size.

    type: Literal["size"] = "size"
    """
    Buildarr type keyword associated with this condition type.
    """

    min: int = Field(0, ge=0)
    """
    The minimum size, in gigabytes (GB).

    In order to match, the media must be larger than this size.
    """

    max: int = Field(1, ge=1)
    """
    The maximum size, in gigabytes (GB).

    In order to match, the media must be smaller than, or equal to, this size.
    """

    _implementation: Literal["SizeSpecification"] = "SizeSpecification"
    _remote_map: List[RemoteMapEntry] = [
        ("min", "min", {"is_field": True}),
        ("max", "max", {"is_field": True}),
    ]

    @validator("max")
    def validate_min_max(cls, value: int, values: Mapping[str, Any]) -> int:
        try:
            size_min: int = values["min"]
            if value < size_min:
                raise ValueError(
                    f"'max' ({value}) is not greater than 'min' ({size_min})",
                )
        except KeyError:
            # `min` only doesn't exist when it failed type validation.
            # If it doesn't exist, skip this validation.
            pass
        return value
