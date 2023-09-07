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
Freebox download client configuration.
"""


from __future__ import annotations

from typing import List, Literal, Optional

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr, Password, Port

from .base import TorrentDownloadClient


class FreeboxPriority(BaseEnum):
    last = 0
    first = 1


class FreeboxDownloadClient(TorrentDownloadClient):
    # Download client for connecting to a Freebox instance.

    type: Literal["freebox"] = "freebox"
    """
    Type value associated with this kind of download client.
    """

    hostname: NonEmptyStr = "mafreebox.freebox.fr"  # type: ignore[assignment]
    """
    Hostname or host IP address of the Freebox.

    The default of `mafreebox.freebox.fr` will only work if on the same network.
    """

    port: Port = 443  # type: ignore[assignment]
    """
    Freebox access port.

    Set to the HTTPS default port as Freebox uses HTTPS by default.
    """

    use_ssl: bool = True
    """
    Use a secure connection when connecting to the Freebox API.
    """

    api_url: NonEmptyStr = "/api/v1"  # type: ignore[assignment]
    """
    Define Freebox API base URL with API version, e.g. `http[s]://<host>:<port>/<api_url>/`.
    """

    app_id: NonEmptyStr
    """
    App ID used to authenticate with the Freebox.
    """

    app_token: Password
    """
    Unique token used to authenticate with the Freebox.
    """

    destination_directory: Optional[str] = None
    """
    Optional location to put downloads in, on the Freebox node.

    Leave blank, undefined or set to `null` to use the default Freebox download location.
    """

    category: Optional[str] = None
    """
    Default category to classify downloads under if no category mappings apply to it.

    This will create a `[category]` subdirectory in the output directory.
    Adding a category specific to Radarr avoids conflicts with unrelated non-Radarr downloads.
    """

    recent_priority: FreeboxPriority = FreeboxPriority.last
    """
    Priority to use when grabbing media that released within the last 14 days.
    """

    older_priority: FreeboxPriority = FreeboxPriority.last
    """
    Priority to use when grabbing media that released over 14 days ago.
    """

    add_paused: bool = False
    """
    Add media to the download client in the Paused state.
    """

    _implementation: str = "TorrentFreeboxDownload"
    _base_remote_map: List[RemoteMapEntry] = [
        ("hostname", "host", {"is_field": True}),
        ("port", "port", {"is_field": True}),
        ("use_ssl", "useSsl", {"is_field": True}),
        ("api_url", "apiUrl", {"is_field": True}),
        ("app_id", "appId", {"is_field": True}),
        ("app_token", "appToken", {"is_field": True}),
        (
            "destination_directory",
            "destinationDirectory",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        (
            "category",
            "category",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        ("recent_priority", "recentPriority", {"is_field": True}),
        ("older_priority", "olderPriority", {"is_field": True}),
        ("add_paused", "addPaused", {"is_field": True}),
    ]
