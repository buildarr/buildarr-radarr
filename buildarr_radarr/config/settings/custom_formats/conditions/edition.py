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
Custom format condition for matching based on media edition.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr

from .base import Condition


class EditionCondition(Condition):
    # Custom format condition for matching based on media edition.

    type: Literal["edition"] = "edition"
    """
    Buildarr type keyword associated with this condition type.
    """

    regex: NonEmptyStr
    """
    The regular expression to use to match editions to the custom format.

    Regular expression matching is case-insensitive.
    """

    _implementation: Literal["EditionSpecification"] = "EditionSpecification"
    _remote_map: List[RemoteMapEntry] = [
        (
            "regex",
            "value",
            {"equals": lambda a, b: a.casefold() == b.casefold(), "is_field": True},
        ),
    ]
