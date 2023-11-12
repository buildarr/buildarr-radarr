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
from typing import TYPE_CHECKING

from aenum import MultiValueEnum

if TYPE_CHECKING:
    from typing import Any, Callable, Generator

    from typing_extensions import Self

logger = getLogger(__name__)


class NabCategory(MultiValueEnum):
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
    def from_name_str(cls, name_str: str) -> Self:
        """
        Get the enumeration object corresponding to the given name case-insensitively.

        Args:
            name_str (str): Name of the enumeration value, or its remote representation.

        Raises:
            KeyError: When the enumeration name is invalid (does not exist).

        Returns:
            The enumeration object for the given name
        """
        name = name_str.lower().replace("/", "_").replace("-", "_")
        for obj in cls:  # type: ignore[attr-defined]
            if (
                obj.name.lower() == name
                or obj.values[1].lower().replace("/", "_").replace("-", "_") == name
            ):
                return obj
        raise KeyError(repr(name))

    def to_name_str(self) -> str:
        """
        Return the name for this enumaration object.

        Returns:
            Remote representation name
        """
        return self.values[1]

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[Any], Self], None, None]:
        """
        Pass class validation functions to Pydantic.

        Yields:
            Validation class functions
        """
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> Self:
        """
        Validate and coerce the given value to an enumeration object.

        Args:
            value (Any): Object to validate and coerce

        Raises:
            ValueError: If a enumeration object corresponding with the value cannot be found

        Returns:
            Enumeration object corresponding to the given value
        """
        try:
            return cls(value)
        except ValueError:
            try:
                return cls.from_name_str(value)
            except (TypeError, KeyError):
                raise ValueError(f"Invalid {cls.__name__} name or value: {value}") from None
