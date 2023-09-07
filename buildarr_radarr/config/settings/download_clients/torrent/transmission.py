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
Transmission download client configuration.
"""


from __future__ import annotations

from typing import Any, List, Literal, Mapping, Optional

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr, Password, Port
from pydantic import validator

from .base import TorrentDownloadClient


class TransmissionPriority(BaseEnum):
    last = 0
    first = 1


class TransmissionDownloadClientBase(TorrentDownloadClient):
    # Configuration options common to both Transmission and Vuze download clients.

    hostname: NonEmptyStr
    """
    Download client host name.
    """

    port: Port = 9091  # type: ignore[assignment]
    """
    Download client access port.
    """

    use_ssl: bool = False
    """
    Use a secure connection when connecting to the download client.
    """

    url_base: NonEmptyStr = "/transmission/"  # type: ignore[assignment]
    """
    Adds a prefix to the API RPC url, e.g.`http://[host]:[port][url_base]rpc`.

    This is set by default in most clients to `/transmission/`.
    """

    username: Optional[str] = None
    """
    User name to use when authenticating with the download client, if required.
    """

    password: Optional[Password] = None
    """
    Password to use to authenticate the download client user, if required.
    """

    category: Optional[str] = None
    """
    Associate media from Radarr with a category.
    Creates a `[category]` subdirectory in the output directory.

    Adding a category specific to Radarr avoids conflicts with unrelated non-Radarr downloads.
    Using a category is optional, but strongly recommended.
    """

    directory: Optional[str] = None
    """
    Optional shared folder to put downloads into.

    Leave blank, set to `null` or undefined to use the default download client location.
    """

    recent_priority: TransmissionPriority = TransmissionPriority.last
    """
    Priority to use when grabbing media that released within the last 21 days.

    Values:

    * `last`
    * `first`
    """

    older_priority: TransmissionPriority = TransmissionPriority.last
    """
    Priority to use when grabbing media that released over 21 days ago.

    Values:

    * `last`
    * `first`
    """

    add_paused: bool = False
    """
    Add media to the download client in the Paused state.
    """

    _remote_map: List[RemoteMapEntry] = [
        ("hostname", "host", {"is_field": True}),
        ("port", "port", {"is_field": True}),
        ("use_ssl", "useSsl", {"is_field": True}),
        ("url_base", "urlBase", {"is_field": True}),
        (
            "username",
            "username",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        ("password", "password", {"is_field": True, "field_default": None}),
        (
            "category",
            "movieCategory",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        (
            "directory",
            "movieDirectory",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        ("recent_priority", "recentMoviePriority", {"is_field": True}),
        ("older_priority", "olderMoviePriority", {"is_field": True}),
        ("add_paused", "addPaused", {"is_field": True}),
    ]

    @validator("directory")
    def category_directory_mutual_exclusion(
        cls,
        value: Optional[str],
        values: Mapping[str, Any],
    ) -> Optional[str]:
        directory = value
        category: Optional[str] = values.get("category", None)
        if directory and category:
            raise ValueError(
                "'directory' and 'category' are mutually exclusive "
                "on a Transmission/Vuze download client",
            )
        return directory


class TransmissionDownloadClient(TransmissionDownloadClientBase):
    # Transmission download client.

    type: Literal["transmission"] = "transmission"
    """
    Type value associated with this kind of download client.
    """

    _implementation: str = "Transmission"
