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
SendGrid notification connection configuration.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry
from buildarr.types import Password
from pydantic import Field, NameEmail
from typing_extensions import Annotated

from .base import Notification


class SendgridNotification(Notification):
    """
    Send media update and health alert emails via the SendGrid delivery service.
    """

    type: Literal["sendgrid"] = "sendgrid"
    """
    Type value associated with this kind of connection.
    """

    api_key: Password
    """
    API key to use to authenticate with SendGrid.
    """

    from_address: NameEmail
    """
    Email address to send the mail as.

    RFC-5322 formatted mailbox addresses are also supported,
    e.g. `Radarr <radarr@example.com>`.
    """

    recipient_addresses: Annotated[List[NameEmail], Field(min_items=1, unique_items=True)]
    """
    The recipient email addresses of the notification mail.

    At least one recipient address is required.
    """

    _implementation: str = "SendGrid"
    _remote_map: List[RemoteMapEntry] = [
        ("api_key", "apiKey", {"is_field": True}),
        ("from_address", "from", {"is_field": True}),
        ("recipient_addresses", "recipients", {"is_field": True}),
    ]
