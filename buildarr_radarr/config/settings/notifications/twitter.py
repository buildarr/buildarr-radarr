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


class TwitterNotification(Notification):
    """
    Send media update and health alert messages via Twitter.

    Twitter requires you to create an application for their API
    to generate the necessary keys and secrets.
    If unsure how to proceed, refer to these guides from
    [Twitter](https://developer.twitter.com/en/docs/authentication/oauth-1-0a/api-key-and-secret)
    and [WikiArr](https://wiki.servarr.com/useful-tools#twitter-connect).

    Access tokens can be obtained using the prodecure documented [here](
    https://developer.twitter.com/en/docs/authentication/oauth-1-0a/obtaining-user-access-tokens).
    """

    type: Literal["twitter"] = "twitter"
    """
    Type value associated with this kind of connection.
    """

    consumer_key: Password
    """
    Consumer key from a Twitter application.
    """

    consumer_secret: Password
    """
    Consumer key from a Twitter application.
    """

    access_token: Password
    """
    Access token for a Twitter user.
    """

    access_token_secret: Password
    """
    Access token secret for a Twitter user.
    """

    mention: NonEmptyStr
    """
    Mention this user in sent tweets.
    """

    direct_message: bool = True
    """
    Send a direct message instead of a public message.
    """

    _implementation: str = "Twitter"
    _remote_map: List[RemoteMapEntry] = [
        ("consumer_key", "consumerKey", {"is_field": True}),
        ("consumer_secret", "consumerSecret", {"is_field": True}),
        ("access_token", "accessToken", {"is_field": True}),
        ("access_token_secret", "accessTokenSecret", {"is_field": True}),
        ("mention", "mention", {"is_field": True}),
        ("direct_message", "direct_message", {"is_field": True}),
    ]
