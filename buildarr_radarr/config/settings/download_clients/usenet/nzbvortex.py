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
NZBVortex download client configuration.
"""


from __future__ import annotations

from typing import List, Literal, Optional

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr, Password, Port

from .base import UsenetDownloadClient


class NzbvortexPriority(BaseEnum):
    low = -1
    normal = 0
    high = 1


class NzbvortexDownloadClient(UsenetDownloadClient):
    # NZBVortex download client.

    type: Literal["nzbvortex"] = "nzbvortex"
    """
    Type value associated with this kind of download client.
    """

    hostname: NonEmptyStr
    """
    NZBVortex host name.
    """

    port: Port = 4321  # type: ignore[assignment]
    """
    Download client access port.
    """

    url_base: Optional[str] = None
    """
    Adds a prefix to the NZBVortex url, e.g. `http://[host]:[port]/[url_base]/api`.
    """

    api_key: Password
    """
    API key to use to authenticate with the download client.
    """

    category: Optional[str] = None
    """
    Associate media from Radarr with a category.

    Adding a category specific to Radarr avoids conflicts with unrelated non-Radarr downloads.
    Using a category is optional, but strongly recommended.
    """

    recent_priority: NzbvortexPriority = NzbvortexPriority.normal
    """
    Priority to use when grabbing media that released within the last 21 days.

    Values:

    * `low`
    * `normal`
    * `high`
    """

    older_priority: NzbvortexPriority = NzbvortexPriority.normal
    """
    Priority to use when grabbing media that released over 21 days ago.

    Values:

    * `low`
    * `normal`
    * `high`
    """

    _implementation: str = "NzbVortex"
    _remote_map: List[RemoteMapEntry] = [
        ("hostname", "host", {"is_field": True}),
        ("port", "port", {"is_field": True}),
        (
            "url_base",
            "urlBase",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        ("api_key", "apiKey", {"is_field": True}),
        (
            "category",
            "tvCategory",  # Yes, it is supposed to be `tvCategory`.
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        ("recent_priority", "recentMoviePriority", {"is_field": True}),
        ("older_priority", "olderMoviePriority", {"is_field": True}),
    ]
