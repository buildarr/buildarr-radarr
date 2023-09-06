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
Emby / Jellyfin notification connection configuration.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr, Password, Port

from .base import Notification


class EmbyJellyfinNotification(Notification):
    """
    Send media update and health alert push notifications to an Emby or Jellyfin media server.
    """

    type: Literal[
        "emby",
        "jellyfin",
        "emby-jellyfin",
        "emby_jellyfin",
        "embyjellyfin",
    ] = "emby-jellyfin"
    """
    Type values associated with this kind of connection.

    It is recommended to use the value representing the actual instance you are using,
    e.g. for Emby use `emby`, for Jellyfin use `jellyfin`.
    """

    hostname: NonEmptyStr
    """
    Emby / Jellyfin server hostname.
    """

    port: Port = 8096  # type: ignore[assignment]
    """
    Emby / Jellyfin server access port.
    """

    use_ssl: bool = False
    """
    Connect to the server using HTTPS.
    """

    api_key: Password
    """
    API key for authenticating with Emby / Jellyfin.
    """

    send_notifications: bool = False
    """
    Have the server send notifications to configured providers.
    """

    update_library: bool = False
    """
    When set to `true`, update the Emby / Jellyfin libraries on import, rename or delete.
    """

    _implementation: str = "MediaBrowser"
    _remote_map: List[RemoteMapEntry] = [
        ("hostname", "host", {"is_field": True}),
        ("port", "port", {"is_field": True}),
        ("use_ssl", "useSsl", {"is_field": True}),
        ("api_key", "apiKey", {"is_field": True}),
        ("send_notifications", "notify", {"is_field": True}),
        ("update_library", "updateLibrary", {"is_field": True}),
    ]
