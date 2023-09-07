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
Pushsafer notification connection configuration.
"""


from __future__ import annotations

from typing import Any, List, Literal, Mapping, Optional, Set, Union

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr, Password
from pydantic import ConstrainedInt, Field, validator
from pydantic.color import Color

from .base import Notification


class PushsaferPriority(BaseEnum):
    silent = -2
    quiet = -1
    normal = 0
    high = 1
    emergency = 2


class PushsaferRetry(ConstrainedInt):
    ge = 60


class PushsaferNotification(Notification):
    """
    Send media update and health alert push notifications to Pushsafer devices.
    """

    type: Literal["pushsafer"] = "pushsafer"
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

    priority: PushsaferPriority = PushsaferPriority.normal
    """
    Pushsafer push notification priority.

    Values:

    * `silent`
    * `quiet`
    * `normal`
    * `high`
    * `emergency`
    """

    retry: Union[Literal[0], PushsaferRetry] = 0
    """
    Interval to retry emergency alerts, in seconds.

    Minimum 60 seconds. Set to 0 to disable retrying emergency alerts.
    """

    expire: int = Field(0, ge=0, le=10800)
    """
    Threshold for retrying emergency alerts, in seconds.
    If `retry` is set, this should be set to a higher value.

    Maximum 10800 seconds (3 hours).
    """

    sound: Optional[int] = None
    """
    Notification sound number (0-62) to use when alerting.

    Leave unset, blank or set to `null` to use the default.
    """

    vibration: Optional[int] = None
    """
    Notification pattern (1-3) to use on devices.

    Leave unset, blank or set to `null` to use the device default.
    """

    icon: Optional[int] = None
    """
    Pushsafer icon number (1-181) to use in notifications.

    Leave unset, blank or set to `null` to use the default Pushsafer icon.
    """

    icon_color: Optional[Color] = None
    """
    The colour to use for the Pushsafer icon in the notification.

    Specify either a colour (e.g. `yellow`) or a hex code (`#00FF00`).
    """

    @validator("expire")
    def validate_expire(cls, value: int, values: Mapping[str, Any]) -> int:
        try:
            retry = values["retry"]
        except KeyError:
            return value
        if retry and value < retry:
            raise ValueError(
                f"'expire' ({value}) is shorter than 'retry' ({retry})",
            )
        return value

    _implementation: str = "Pushsafer"
    _remote_map: List[RemoteMapEntry] = [
        ("api_key", "apiKey", {"is_field": True}),
        ("device_ids", "deviceIds", {"is_field": True, "encoder": lambda v: sorted(v)}),
        ("priority", "priority", {"is_field": True}),
        ("retry", "retry", {"is_field": True}),
        ("expire", "expire", {"is_field": True}),
        ("sound", "sound", {"is_field": True}),
        ("vibration", "vibration", {"is_field": True}),
        ("icon", "icon", {"is_field": True}),
        (
            "icon_color",
            "iconColor",
            {
                "is_field": True,
                "decoder": lambda v: v or None,
                "encoder": lambda v: (
                    ("#" + "".join(f"{i:02x}".upper() for i in v.as_rgb_tuple())) if v else ""
                ),
            },
        ),
    ]
