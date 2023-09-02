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
Apprise notification connection configuration.
"""


from __future__ import annotations

from typing import List, Literal, Optional, Set

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr
from pydantic import AnyHttpUrl, SecretStr

from .base import Notification


class AppriseNotification(Notification):
    """
    Receive media update and health alert push notifications via an Apprise server.
    """

    type: Literal["apprise"] = "apprise"
    """
    Type value associated with this kind of connection.
    """

    base_url: AnyHttpUrl
    """
    Apprise server base URL, including `http[s]://` and port if needed.
    """

    configuration_key: Optional[SecretStr] = None
    """
    Configuration key for the Persistent Storage Solution.

    Leave empty if Stateless URLs are used.
    """

    stateless_urls: Set[AnyHttpUrl] = set()
    """
    One or more URLs where notifications should be sent to.

    Leave undefined or empty if Persistent Storage is used.
    """

    apprise_tags: Set[NonEmptyStr] = set()
    """
    Optionally notify only targets with the defined tags.
    """

    auth_username: Optional[str] = None
    """
    Username for authenticating with Apprise, if required.
    """

    auth_password: Optional[SecretStr] = None
    """
    Password for authenticating with Apprise, if required.
    """

    _implementation: str = "Apprise"
    _remote_map: List[RemoteMapEntry] = [
        ("base_url", "baseUrl", {"is_field": True}),
        (
            "configuration_key",
            "configurationKey",
            {
                "is_field": True,
                "decoder": lambda v: SecretStr(v) if v else None,
                "encoder": lambda v: v.get_secret_value() if v else "",
            },
        ),
        (
            "stateless_urls",
            "statelessUrls",
            {
                "is_field": True,
                "decoder": lambda v: set(url.strip() for url in "".split(",") if url.strip()),
                "encoder": lambda v: ",".join(sorted(str(url) for url in v)),
            },
        ),
        (
            "apprise_tags",
            "tags",
            {"is_field": True, "encoder": lambda v: sorted(v)},
        ),
        (
            "auth_username",
            "authUsername",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        (
            "auth_password",
            "authPassword",
            {
                "is_field": True,
                "decoder": lambda v: SecretStr(v) if v else None,
                "encoder": lambda v: v.get_secret_value() if v else "",
            },
        ),
    ]
