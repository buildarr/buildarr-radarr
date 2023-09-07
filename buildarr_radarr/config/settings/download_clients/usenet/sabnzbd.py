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
SABnzbd download client configuration.
"""


from __future__ import annotations

from typing import List, Literal, Optional

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr, Port
from pydantic import SecretStr

from .base import UsenetDownloadClient


class SabnzbdPriority(BaseEnum):
    default = -100
    paused = -2
    low = -1
    normal = 0
    high = 1
    force = 2


class SabnzbdDownloadClient(UsenetDownloadClient):
    # SABnzbd download client.

    type: Literal["sabnzbd"] = "sabnzbd"
    """
    Type value associated with this kind of download client.
    """

    hostname: NonEmptyStr
    """
    SABnzbd host name.
    """

    port: Port = 4321  # type: ignore[assignment]
    """
    Download client access port.
    """

    use_ssl: bool = False
    """
    Use a secure connection when connecting to the download client.
    """

    url_base: Optional[str] = None
    """
    Adds a prefix to the SABnzbd URL, e.g. `http://[host]:[port]/[url_base]/api/`.
    """

    api_key: Optional[SecretStr] = None
    """
    API key to use to authenticate with SABnzbd, if required.
    """

    username: Optional[str] = None
    """
    User name to use when authenticating with SABnzbd, if required.
    """

    password: Optional[SecretStr] = None
    """
    Password to use to authenticate with SABnzbd, if required.
    """

    category: Optional[str] = None
    """
    Associate media from Radarr with a category.

    Adding a category specific to Radarr avoids conflicts with unrelated non-Radarr downloads.
    Using a category is optional, but strongly recommended.
    """

    recent_priority: SabnzbdPriority = SabnzbdPriority.default
    """
    Priority to use when grabbing media that releases within the last 21 days.

    Values:

    * `default`
    * `paused`
    * `low`
    * `normal`
    * `high`
    * `force`
    """

    older_priority: SabnzbdPriority = SabnzbdPriority.default
    """
    Priority to use when grabbing media that releases over 21 days ago.

    Values:

    * `default`
    * `paused`
    * `low`
    * `normal`
    * `high`
    * `force`
    """

    _implementation: str = "Sabnzbd"
    _base_remote_map: List[RemoteMapEntry] = [
        ("hostname", "host", {"is_field": True}),
        ("port", "port", {"is_field": True}),
        ("use_ssl", "useSsl", {"is_field": True}),
        (
            "url_base",
            "urlBase",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        (
            "api_key",
            "apiKey",
            {
                "is_field": True,
                "decoder": lambda v: v or None,
                "encoder": lambda v: v.get_secret_value() if v else "",
            },
        ),
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
                "decoder": lambda v: v or None,
                "encoder": lambda v: v.get_secret_value() if v else "",
            },
        ),
        (
            "category",
            "movieCategory",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        ("recent_priority", "recentMoviePriority", {"is_field": True}),
        ("older_priority", "olderMoviePriority", {"is_field": True}),
    ]
