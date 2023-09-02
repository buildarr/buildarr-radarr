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
Boxcar notification connection configuration.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry
from buildarr.types import Password

from .base import Notification


class BoxcarNotification(Notification):
    """
    Receive media update and health alert push notifications via Boxcar.
    """

    type: Literal["boxcar"] = "boxcar"
    """
    Type value associated with this kind of connection.
    """

    access_token: Password
    """
    Access token for authenticating with Boxcar.
    """

    _implementation: str = "Boxcar"
    _remote_map: List[RemoteMapEntry] = [("access_token", "token", {"is_field": True})]
