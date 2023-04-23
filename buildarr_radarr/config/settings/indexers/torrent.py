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

from logging import getLogger
from typing import List, Literal, Mapping, Optional, Set

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr, Password, RssUrl
from pydantic import AnyHttpUrl, PositiveInt

from .base import Indexer, NabCategory

logger = getLogger(__name__)


class FilelistCategory(BaseEnum):
    """
    Filelist category enumeration.
    """

    ANIME = "Anime"
    ANIMATION = "Animation"
    TV_4K = "TV 4K"
    TV_HD = "TV HD"
    TV_SD = "TV SD"
    SPORT = "Sport"


class TorrentIndexer(Indexer):
    """
    Configuration attributes common to all torrent indexers.
    """

    minimum_seeders: PositiveInt = 1
    """
    The minimum number of seeders required before downloading a release.
    """

    seed_ratio: Optional[float] = None
    """
    The seed ratio a torrent should reach before stopping.

    If unset or set to `null`, use the download client's defaults.
    """

    seed_time: Optional[int] = None  # minutes
    """
    The amount of time (in minutes) a torrent should be seeded before stopping.

    If unset or set to `null`, use the download client's defaults.
    """

    seasonpack_seed_time: Optional[int] = None  # minutes
    """
    The amount of time (in minutes) a season-pack torrent should be seeded before stopping.

    If unset or set to `null`, use the download client's defaults.
    """

    @classmethod
    def _get_base_remote_map(
        cls,
        download_client_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
    ) -> List[RemoteMapEntry]:
        return [
            *super()._get_base_remote_map(download_client_ids, tag_ids),
            ("minimum_seeders", "minimumSeeders", {"is_field": True, "field_default": None}),
            ("seed_ratio", "seedCriteria.seedRatio", {"is_field": True, "field_default": None}),
            ("seed_time", "seedCriteria.seedTime", {"is_field": True, "field_default": None}),
            (
                "seasonpack_seed_time",
                "seedCriteria.seasonPackSeedTime",
                {"is_field": True, "field_default": None},
            ),
        ]


class FilelistIndexer(TorrentIndexer):
    """
    Monitor for new releases on FileList.io.
    """

    type: Literal["filelist"] = "filelist"
    """
    Type value associated with this kind of indexer.
    """

    username: NonEmptyStr
    """
    FileList username.
    """

    passkey: Password
    """
    FileList account API key.
    """

    api_url: AnyHttpUrl = "https://filelist.io"  # type: ignore[assignment]
    """
    FileList API URL.

    Do not change this unless you know what you're doing,
    as your API key will be sent to this host.
    """

    categories: Set[FilelistCategory] = {
        FilelistCategory.TV_SD,
        FilelistCategory.TV_HD,
        FilelistCategory.TV_4K,
    }
    """
    Categories to monitor for standard/daily show new releases.

    Set to an empty list to not monitor for standard/daily shows.

    Values:

    * `Anime`
    * `Animation`
    * `TV 4K`
    * `TV HD`
    * `TV SD`
    * `Sport`
    """

    anime_categories: Set[FilelistCategory] = set()
    """
    Categories to monitor for anime new releases.

    Leave empty to not monitor for anime.

    Values:

    * `Anime`
    * `Animation`
    * `TV 4K`
    * `TV HD`
    * `TV SD`
    * `Sport`
    """

    _implementation = "FileList"
    _remote_map: List[RemoteMapEntry] = [
        ("username", "username", {"is_field": True}),
        ("passkey", "passKey", {"is_field": True}),
        ("api_url", "apiUrl", {"is_field": True}),
        (
            "categories",
            "categories",
            {"is_field": True, "encoder": lambda v: sorted(c.value for c in v)},
        ),
        (
            "anime_categories",
            "animeCategories",
            {"is_field": True, "encoder": lambda v: sorted(c.value for c in v)},
        ),
    ]


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


class IptorrentsIndexer(TorrentIndexer):
    """
    Monitor for releases using the IP Torrents native API.

    !!! note
        IP Torrents' native API does not support automatic searching.
        It is recommended to instead configure IP Torrents as a Torznab indexer.
    """

    type: Literal["iptorrents"] = "iptorrents"
    """
    Type value associated with this kind of indexer.
    """

    # NOTE: automatic_search and interactive_search are not supported
    # by this indexer, therefore its value is ignored.

    feed_url: RssUrl
    """
    The full RSS feed url generated by IP Torrents, using only the categories
    you selected (HD, SD, x264, etc ...).
    """

    _implementation = "IPTorrents"
    _remote_map: List[RemoteMapEntry] = [
        ("feed_url", "feedUrl", {"is_field": True}),
    ]


