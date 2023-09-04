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
Nyaa indexer configuration.
"""


from __future__ import annotations

from typing import List, Literal, Optional

from buildarr.config import RemoteMapEntry
from pydantic import AnyHttpUrl

from .base import TorrentIndexer


class NyaaIndexer(TorrentIndexer):
    # Monitor for new releases on the configured Nyaa domain.

    type: Literal["nyaa"] = "nyaa"
    """
    Type value associated with this kind of indexer.
    """

    base_url: AnyHttpUrl
    """
    Base URL for accessing Nyaa.
    """

    additional_parameters: Optional[str] = "&cats=1_0&filter=1"
    """
    Parameters to send in the Nyaa search request.

    Note that if you change the category, you will have to add
    required/restricted rules about the subgroups to avoid foreign language releases.
    """

    _implementation = "Nyaa"
    _remote_map: List[RemoteMapEntry] = [
        ("base_url", "baseUrl", {"is_field": True}),
        (
            "additional_parameters",
            "additionalParameters",
            {"is_field": True, "field_default": None, "decoder": lambda v: v or None},
        ),
    ]
