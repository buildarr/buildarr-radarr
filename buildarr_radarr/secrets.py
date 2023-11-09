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
Plugin secrets file model.
"""


from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

import radarr

from buildarr.secrets import SecretsPlugin
from buildarr.types import NonEmptyStr, Port
from radarr.exceptions import UnauthorizedException

from .api import api_get, radarr_api_client
from .exceptions import RadarrAPIError, RadarrSecretsUnauthorizedError
from .types import ArrApiKey, RadarrProtocol

if TYPE_CHECKING:
    from typing_extensions import Self

    from .config import RadarrConfig

    class _RadarrSecrets(SecretsPlugin[RadarrConfig]):
        ...

else:

    class _RadarrSecrets(SecretsPlugin):
        ...


class RadarrSecrets(_RadarrSecrets):
    """
    Radarr API secrets.
    """

    hostname: NonEmptyStr
    port: Port
    protocol: RadarrProtocol
    api_key: ArrApiKey
    version: NonEmptyStr

    @property
    def host_url(self) -> str:
        return f"{self.protocol}://{self.hostname}:{self.port}"

    @classmethod
    def get(cls, config: RadarrConfig) -> Self:
        if config.api_key:
            api_key = config.api_key.get_secret_value()
            remote_metadata = api_get(config.host_url, "/initialize.json", api_key=api_key)
            # TODO: Switch to `radarr.InitializeJsApi.get_initialize_js` when fixed.
            # with radarr_api_client(host_url=config.host_url) as api_client:
            #     remote_metadata = radarr.InitializeJsApi(api_client).get_initialize_js()
        else:
            try:
                remote_metadata = api_get(config.host_url, "/initialize.json")
            except RadarrAPIError as err:
                if err.status_code == HTTPStatus.UNAUTHORIZED:
                    raise RadarrSecretsUnauthorizedError(
                        "Unable to retrieve the API key for the Radarr instance "
                        f"at '{config.host_url}': Authentication is enabled. "
                        "Please try manually setting the "
                        "'Settings -> General -> Authentication Required' attribute "
                        "to 'Disabled for Local Addresses', or if that does not work, "
                        "explicitly define the API key in the Buildarr configuration.",
                    ) from None
                else:
                    raise
            else:
                api_key = remote_metadata["apiKey"]
        return cls(
            hostname=config.hostname,
            port=config.port,
            protocol=config.protocol,
            api_key=api_key,  # type: ignore[arg-type]
            version=remote_metadata["version"],
        )

    def test(self) -> bool:
        with radarr_api_client(secrets=self) as api_client:
            try:
                radarr.SystemApi(api_client).get_system_status()
            except UnauthorizedException:
                return False
        return True
