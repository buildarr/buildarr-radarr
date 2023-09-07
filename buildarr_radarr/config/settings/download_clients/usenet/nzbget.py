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
NZBGet download client configuration.
"""


from __future__ import annotations

from logging import getLogger
from typing import List, Literal, Optional

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr, Password, Port

from .base import UsenetDownloadClient

logger = getLogger(__name__)


class NzbgetPriority(BaseEnum):
    verylow = -100
    low = -50
    normal = 0
    high = 50
    veryhigh = 100
    force = 900


class NzbgetDownloadClient(UsenetDownloadClient):
    # NZBGet download client.

    type: Literal["nzbget"] = "nzbget"
    """
    Type value associated with this kind of download client.
    """

    hostname: NonEmptyStr
    """
    NZBGet host name.
    """

    port: Port = 5000  # type: ignore[assignment]
    """
    Download client access port.
    """

    use_ssl: bool = False
    """
    Use a secure connection when connecting to the download client.
    """

    url_base: Optional[str] = None
    """
    Adds a prefix to the NZBGet url, e.g. `http://[host]:[port]/[url_base]/jsonrpc`.
    """

    username: NonEmptyStr
    """
    User name to use when authenticating with the download client.
    """

    password: Password
    """
    Password to use to authenticate the download client user.
    """

    category: Optional[str] = None
    """
    Associate media from Radarr with a category.

    Adding a category specific to Radarr avoids conflicts with unrelated non-Radarr downloads.
    Using a category is optional, but strongly recommended.
    """

    recent_priority: NzbgetPriority = NzbgetPriority.normal
    """
    Priority to use when grabbing media that released within the last 21 days.

    Values:

    * `verylow`
    * `low`
    * `normal`
    * `high`
    * `veryhigh`
    * `force`
    """

    older_priority: NzbgetPriority = NzbgetPriority.normal
    """
    Priority to use when grabbing media that released over 21 days ago.

    Values:

    * `verylow`
    * `low`
    * `normal`
    * `high`
    * `veryhigh`
    * `force`
    """

    add_paused: bool = False
    """
    Add media to the download client in the paused state.

    This option requires NZBGet version 16.0 or later.
    """

    _implementation: str = "Nzbget"
    _base_remote_map: List[RemoteMapEntry] = [
        ("hostname", "host", {"is_field": True}),
        ("port", "port", {"is_field": True}),
        ("use_ssl", "useSsl", {"is_field": True}),
        (
            "url_base",
            "urlBase",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        ("username", "username", {"is_field": True}),
        ("password", "password", {"is_field": True}),
        (
            "category",
            "movieCategory",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        ("recent_priority", "recentMoviePriority", {"is_field": True}),
        ("older_priority", "olderMoviePriority", {"is_field": True}),
        ("add_paused", "addPaused", {"is_field": True}),
    ]
