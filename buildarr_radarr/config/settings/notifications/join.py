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
Join notification connection configuration.
"""


from __future__ import annotations

from typing import List, Literal, Set

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr, Password

from .base import Notification


class JoinPriority(BaseEnum):
    """
    Join notification priority.
    """

    silent = -2
    quiet = -1
    normal = 0
    high = 1
    emergency = 2


class JoinNotification(Notification):
    """
    Send media update and health alert push notifications via Join.
    """

    type: Literal["join"] = "join"
    """
    Type value associated with this kind of connection.
    """

    api_key: Password
    """
    API key to use to authenticate with Join.
    """

    # Only uncomment if absolutely required.
    # device_ids: Set[int] = set()

    device_names: Set[NonEmptyStr] = set()
    """
    List of full or partial device names you'd like to send notifications to.

    If unset or empty, all devices will receive notifications.
    """

    priority: JoinPriority = JoinPriority.normal
    """
    Join push notification priority.

    Values:

    * `silent`
    * `quiet`
    * `normal`
    * `high`
    * `emergency`
    """

    _implementation: str = "Join"
    _remote_map: List[RemoteMapEntry] = [
        ("api_key", "apiKey", {"is_field": True}),
        # ("device_ids", "deviceIds", {"is_field": True}),
        (
            "device_names",
            "deviceNames",
            {
                "is_field": True,
                "decoder": lambda v: (
                    set(d.strip() for d in v.split(",")) if v and v.strip() else set()
                ),
                "encoder": lambda v: ",".join(sorted(v)) if v else "",
            },
        ),
        ("priority", "priority", {"is_field": True}),
    ]
