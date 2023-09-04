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
HDBits indexer configuration.
"""


from __future__ import annotations

from typing import List, Literal, Set

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr, Password
from pydantic import AnyHttpUrl

from .base import TorrentIndexer


class HdbitsCategory(BaseEnum):
    MOVIE = "Movie"
    TV = "Tv"
    DOCUMENTARY = "Documentary"
    MUSIC = "Music"
    SPORT = "Sport"
    AUDIO = "Audio"
    XXX = "Xxx"
    MISCDEMO = "MiscDemo"


class HdbitsCodec(BaseEnum):
    H264 = "H264"
    MPEG2 = "MPEG2"
    VC1 = "VC1"
    XVID = "Xvid"
    HEVC = "HEVC"


class HdbitsMedium(BaseEnum):
    BLURAY = "Bluray"
    ENCODE = "Encode"
    CAPTURE = "Capture"
    REMUX = "Remux"
    WEBDL = "WebDl"


class HdbitsIndexer(TorrentIndexer):
    # Monitor for new releases on HDBits.

    type: Literal["hdbits"] = "hdbits"
    """
    Type value associated with this kind of indexer.
    """

    base_url: AnyHttpUrl = "https://hdbits.org"  # type: ignore[assignment]
    """
    HDBits API URL.

    Do not change this unless you know what you're doing,
    as your API key will be sent to this host.
    """

    username: NonEmptyStr
    """
    HDBits account username.
    """

    api_key: Password
    """
    HDBits API key assigned to the account.
    """

    categories: Set[HdbitsCategory] = {HdbitsCategory.MOVIE}
    """
    Categories to filter releases by in the indexer.

    If defined as an empty list, search under all categories.

    Values:

    * `Movie`
    * `TV`
    * `Documentary`
    * `Music`
    * `Sport`
    * `Audio`
    * `XXX`
    * `MiscDemo`
    """

    codecs: Set[HdbitsCodec] = set()
    """
    Only allow releases using the defined codecs.

    If defined as an empty list, allow all codecs.

    Values:

    * `H264`
    * `MPEG2`
    * `VC1`
    * `Xvid`
    * `HEVC`
    """

    mediums: Set[HdbitsMedium] = set()
    """
    Only allow releases using the defined codecs.

    If defined as an empty list, allow all codecs.

    Values:

    * `Bluray`
    * `Encode`
    * `Capture`
    * `Remux`
    * `WebDl`
    """

    _implementation = "HDBits"
    _remote_map: List[RemoteMapEntry] = [
        ("base_url", "baseUrl", {"is_field": True}),
        ("username", "username", {"is_field": True}),
        ("api_key", "apiKey", {"is_field": True}),
        ("categories", "categories", {"is_field": True}),
        ("codecs", "codecs", {"is_field": True}),
        ("mediums", "mediums", {"is_field": True}),
    ]
