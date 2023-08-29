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
Prowlarr plugin notification connection configuration.
"""


from __future__ import annotations

from logging import getLogger
from typing import Any, Dict, List, Literal, Mapping, Optional, Set, Tuple, Type, Union

import prowlarr

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr, Password, Port
from pydantic import AnyHttpUrl, ConstrainedInt, Field, NameEmail, SecretStr
from typing_extensions import Annotated, Self

from ...api import prowlarr_api_client
from ...secrets import ProwlarrSecrets
from ..types import ProwlarrConfigBase


class NotifiarrNotification(Notification):
    """
    Send media update and health alert emails via the Notifiarr notification service.
    """

    type: Literal["notifiarr"] = "notifiarr"
    """
    Type value associated with this kind of connection.
    """

    api_key: Password
    """
    API key to use to authenticate with Notifiarr.
    """

    _implementation: str = "Notifiarr"
    _remote_map: List[RemoteMapEntry] = [("api_key", "apiKey", {"is_field": True})]
