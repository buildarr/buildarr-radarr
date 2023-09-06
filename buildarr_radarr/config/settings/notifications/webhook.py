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
Webhook notification connection configuration.
"""


from __future__ import annotations

from typing import List, Literal, Optional

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum
from pydantic import AnyHttpUrl, SecretStr

from .base import Notification


class WebhookMethod(BaseEnum):
    """
    HTTP method to use on a webhook connection.
    """

    POST = 1
    PUT = 2


class WebhookNotification(Notification):
    """
    Send media update and health alert notifications to a webhook API.
    """

    type: Literal["webhook"] = "webhook"
    """
    Type value associated with this kind of connection.
    """

    url: AnyHttpUrl
    """
    Webhook URL to send notifications to.
    """

    method: WebhookMethod = WebhookMethod.POST
    """
    HTTP request method type to use.

    Values:

    * `POST`
    * `PUT`
    """

    username: Optional[str] = None
    """
    Webhook API username, if required.
    """

    password: Optional[SecretStr] = None
    """
    Webhook API password, if required.
    """

    _implementation: str = "Webhook"
    _remote_map: List[RemoteMapEntry] = [
        ("url", "url", {"is_field": True}),
        ("method", "method", {"is_field": True}),
        (
            "username",
            "username",
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
    ]
