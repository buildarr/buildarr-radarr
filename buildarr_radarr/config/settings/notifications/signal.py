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
Signal notification connection configuration.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr, Password, Port

from .base import Notification


class SignalNotification(Notification):
    """
    Send media update and health alert messages to a Signal user/group.
    """

    type: Literal["signal"] = "signal"
    """
    Type value associated with this kind of connection.
    """

    hostname: NonEmptyStr
    """
    Signal API hostname.
    """

    port: Port = 8080  # type: ignore[assignment]
    """
    Signal API access port.
    """

    use_ssl: bool = False
    """
    Use HTTPS instead of HTTP when connecting to Signal API.
    """

    sender_number: NonEmptyStr
    """
    Phone number of the sender registered in Signal.
    """

    receiver_id: NonEmptyStr
    """
    Group ID / phone number of the receiver.
    """

    username: NonEmptyStr
    """
    Signal API auth username.
    """

    password: Password
    """
    Signal API auth password.
    """

    _implementation: str = "Signal"
    _remote_map: List[RemoteMapEntry] = [
        ("hostname", "host", {"is_field": True}),
        ("port", "port", {"is_field": True}),
        ("use_ssl", "useSsl", {"is_field": True}),
        ("sender_number", "senderNumber", {"is_field": True}),
        ("receiver_id", "receiverId", {"is_field": True}),
        ("username", "authUsername", {"is_field": True}),
        ("password", "authPassword", {"is_field": True}),
    ]
