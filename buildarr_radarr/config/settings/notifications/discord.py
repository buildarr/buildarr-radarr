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
Discord notification connection configuration.
"""


from __future__ import annotations

from typing import List, Literal, Optional, Set

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum
from pydantic import AnyHttpUrl

from .base import Notification


class OnGrabField(BaseEnum):
    overview = 0
    rating = 1
    genres = 2
    quality = 3
    group = 4
    size = 5
    links = 6
    release = 7
    poster = 8
    fanart = 9
    indexer = 10
    custom_formats = 11
    custom_format_score = 12


class OnImportField(BaseEnum):
    overview = 0
    rating = 1
    genres = 2
    quality = 3
    codecs = 4
    group = 5
    size = 6
    languages = 7
    subtitles = 8
    links = 9
    release = 10
    poster = 11
    fanart = 12


class OnManualInteractionField(BaseEnum):
    overview = 0
    rating = 1
    genres = 2
    quality = 3
    group = 4
    size = 5
    links = 6
    download_title = 7
    poster = 8
    fanart = 9


class DiscordNotification(Notification):
    """
    Send media update and health alert messages to a Discord server.
    """

    type: Literal["discord"] = "discord"
    """
    Type value associated with this kind of connection.
    """

    webhook_url: AnyHttpUrl
    """
    Discord server webhook URL.
    """

    username: Optional[str] = None
    """
    The username to post as.

    If unset, blank or set to `None`, use the default username set to the webhook URL.
    """

    avatar: Optional[str] = None
    """
    Change the avatar that is used for messages from this connection.

    If unset, blank or set to `None`, use the default avatar for the user.
    """

    # Name override, None -> use machine_name
    host: Optional[str] = None
    """
    Override the host name that shows for this notification.

    If unset, blank or set to `None`, use the machine name.
    """

    on_grab_fields: Set[OnGrabField] = {
        OnGrabField.overview,
        OnGrabField.rating,
        OnGrabField.genres,
        OnGrabField.quality,
        OnGrabField.group,
        OnGrabField.size,
        OnGrabField.links,
        OnGrabField.release,
        OnGrabField.poster,
        OnGrabField.fanart,
        OnGrabField.indexer,
        OnGrabField.custom_formats,
        OnGrabField.custom_format_score,
    }
    """
    Set the fields that are passed in for this 'on grab' notification.
    By default, all fields are passed in.

    Values:

    * `overview`
    * `rating`
    * `genres`
    * `quality`
    * `group`
    * `size`
    * `links`
    * `release`
    * `poster`
    * `fanart`
    * `indexer`
    * `custom-formats`
    * `custom-format-score`

    Example:

    ```yaml
    ...
      notifications:
        definitions:
          Discord:
            type: discord
            webhook_url: "https://..."
            on_grab_fields:
              - overview
              - quality
              - release
    ```
    """

    on_import_fields: Set[OnImportField] = {
        OnImportField.overview,
        OnImportField.rating,
        OnImportField.genres,
        OnImportField.quality,
        OnImportField.codecs,
        OnImportField.group,
        OnImportField.size,
        OnImportField.languages,
        OnImportField.subtitles,
        OnImportField.links,
        OnImportField.release,
        OnImportField.poster,
        OnImportField.fanart,
    }
    """
    Set the fields that are passed in for this 'on import' notification.
    By default, all fields are passed in.

    Values:

    * `overview`
    * `rating`
    * `genres`
    * `quality`
    * `codecs`
    * `group`
    * `size`
    * `languages`
    * `subtitles`
    * `links`
    * `release`
    * `poster`
    * `fanart`

    Example:

    ```yaml
    ...
      notifications:
        definitions:
          Discord:
            type: discord
            webhook_url: https://...
            on_import_fields:
              - overview
              - quality
              - release
    ```
    """

    on_manual_interaction_fields: Set[OnManualInteractionField] = {
        OnManualInteractionField.overview,
        OnManualInteractionField.rating,
        OnManualInteractionField.genres,
        OnManualInteractionField.quality,
        OnManualInteractionField.group,
        OnManualInteractionField.size,
        OnManualInteractionField.links,
        OnManualInteractionField.download_title,
        OnManualInteractionField.poster,
        OnManualInteractionField.fanart,
    }

    _implementation: str = "Discord"
    _remote_map: List[RemoteMapEntry] = [
        ("webhook_url", "webHookUrl", {"is_field": True}),
        (
            "username",
            "username",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        (
            "avatar",
            "avatar",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        (
            "host",
            "author",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        (
            "on_grab_fields",
            "grabFields",
            {"is_field": True, "encoder": lambda v: sorted(f.value for f in v)},
        ),
        (
            "on_import_fields",
            "importFields",
            {"is_field": True, "encoder": lambda v: sorted(f.value for f in v)},
        ),
        (
            "on_manual_interaction_fields",
            "manualInteractionFields",
            {"is_field": True, "encoder": lambda v: sorted(f.value for f in v)},
        ),
    ]
