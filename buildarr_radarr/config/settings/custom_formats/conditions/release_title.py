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

from typing import List, Literal, Optional

from buildarr.config import RemoteMapEntry

from .base import Condition


class ReleaseTitleCondition(Condition):
    """ """

    type: Literal["release-title", "release_title", "releasetitle"] = "release-title"
    """ """

    regex: Optional[str] = None
    """Case insensitive."""

    preset: Optional[str] = None
    """Template preset from the Radarr API."""

    _implementation: Literal["ReleaseTitleSpecification"] = "ReleaseTitleSpecification"
    _remote_map: List[RemoteMapEntry] = [
        (
            "regex",
            "value",
            {"equals": lambda a, b: a.casefold() == b.casefold(), "is_field": True},
        ),
    ]
