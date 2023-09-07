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
Flood download client configuration.
"""


from __future__ import annotations

from typing import List, Literal, Optional, Set

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr, Password, Port

from .base import TorrentDownloadClient


class FloodMediaTag(BaseEnum):
    collection = 0
    quality = 1
    languages = 2
    release_group = 3
    year = 4
    indexer = 5
    studio = 6


class FloodDownloadClient(TorrentDownloadClient):
    """
    Flood download client.
    """

    type: Literal["flood"] = "flood"
    """
    Type value associated with this kind of download client.
    """

    hostname: NonEmptyStr
    """
    Flood host name.
    """

    port: Port = 3000  # type: ignore[assignment]
    """
    Download client access port.
    """

    use_ssl: bool = False
    """
    Use a secure connection when connecting to the download client.
    """

    url_base: Optional[str] = None
    """
    Optionally adds a prefix to Flood API, such as `[protocol]://[host]:[port]/[url_base]api`.
    """

    username: NonEmptyStr
    """
    User name to use when authenticating with the download client.
    """

    password: Password
    """
    Password to use to authenticate the download client user.
    """

    destination: Optional[str] = None
    """
    Manually specified download destination.
    """

    flood_tags: Set[NonEmptyStr] = {"radarr"}  # type: ignore[arg-type]
    """
    Initial tags of a download within Flood.

    To be recognized, a download must have all initial tags.
    This avoids conflicts with unrelated downloads.
    """

    additional_tags: Set[FloodMediaTag] = set()
    """
    Adds properties of media as tags within Flood.

    Multiple can be specified at a time.

    Values:

    * `collection`
    * `quality`
    * `languages`
    * `release-group`
    * `year`
    * `indexer`
    * `studio`
    """

    add_paused: bool = False
    """
    Add media to the download client in the Paused state.
    """

    _implementation: str = "Flood"
    _remote_map: List[RemoteMapEntry] = [
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
            "destination",
            "destination",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        ("flood_tags", "tags", {"is_field": True, "encoder": sorted}),
        (
            "additional_tags",
            "additionalTags",
            {
                "is_field": True,
                "decoder": lambda v: set(FloodMediaTag(t) for t in v),
                "encoder": lambda v: sorted(t.value for t in v),
            },
        ),
        ("add_paused", "addPaused", {"is_field": True}),
    ]
