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
Email notification connection configuration.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr, Password, Port
from pydantic import Field, NameEmail
from typing_extensions import Annotated

from .base import Notification


class EmailNotification(Notification):
    """
    Send media update and health alert messages to an email address.
    """

    type: Literal["email"] = "email"
    """
    Type value associated with this kind of connection.
    """

    server: NonEmptyStr
    """
    Hostname or IP address of the SMTP server to send outbound mail to.
    """

    port: Port = 587  # type: ignore[assignment]
    """
    The port number on the SMTP server to use to submit mail.

    The default is to use STARTTLS on the standard SMTP submission port.
    """

    use_encryption: bool = False
    """
    Whether or not to use encryption when sending mail to the SMTP server.

    If the port number is set to 465, SMTPS (implicit TLS) will be used.
    Any other port number will result in STARTTLS being used.

    The default is to not require encryption.
    """

    username: NonEmptyStr
    """
    SMTP username of the account to send the mail from.
    """

    password: Password
    """
    SMTP password of the account to send the mail from.
    """

    from_address: NameEmail
    """
    Email address to send the mail as.

    RFC-5322 formatted mailbox addresses are also supported,
    e.g. `Radarr <radarr@example.com>`.
    """

    recipient_addresses: Annotated[List[NameEmail], Field(min_items=1, unique_items=True)]
    """
    List of email addresses to directly address the mail to.

    At least one address must be provided.
    """

    cc_addresses: Annotated[List[NameEmail], Field(unique_items=True)] = []
    """
    Optional list of email addresses to copy (CC) the mail to.
    """

    bcc_addresses: Annotated[List[NameEmail], Field(unique_items=True)] = []
    """
    Optional list of email addresses to blind copy (BCC) the mail to.
    """

    _implementation: str = "Email"
    _remote_map: List[RemoteMapEntry] = [
        ("server", "server", {"is_field": True}),
        ("port", "port", {"is_field": True}),
        ("use_encryption", "requireEncryption", {"is_field": True}),
        ("username", "username", {"is_field": True}),
        ("password", "password", {"is_field": True}),
        ("from_address", "from", {"is_field": True}),
        ("recipient_addresses", "to", {"is_field": True}),
        ("cc_addresses", "cc", {"is_field": True}),
        ("bcc_addresses", "bcc", {"is_field": True}),
    ]
