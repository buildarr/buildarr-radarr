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
Slack notification connection configuration.
"""


from __future__ import annotations

from typing import List, Literal, Optional

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr
from pydantic import AnyHttpUrl

from .base import Notification


class SlackNotification(Notification):
    """
    Send media update and health alert messages to a Slack channel.
    """

    type: Literal["slack"] = "slack"
    """
    Type value associated with this kind of connection.
    """

    webhook_url: AnyHttpUrl
    """
    Webhook URL for the Slack channel to send to.
    """

    username: NonEmptyStr
    """
    Username to post as.
    """

    icon: Optional[str] = None
    """
    The icon that is used for messages from this integration (emoji or URL).

    If unset, blank or set to `None`, use the default for the user.
    """

    channel: Optional[str] = None
    """
    If set, overrides the default channel in the webhook.
    """

    _implementation: str = "Slack"
    _remote_map: List[RemoteMapEntry] = [
        ("webhook_url", "webHookUrl", {"is_field": True}),
        ("username", "username", {"is_field": True}),
        (
            "icon",
            "icon",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        (
            "channel",
            "channel",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
    ]
