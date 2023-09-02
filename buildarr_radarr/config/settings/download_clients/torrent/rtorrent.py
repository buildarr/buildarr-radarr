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
Radarr plugin torrent download client definitions.
"""


from __future__ import annotations

from typing import List, Literal, Optional

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr, Password, Port

from .base import TorrentDownloadClient


class RtorrentPriority(BaseEnum):
    """
    RTorrent media priority.

    Values:

    * `verylow` (Very Low)
    * `low` (Low)
    * `normal` (Normal)
    * `high` (High)
    """

    verylow = 0
    low = 1
    normal = 2
    high = 3


class RtorrentDownloadClient(TorrentDownloadClient):
    """
    RTorrent (ruTorrent) download client.
    """

    type: Literal["rtorrent", "rutorrent"] = "rtorrent"
    """
    Type value associated with this kind of download client.
    """

    host: NonEmptyStr
    """
    RTorrent host name.
    """

    port: Port = 8080  # type: ignore[assignment]
    """
    Download client access port.
    """

    use_ssl: bool = False
    """
    Use a secure connection when connecting to the download client.
    """

    url_base: NonEmptyStr = "RPC2"  # type: ignore[assignment]
    """
    Path to the XMLRPC endpoint, e.g. `http(s)://[host]:[port]/[url_base]`.

    When using RTorrent this usually is `RPC2` or `plugins/rpc/rpc.php`.
    """

    username: NonEmptyStr
    """
    User name to use when authenticating with the download client.
    """

    password: Password
    """
    Password to use to authenticate the download client user.
    """

    category: Optional[str] = "radarr"
    """
    Associate media from Radarr with a category.

    Adding a category specific to Radarr avoids conflicts with unrelated non-Radarr downloads.
    Using a category is optional, but strongly recommended.
    """

    directory: Optional[str] = None
    """
    Optional shared folder to put downloads into.

    Leave blank, set to `null` or undefined to use the default download client location.
    """

    client_priority: RtorrentPriority = RtorrentPriority.normal
    """
    Priority to use when grabbing releases.

    Values:

    * `verylow`
    * `low`
    * `normal`
    * `high`
    """

    add_stopped: bool = False
    """
    Enabling will add torrents and magnets to RTorrent in a stopped state.

    This may break magnet files.
    """

    _implementation: str = "RTorrent"
    _base_remote_map: List[RemoteMapEntry] = [
        ("host", "host", {"is_field": True}),
        ("port", "port", {"is_field": True}),
        ("use_ssl", "useSsl", {"is_field": True}),
        ("url_base", "urlBase", {"is_field": True}),
        ("username", "username", {"is_field": True}),
        ("password", "password", {"is_field": True}),
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
        ("client_priority", "recentMoviePriority", {"is_field": True}),
        ("add_stopped", "addStopped", {"is_field": True}),
    ]
