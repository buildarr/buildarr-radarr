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
Kodi notification connection configuration.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr, Password, Port

from .base import Notification


class KodiNotification(Notification):
    """
    Send media update and health alert push notifications to a Kodi (XBMC) media server.
    """

    type: Literal["kodi", "xbmc"] = "kodi"
    """
    Type values associated with this kind of connection.
    """

    hostname: NonEmptyStr
    """
    Kodi server hostname.
    """

    port: Port = 8080  # type: ignore[assignment]
    """
    Kodi server access port.
    """

    use_ssl: bool = False
    """
    Connect to the server using HTTPS.
    """

    username: NonEmptyStr
    """
    Kodi administrator username.
    """

    password: Password
    """
    Kodi user password.
    """

    display_notification: bool = False
    """
    Display the notification in the Kodi GUI.
    """

    display_time: int = 5
    """
    Display time of the notification (in seconds).
    """

    clean_library: bool = False
    """
    When set to `true`, clean the library update.
    """

    always_update: bool = False
    """
    Always update the library, even when a video is playing.
    """

    _implementation: str = "Xbmc"
    _remote_map: List[RemoteMapEntry] = [
        ("hostname", "host", {"is_field": True}),
        ("port", "port", {"is_field": True}),
        ("use_ssl", "useSsl", {"is_field": True}),
        ("username", "username", {"is_field": True}),
        ("password", "password", {"is_field": True}),
        ("display_notification", "notify", {"is_field": True}),
        ("display_time", "displayTime", {"is_field": True}),
        ("update_library", "updateLibrary", {"is_field": True}),
        ("always_update", "alwaysUpdate", {"is_field": True}),
    ]
