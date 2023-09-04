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
Torrent RSS feed indexer configuration.
"""


from __future__ import annotations

from typing import List, Literal, Optional

from buildarr.config import RemoteMapEntry
from buildarr.types import RssUrl

from .base import TorrentIndexer


class TorrentRssIndexer(TorrentIndexer):
    # Generic parser for monitoring a torrent RSS feed.

    type: Literal[
        "torrent-rss",
        "torrent-rss-feed",
        "torrent_rss",
        "torrent_rss_feed",
        "torrentrss",
        "torrentrssfeed",
    ] = "torrent-rss"
    """
    Type values associated with this kind of indexer.
    """

    base_url: RssUrl
    """
    Full RSS feed URL to monitor.
    """

    cookie: Optional[str] = None
    """
    Session cookie for accessing the RSS feed.

    If the RSS feed requires one, this should be retrieved manually via a web browser.
    """

    allow_zero_size: bool = False
    """
    Allow access to releases that don't specify release size.

    As size checks will not be performed, be careful when enabling this option.
    """

    _implementation = "TorrentRssIndexer"
    _remote_map: List[RemoteMapEntry] = [
        ("full_rss_feed_url", "feedUrl", {"is_field": True}),
        (
            "cookie",
            "cookie",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        ("allow_zero_size", "allowZeroSize", {"is_field": True}),
    ]
