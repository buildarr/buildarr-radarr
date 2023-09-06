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
ntfy notification connection configuration.
"""


from __future__ import annotations

from typing import List, Literal, Optional, Set

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr
from pydantic import AnyHttpUrl, SecretStr

from .base import Notification


class NtfyPriority(BaseEnum):
    min = 1
    low = 2
    default = 3
    high = 4
    max = 5


class NtfyNotification(Notification):
    """
    Send media update and health alert emails via the ntfy.sh notification service,
    or a self-hosted server using the same software.
    """

    type: Literal["ntfy"] = "ntfy"
    """
    Type value associated with this kind of connection.
    """

    base_url: Optional[AnyHttpUrl] = None
    """
    Custom ntfy server URL.

    Leave blank, set to `null` or undefined to use the public server (`https://ntfy.sh`).
    """

    access_token: Optional[SecretStr] = None
    """
    Optional token-based authorisation.

    When both are defined, access token takes priority over username/password.
    """

    username: Optional[str] = None
    """
    Username to use to authenticate, if required.
    """

    password: Optional[SecretStr] = None
    """
    Password to use to authenticate, if required.
    """

    priority: NtfyPriority = NtfyPriority.default
    """
    Values:

    * `min`
    * `low`
    * `default`
    * `high`
    * `max`
    """

    topics: Set[NonEmptyStr] = set()
    """
    List of Topics to send notifications to.
    """

    ntfy_tags: Set[NonEmptyStr] = set()
    """
    Optional list of tags or [emojis](https://ntfy.sh/docs/emojis) to use.
    """

    click_url: Optional[AnyHttpUrl] = None
    """
    Optional link for when the user clicks the notification.
    """

    _implementation: str = "Ntfy"
    _remote_map: List[RemoteMapEntry] = [
        (
            "server_url",
            "serverUrl",
            {
                "is_field": True,
                "decoder": lambda v: v or None,
                "encoder": lambda v: str(v) if v else "",
            },
        ),
        (
            "access_token",
            "accessToken",
            {
                "is_field": True,
                "decoder": lambda v: SecretStr(v) if v else None,
                "encoder": lambda v: v.get_secret_value() if v else "",
            },
        ),
        (
            "username",
            "userName",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        (
            "password",
            "password",
            {
                "is_field": True,
                "decoder": lambda v: SecretStr(v) if v else None,
                "encoder": lambda v: v.get_secret_value() if v else "",
            },
        ),
        ("priority", "priority", {"is_field": True}),
        ("topics", "topics", {"is_field": True, "encoder": sorted}),
        ("ntfy_tags", "tags", {"is_field": True, "encoder": sorted}),
        (
            "click_url",
            "clickUrl",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
    ]
