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
Pushbullet notification connection configuration.
"""


from __future__ import annotations

from typing import List, Literal, Optional, Set

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr, Password

from .base import Notification


class PushbulletNotification(Notification):
    """
    Send media update and health alert push notifications to Pushbullet devices.
    """

    type: Literal["pushbullet"] = "pushbullet"
    """
    Type value associated with this kind of connection.
    """

    api_key: Password
    """
    API key to use when authenticating with Pushbullet.
    """

    device_ids: Set[NonEmptyStr] = set()
    """
    List of device IDs to send notifications to.

    If unset or empty, send to all devices.
    """

    channel_tags: Set[NonEmptyStr] = set()
    """
    List of Channel Tags to send notifications to.
    """

    sender_id: Optional[str] = None
    """
    The device ID to send notifications from
    (`device_iden` in the device's URL on [pushbullet.com](https://pushbullet.com)).

    Leave unset, blank or set to `null` to send from yourself.
    """

    _implementation: str = "PushBullet"
    _remote_map: List[RemoteMapEntry] = [
        ("api_key", "apiKey", {"is_field": True}),
        ("device_ids", "deviceIds", {"is_field": True, "encoder": lambda v: sorted(v)}),
        ("channel_tags", "channelTags", {"is_field": True, "encoder": lambda v: sorted(v)}),
        (
            "sender_id",
            "senderId",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
    ]
