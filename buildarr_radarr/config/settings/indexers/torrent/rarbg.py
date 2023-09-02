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

from typing import List, Literal, Optional

from buildarr.config import RemoteMapEntry
from pydantic import AnyHttpUrl

from .base import TorrentIndexer


class RarbgIndexer(TorrentIndexer):
    """
    Monitor for new releases on the RARBG torrent tracker.
    """

    type: Literal["rarbg"] = "rarbg"
    """
    Type value associated with this kind of indexer.
    """

    api_url: AnyHttpUrl
    """
    RARBG API url.
    """

    ranked_only: bool = False
    """
    Only include ranked results.
    """

    captcha_token: Optional[str] = None
    """
    CAPTCHA clearance token used to handle CloudFlare anti-DDoS measures on shared-IP VPNs.
    """

    _implementation = "Rarbg"
    _remote_map: List[RemoteMapEntry] = [
        ("api_url", "apiUrl", {"is_field": True}),
        ("ranked_only", "rankedOnly", {"is_field": True}),
        (
            "captcha_token",
            "captchaToken",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
    ]
