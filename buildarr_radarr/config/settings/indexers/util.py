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
Indexer configuration utility classes and functions.
"""


from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, cast

from buildarr.types import BaseEnum

if TYPE_CHECKING:
    from typing import Union

    from typing_extensions import Self

logger = getLogger(__name__)


class NabCategory(BaseEnum):
    # https://github.com/Prowlarr/Prowlarr/blob/develop/src/NzbDrone.Core/Indexers/NewznabStandardCategory.cs
    MOVIES = (2000, "Movies")
    MOVIES_FOREIGN = (2010, "Movies/Foreign")
    MOVIES_OTHER = (2020, "Movies/Other")
    MOVIES_SD = (2030, "Movies/SD")
    MOVIES_HD = (2040, "Movies/HD")
    MOVIES_UHD = (2045, "Movies/UHD")
    MOVIES_BLURAY = (2050, "Movies/BluRay")
    MOVIES_3D = (2060, "Movies/3D")
    MOVIES_DVD = (2070, "Movies/DVD")
    MOVIES_WEBDL = (2080, "Movies/WEB-DL")
    MOVIES_X265 = (2090, "Movies/x265")

    @classmethod
    def decode(cls, value: int) -> Union[Self, int]:
        try:
            return cls(value)
        except ValueError:
            return value

    @classmethod
    def encode(cls, value: Union[Self, int]) -> int:
        return value if isinstance(value, int) else cast(int, value.value)
