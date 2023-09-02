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
Prowl notification connection configuration.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, Password

from .base import Notification


class ProwlPriority(BaseEnum):
    """
    Prowl notification priority.
    """

    verylow = -2
    low = -1
    normal = 0
    high = 1
    emergency = 2


class ProwlNotification(Notification):
    """
    Send media update and health alert push notifications to a Prowl client.
    """

    type: Literal["prowl"] = "prowl"
    """
    Type value associated with this kind of connection.
    """

    api_key: Password
    """
    API key to use when authenticating with Prowl.
    """

    priority: ProwlPriority = ProwlPriority.normal
    """
    Prowl push notification priority.

    Values:

    * `verylow`
    * `low`
    * `normal`
    * `high`
    * `emergency`
    """

    _implementation: str = "Prowl"
    _remote_map: List[RemoteMapEntry] = [
        ("api_key", "apiKey", {"is_field": True}),
        ("priority", "priority", {"is_field": True}),
    ]
