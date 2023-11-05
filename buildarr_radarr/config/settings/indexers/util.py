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

from buildarr.types import BaseEnum

logger = getLogger(__name__)


class NabCategory(BaseEnum):
    MOVIES = 2000
    MOVIES_FOREIGN = 2010
    MOVIES_OTHER = 2020
    MOVIES_SD = 2030
    MOVIES_HD = 2040
    MOVIES_UHD = 2045
    MOVIES_BLURAY = 2050
    MOVIES_3D = 2060
    MOVIES_DVD = 2070

    # TODO: Make the enum also accept these values.
    # MOVIES_FOREIGN = "Movies/Foreign"
    # MOVIES_OTHER = "Movies/Other"
    # MOVIES_SD = "Movies/SD"
    # MOVIES_HD = "Movies/HD"
    # MOVIES_UHD = "Movies/UHD"
    # MOVIES_3D = "Movies/3D"
    # MOVIES_DVD = "Movies/DVD"