class NyaaIndexer(TorrentIndexer):
    """
    Monitor for new anime releases on the configured Nyaa domain.

    Nyaa only supports searching for Anime series type releases.
    """

    type: Literal["nyaa"] = "nyaa"
    """
    Type value associated with this kind of indexer.
    """

    website_url: AnyHttpUrl
    """
    HTTPS URL for accessing Nyaa.
    """

    anime_standard_format_search: bool = False
    """
    Also search for anime using the standard numbering. Only applies for Anime series types.
    """

    additional_parameters: Optional[str] = "&cats=1_0&filter=1"
    """
    Parameters to send in the Nyaa search request.

    Note that if you change the category, you will have to add
    required/restricted rules about the subgroups to avoid foreign language releases.
    """

    _implementation = "Nyaa"
    _remote_map: List[RemoteMapEntry] = [
        ("website_url", "websiteUrl", {"is_field": True}),
        ("anime_standard_format_search", "animeStandardFormatSearch", {"is_field": True}),
        (
            "additional_parameters",
            "additionalParameters",
            {"is_field": True, "field_default": None, "decoder": lambda v: v or None},
        ),
    ]


# TODO: PassThePopcorn


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


class TorrentrssfeedIndexer(TorrentIndexer):
    """
    Generic parser for monitoring a torrent RSS feed.

    !!! note
        This indexer does not support automatic searching.
        It is recommended to use an indexer that natively communicates with
        a tracker using an API.
    """

    type: Literal["torrentrssfeed"] = "torrentrssfeed"
    """
    Type value associated with this kind of indexer.
    """

    # NOTE: automatic_search and interactive_search are not supported
    # by this indexer, therefore its value is ignored.

    full_rss_feed_url: RssUrl
    """
    RSS feed to monitor.
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


# TODO: TorrentPotato


class TorznabIndexer(TorrentIndexer):
    """
    Monitor and search for new releases on a Torznab-compliant torrent indexing site.

    Sonarr defines presets for several popular sites.
    """

    type: Literal["torznab"] = "torznab"
    """
    Type value associated with this kind of indexer.
    """

    url: AnyHttpUrl
    """
    URL of the Torznab-compatible indexing site.
    """

    api_path: NonEmptyStr = "/api"  # type: ignore[assignment]
    """
    Tornab API endpoint. Usually `/api`.
    """

    api_key: Password
    """
    API key for use with the Torznab API.
    """

    categories: Set[NabCategory] = {NabCategory.TV_SD, NabCategory.TV_HD}
    """
    Categories to monitor for standard/daily shows.
    Define as empty to disable.

    Values:

    * `TV-WEBDL`
    * `TV-Foreign`
    * `TV-SD`
    * `TV-HD`
    * `TV-UHD`
    * `TV-Other`
    * `TV-Sports`
    * `TV-Anime`
    * `TV-Documentary`
    """

    anime_categories: Set[NabCategory] = set()
    """
    Categories to monitor for anime.

    Values:

    * `TV-WEBDL`
    * `TV-Foreign`
    * `TV-SD`
    * `TV-HD`
    * `TV-UHD`
    * `TV-Other`
    * `TV-Sports`
    * `TV-Anime`
    * `TV-Documentary`
    """

    anime_standard_format_search: bool = False
    """
    Also search for anime using the standard numbering. Only applies for Anime series types.
    """

    additional_parameters: Optional[str] = None
    """
    Additional Torznab API parameters.
    """

    _implementation = "Torznab"
    _remote_map: List[RemoteMapEntry] = [
        ("url", "baseUrl", {"is_field": True}),
        ("api_path", "apiPath", {"is_field": True}),
        ("api_key", "apiKey", {"is_field": True}),
        (
            "categories",
            "categories",
            {"is_field": True, "encoder": lambda v: sorted(c.value for c in v)},
        ),
        (
            "anime_categories",
            "animeCategories",
            {"is_field": True, "encoder": lambda v: sorted(c.value for c in v)},
        ),
        ("anime_standard_format_search", "animeStandardFormatSearch", {"is_field": True}),
        (
            "additional_parameters",
            "additionalParameters",
            {"is_field": True, "field_default": None, "decoder": lambda v: v or None},
        ),
    ]
