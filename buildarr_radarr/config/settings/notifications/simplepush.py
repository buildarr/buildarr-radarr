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
Simplepush notification connection configuration.
"""


from __future__ import annotations

from typing import List, Literal, Optional

from buildarr.config import RemoteMapEntry
from buildarr.types import Password

from .base import Notification


class SimplepushNotification(Notification):
    """
    Send media update and health alert messages to Simplepush.
    """

    type: Literal["simplepush"] = "simplepush"
    """
    Type value associated with this kind of connection.
    """

    api_key: Password
    """
    Simplepush API key.
    """

    event: Optional[str] = None
    """
    Customise the behaviour of push notification.
    """

    _implementation: str = "Simplepush"
    _remote_map: List[RemoteMapEntry] = [
        ("api_key", "key", {"is_field": True}),
        (
            "event",
            "event",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
    ]
