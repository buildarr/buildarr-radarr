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
from typing import List, Mapping, Optional

import radarr

from buildarr.config import RemoteMapEntry
from pydantic import PositiveInt

from ..base import Indexer

logger = getLogger(__name__)


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

    @classmethod
    def _get_base_remote_map(
        cls,
        api_schema: radarr.IndexerResource,
        downloadclient_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
    ) -> List[RemoteMapEntry]:
        return [
            *super()._get_base_remote_map(
                api_schema=api_schema,
                downloadclient_ids=downloadclient_ids,
                tag_ids=tag_ids,
            ),
            ("minimum_seeders", "minimumSeeders", {"is_field": True, "field_default": None}),
            ("seed_ratio", "seedCriteria.seedRatio", {"is_field": True, "field_default": None}),
            ("seed_time", "seedCriteria.seedTime", {"is_field": True, "field_default": None}),
        ]
