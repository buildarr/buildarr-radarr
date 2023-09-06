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
Custom script notification connection configuration.
"""


from __future__ import annotations

from logging import getLogger
from typing import List, Literal, Optional

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr

from .base import Notification

logger = getLogger(__name__)


class CustomScriptNotification(Notification):
    """
    Execute a local script on the Radarr host (container) when events occur.
    """

    type: Literal["custom-script", "custom_script", "customscript"] = "custom-script"
    """
    Type value associated with this kind of connection.
    """

    path: NonEmptyStr
    """
    Path of the script to execute.
    """

    arguments: Optional[str] = None
    """
    Arguments to pass to the script, if required.
    """

    _implementation: str = "CustomScript"
    _remote_map: List[RemoteMapEntry] = [("path", "path", {"is_field": True})]
