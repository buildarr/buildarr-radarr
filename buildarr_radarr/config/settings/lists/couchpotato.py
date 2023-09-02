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
CouchPotato import list configuration.
"""


from __future__ import annotations

from typing import List, Literal, Optional
from urllib.parse import urlparse

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr, Password, Port

from .base import ImportList


class CouchpotatoImportList(ImportList):
    """ """

    type: Literal["couchpotato"] = "couchpotato"
    """
    Type value associated with this kind of import list.
    """

    host: NonEmptyStr
    """ """

    port: Port = 5050  # type: ignore[assignment]
    """ """

    use_ssl: bool = False
    """ """

    url_base: Optional[str] = None
    """ """

    api_key: Password
    """ """

    only_wanted: bool = True
    """
    Only add wanted movies.
    """

    _implementation: Literal["CouchPotatoImport"] = "CouchPotatoImport"
    _remote_map: List[RemoteMapEntry] = [
        (
            "host",
            "link",
            {
                "is_field": True,
                "decoder": lambda v: urlparse(v).netloc,
                "root_encoder": lambda vs: f"{'https' if vs.use_ssl else 'http'}://{vs.host}",
            },
        ),
        ("port", "port", {"is_field": True}),
        (
            "use_ssl",
            "link",
            {
                "is_field": True,
                "decoder": lambda v: urlparse(v).scheme == "https",
                "root_encoder": lambda vs: f"{'https' if vs.use_ssl else 'http'}://{vs.host}",
            },
        ),
        (
            "url_base",
            "urlBase",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        ("only_wanted", "onlyActive", {"is_field": True}),
    ]
