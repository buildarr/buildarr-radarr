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
PassThePopcorn indexer configuration.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr, Password
from pydantic import AnyHttpUrl

from .base import TorrentIndexer


class PassthepopcornIndexer(TorrentIndexer):
    # Monitor for new releases on PassThePopcorn.

    type: Literal["passthepopcorn"] = "passthepopcorn"
    """
    Type value associated with this kind of indexer.
    """

    base_url: AnyHttpUrl = "https://passthepopcorn.me"  # type: ignore[assignment]
    """
    PassThePopcorn API URL.

    Do not change this unless you know what you're doing,
    as your API key will be sent to this host.
    """

    api_user: NonEmptyStr
    """
    The API user of the PassThePopcorn account, as shown in Edit Profile > Security.
    """

    api_key: Password
    """
    PassThePopcorn API key associated with the account.
    """

    _implementation = "Nyaa"
    _remote_map: List[RemoteMapEntry] = [
        ("base_url", "baseUrl", {"is_field": True}),
        ("api_user", "aPIUser", {"is_field": True}),
        ("api_key", "aPIKey", {"is_field": True}),
    ]
