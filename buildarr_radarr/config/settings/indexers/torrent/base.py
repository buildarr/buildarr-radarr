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
Torrent indexer configuration base class.
"""


from __future__ import annotations

from logging import getLogger
from typing import List, Mapping, Optional, Set

import radarr

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr
from pydantic import PositiveInt, validator

from ..base import Indexer

logger = getLogger(__name__)


class TorrentIndexer(Indexer):
    # Configuration attributes common to all torrent indexers.

    minimum_seeders: PositiveInt = 1
    """
    The minimum number of seeders required before downloading a release.
    """

    required_flags: Set[NonEmptyStr] = set()
    """
    Require one or more indexer flags to be set on candidate releases.

    If the required flags are not set, the release will be rejected.

    All values supported by your Radarr instance version can be defined.
    As of Radarr v4.7.5, the following flags are available:

    * `g-freeleech`
    * `g-halfleech`
    * `g-doubleupload`
    * `ptp-golden`
    * `ptp-approved`
    * `hdb-internal`
    * `ahd-internal`
    * `g-scene`
    * `g-freeleech75`
    * `g-freeleech25`
    * `ahd-userrelease`
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
    def _flag_parse(cls, value: str) -> str:
        # Results:
        #   1. G Freeleech -> g-freeleech
        #   2. G_FREELEECH -> g-freeleech
        return value.lower().replace("_", "-").replace(" ", "-")

    @validator("required_flags")
    def validate_flag(cls, value: Set[str]) -> Set[str]:
        return set(cls._flag_parse(flag) for flag in value)

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
            (
                "required_flags",
                "requiredFlags",
                {
                    "decoder": lambda v: set(cls._flag_decode(api_schema, f) for f in v),
                    "encoder": lambda v: sorted(cls._flag_encode(api_schema, f) for f in v),
                    "is_field": True,
                },
            ),
            ("seed_ratio", "seedCriteria.seedRatio", {"is_field": True, "field_default": None}),
            ("seed_time", "seedCriteria.seedTime", {"is_field": True, "field_default": None}),
        ]

    @classmethod
    def _flag_decode(cls, api_schema: radarr.IndexerResource, value: int) -> str:
        field: radarr.Field = next(f for f in api_schema.fields if f.name == "requiredFlags")
        select_options: List[radarr.SelectOption] = field.select_options
        for option in select_options:
            option_name: str = option.name
            option_value: int = option.value
            if option_value == value:
                return cls._flag_parse(option_name)
        supported_flags = ", ".join(
            (f"{cls._flag_parse(o.name)} ({o.value})" for o in select_options),
        )
        raise ValueError(
            f"Invalid custom format quality flag value {value} during decoding"
            f", supported quality flags are: {supported_flags}",
        )

    @classmethod
    def _flag_encode(cls, api_schema: radarr.IndexerResource, value: str) -> int:
        field: radarr.Field = next(f for f in api_schema.fields if f.name == "requiredFlags")
        select_options: List[radarr.SelectOption] = field.select_options
        for option in select_options:
            option_name: str = option.name
            option_value: int = option.value
            if cls._flag_parse(option_name) == value:
                return option_value
        supported_flags = ", ".join(cls._flag_parse(o.name) for o in select_options)
        raise ValueError(
            f"Invalid or unsupported custom format flag name '{value}'"
            f", supported flags are: {supported_flags}",
        )
