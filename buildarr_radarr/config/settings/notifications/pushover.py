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
Pushover notification connection configuration.
"""


from __future__ import annotations

from typing import Any, List, Literal, Mapping, Optional, Set, Union

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr, Password
from pydantic import ConstrainedInt, Field, SecretStr, validator

from .base import Notification


class PushoverApiKey(SecretStr):
    min_length = 30
    max_length = 30


class PushoverPriority(BaseEnum):
    silent = -2
    quiet = -1
    normal = 0
    high = 1
    emergency = 2


class PushoverRetry(ConstrainedInt):
    ge = 30


class PushoverNotification(Notification):
    """
    Send media update and health alert push notifications to Pushover devices.
    """

    type: Literal["pushover"] = "pushover"
    """
    Type value associated with this kind of connection.
    """

    user_key: PushoverApiKey
    """
    User key to use to authenticate with your Pushover account.
    """

    api_key: Password
    """
    API key assigned to this application in Pushover.
    """

    devices: Set[NonEmptyStr] = set()
    """
    List of device names to send notifications to.

    If unset or empty, send to all devices.
    """

    priority: PushoverPriority = PushoverPriority.normal
    """
    Pushover push notification priority.

    Values:

    * `silent`
    * `quiet`
    * `normal`
    * `high`
    * `emergency`
    """

    retry: Union[Literal[0], PushoverRetry] = 0
    """
    Interval to retry emergency alerts, in seconds.

    Minimum 30 seconds. Set to 0 to disable retrying emergency alerts.
    """

    expire: int = Field(0, ge=0, le=86400)
    """
    Threshold for retrying emergency alerts, in seconds.
    If `retry` is set, this should be set to a higher value.

    Maximum 86400 seconds (1 day).
    """

    sound: Optional[str] = None
    """
    Notification sound to use on devices.

    Leave unset, blank or set to `null` to use the default.
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

    _implementation: str = "Pushover"
    _remote_map: List[RemoteMapEntry] = [
        ("user_key", "userKey", {"is_field": True}),
        ("api_key", "apiKey", {"is_field": True}),
        ("devices", "devices", {"is_field": True, "encoder": lambda v: sorted(v)}),
        ("priority", "priority", {"is_field": True}),
        ("retry", "retry", {"is_field": True}),
        ("expire", "expire", {"is_field": True}),
        (
            "sound",
            "sound",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
    ]
