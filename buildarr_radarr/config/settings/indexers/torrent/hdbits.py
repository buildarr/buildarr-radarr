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
Radarr plugin torrent indexers configuration.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr, Password
from pydantic import AnyHttpUrl

from .base import TorrentIndexer


class HdbitsIndexer(TorrentIndexer):
    """
    Monitor for new releases on HDBits.
    """

    type: Literal["hdbits"] = "hdbits"
    """
    Type value associated with this kind of indexer.
    """

    username: NonEmptyStr
    """
    HDBits account username.
    """

    api_key: Password
    """
    HDBits API key assigned to the account.
    """

    api_url: AnyHttpUrl = "https://hdbits.org"  # type: ignore[assignment]
    """
    HDBits API URL.

    Do not change this unless you know what you're doing,
    as your API key will be sent to this host.
    """

    _implementation = "HDBits"
    _remote_map: List[RemoteMapEntry] = [
        ("username", "username", {"is_field": True}),
        ("api_key", "apiKey", {"is_field": True}),
        ("api_url", "apiUrl", {"is_field": True}),
    ]
