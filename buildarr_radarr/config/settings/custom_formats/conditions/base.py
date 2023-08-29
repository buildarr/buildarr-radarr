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


from typing import List

import radarr

from buildarr.config import RemoteMapEntry
from typing_extensions import Self

from ....types import RadarrConfigBase


class Condition(RadarrConfigBase):
    """ """

    negate: bool = False
    """ """

    required: bool = False
    """ """

    _implementation: str
    _base_remote_map: List[RemoteMapEntry] = [
        ("negate", "negate", {}),
        ("required", "required", {}),
    ]
    _remote_map: List[RemoteMapEntry] = []

    @classmethod
    def _get_remote_map(
        cls,
        api_schema: radarr.CustomFormatSpecificationSchema,
    ) -> List[RemoteMapEntry]:
        return []

    @classmethod
    def _from_remote(
        cls,
        api_schema: radarr.CustomFormatSpecificationSchema,
        api_condition: radarr.CustomFormatSpecificationSchema,
    ) -> Self:
        return cls(
            **cls.get_local_attrs(
                remote_map=(
                    cls._base_remote_map
                    + cls._get_remote_map(api_schema)
                    + cls._remote_map
                ),
                remote_attrs=api_condition.to_dict(),
            ),
        )
