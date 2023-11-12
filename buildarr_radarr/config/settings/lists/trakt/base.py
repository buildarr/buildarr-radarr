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
Trakt import list configuration base class.
"""


from __future__ import annotations

import re

from datetime import datetime
from logging import getLogger
from typing import (
    List,
    Mapping,
    Optional,
    Set,
)

from buildarr.config import RemoteMapEntry
from buildarr.types import LowerCaseNonEmptyStr, NonEmptyStr, Password
from pydantic import ConstrainedStr, PositiveInt

from ....util import trakt_expires_encoder
from ..base import ImportList

logger = getLogger(__name__)


class YearRange(ConstrainedStr):
    """
    Constrained string type for a singular year or range of years.
    """

    regex = re.compile(r"[0-9]+(?:-[0-9]+)?")

    # TODO: validate that the end year is higher than the start year


class TraktImportList(ImportList):
    """
    Import added media from a list on the Trakt media tracker.

    !!! note

        Radarr directly authenticates with Trakt to generate tokens for it to use.
        At the moment, the easiest way to generate the tokens for Buildarr
        is to do it using the GUI within Radarr, and use the following
        shell command to retrieve the generated configuration.

        ```bash
        curl -X "GET" "<radarr-url>/api/v3/notification" -H "X-Api-Key: <api-key>"
        ```

    The following parameters are common to all Trakt import list types.
    The authenticated-related parameters (`access_token`, `refresh_token`, `expires`, `auth_user`)
    are required.
    """

    # Base class for import lists based on Trakt.

    # FIXME: Determine easier procedure for getting access tokens and test.

    access_token: Password
    """
    Access token for Radarr from Trakt.
    """

    refresh_token: Password
    """
    Refresh token for Radarr from Trakt.
    """

    expires: datetime
    """
    Expiry date-time of the access token, preferably in ISO-8601 format and in UTC.

    Example: `2023-05-10T15:34:08.117451Z`
    """

    auth_user: LowerCaseNonEmptyStr
    """
    The username being authenticated in Trakt.
    """

    # rating
    # TODO: constraints
    rating: NonEmptyStr = "0-100"  # type: ignore[assignment]
    """
    Filter series by rating range, with a maximum range of 0-100.
    """

    username: Optional[str] = None
    """
    Username for the list to import from.

    Leave undefined, empty or set to `None` to use the auth user.
    """

    genres: Set[NonEmptyStr] = set()
    """
    Filter series by Trakt genre slug.
    """

    years: Optional[YearRange] = None
    """
    Filter series by year or year range. (e.g. `2009` or `2009-2015`)
    """

    limit: PositiveInt = 100
    """
    Limit the number of series to get.
    """

    trakt_additional_parameters: Optional[str] = None
    """
    Additional parameters to send to the Trakt API.
    """

    @classmethod
    def _get_base_remote_map(
        cls,
        quality_profile_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
    ) -> List[RemoteMapEntry]:
        return [
            *super()._get_base_remote_map(
                quality_profile_ids=quality_profile_ids,
                tag_ids=tag_ids,
            ),
            ("access_token", "accessToken", {"is_field": True}),
            ("refresh_token", "refreshToken", {"is_field": True}),
            ("expires", "expires", {"is_field": True, "encoder": trakt_expires_encoder}),
            ("auth_user", "authUser", {"is_field": True}),
            ("rating", "rating", {"is_field": True}),
            (
                "username",
                "username",
                {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
            ),
            (
                "genres",
                "genres",
                {
                    "is_field": True,
                    "decoder": lambda v: set(v.split(",")) if v else set(),
                    "encoder": lambda v: ",".join(sorted(v)) if v else "",
                },
            ),
            (
                "years",
                "years",
                {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
            ),
            ("limit", "limit", {"is_field": True}),
            ("trakt_additional_parameters", "traktAdditionalParameters", {"is_field": True}),
        ]
