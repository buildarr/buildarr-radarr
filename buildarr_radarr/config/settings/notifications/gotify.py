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
Gotify notification connection configuration.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, Password
from pydantic import AnyHttpUrl

from .base import Notification


class GotifyPriority(BaseEnum):
    """
    Gotify notification priority.
    """

    min = 0
    low = 2
    normal = 5
    high = 8


class GotifyNotification(Notification):
    """
    Send media update and health alert push notifications through a Gotify server.
    """

    type: Literal["gotify"] = "gotify"
    """
    Type value associated with this kind of connection.
    """

    base_url: AnyHttpUrl
    """
    Gotify server URL. (e.g. `http://gotify.example.com:1234`)
    """

    app_token: Password
    """
    App token to use to authenticate with Gotify.
    """

    priority: GotifyPriority = GotifyPriority.normal
    """
    Gotify notification priority.

    Values:

    * `min`
    * `low`
    * `normal`
    * `high`
    """

    include_movie_poster: bool = False
    """
    Include movie posters of the relevant media in messages.
    """

    _implementation: str = "Gotify"
    _remote_map: List[RemoteMapEntry] = [
        ("base_url", "server", {"is_field": True}),
        ("app_token", "appToken", {"is_field": True}),
        ("priority", "priority", {"is_field": True}),
        ("include_movie_poster", "includeMoviePoster", {"is_field": True}),
    ]
