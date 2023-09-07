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
Aria2 download client configuration.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr, Password, Port

from .base import TorrentDownloadClient


class Aria2DownloadClient(TorrentDownloadClient):
    # Aria2 download client.

    type: Literal["aria2"] = "aria2"
    """
    Type value associated with this kind of download client.
    """

    hostname: NonEmptyStr
    """
    Aria2 host name.
    """

    port: Port = 6800  # type: ignore[assignment]
    """
    Download client access port.
    """

    use_ssl: bool = False
    """
    Use a secure connection when connecting to the download client.
    """

    rpc_path: NonEmptyStr = "/rpc"  # type: ignore[assignment]
    """
    XML RPC path in the Aria2 client URL.
    """

    secret_token: Password
    """
    Secret token to use to authenticate with the download client.
    """

    _implementation: str = "Aria2"
    _remote_map: List[RemoteMapEntry] = [
        ("hostname", "host", {"is_field": True}),
        ("port", "port", {"is_field": True}),
        ("use_ssl", "useSsl", {"is_field": True}),
        ("rpc_path", "rpcPath", {"is_field": True}),
        ("secret_token", "secretToken", {"is_field": True}),
    ]
