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
Plugin and instance configuration.
"""


from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

import radarr

from buildarr.config import ConfigPlugin
from buildarr.types import NonEmptyStr, Port
from typing_extensions import Self

from ..api import radarr_api_client
from ..types import ArrApiKey, RadarrProtocol
from .settings import RadarrSettings

if TYPE_CHECKING:
    from ..secrets import RadarrSecrets

    class _RadarrInstanceConfig(ConfigPlugin[RadarrSecrets]):
        ...

else:

    class _RadarrInstanceConfig(ConfigPlugin):
        ...


class RadarrInstanceConfig(_RadarrInstanceConfig):
    """
    By default, Buildarr will look for a single instance at `http://radarr:7878`.
    Most configurations are different, and to accommodate those, you can configure
    how Buildarr connects to individual Radarr instances.

    Configuration of a single Radarr instance:

    ```yaml
    radarr:
      hostname: "radarr.example.com"
      port: 7878
      protocol: "http"
      settings:
        ...
    ```

    Configuration of multiple instances:

    ```yaml
    radarr:
      # Configuration and settings common to all instances.
      port: 7878
      settings:
        ...
      instances:
        # Radarr instance 1-specific configuration.
        radarr1:
          hostname: "radarr1.example.com"
          settings:
            ...
        # Radarr instance 2-specific configuration.
        radarr2:
          hostname: "radarr2.example.com"
          api_key: "..." # Explicitly define API key
          settings:
            ...
    ```
    """

    hostname: NonEmptyStr = "radarr"  # type: ignore[assignment]
    """
    Hostname of the Radarr instance to connect to.

    When defining a single instance using the global `radarr` configuration block,
    the default hostname is `radarr`.

    When using multiple instance-specific configurations, the default hostname
    is the name given to the instance in the `instances` attribute.

    ```yaml
    radarr:
      instances:
        radarr1: # <--- This becomes the default hostname
          ...
    ```
    """

    port: Port = 7878  # type: ignore[assignment]
    """
    Port number of the Radarr instance to connect to.
    """

    protocol: RadarrProtocol = "http"  # type: ignore[assignment]
    """
    Communication protocol to use to connect to Radarr.

    Values:

    * `http`
    * `https`
    """

    api_key: Optional[ArrApiKey] = None
    """
    API key to use to authenticate with the Radarr instance.

    If undefined or set to `null`, automatically retrieve the API key.
    This can only be done on Radarr instances with authentication disabled.

    **If authentication is enabled on the Radarr instance, this field is required.**
    """

    version: Optional[str] = None
    """
    The expected version of the Radarr instance.
    If undefined or set to `null`, the version is auto-detected.

    This value is also used when generating a Docker Compose file.
    When undefined or set to `null`, the version tag will be set to `latest`.
    """

    image: NonEmptyStr = "lscr.io/linuxserver/radarr"  # type: ignore[assignment]
    """
    The default Docker image URI to use when generating a Docker Compose file.
    """

    settings: RadarrSettings = RadarrSettings()
    """
    Radarr application settings.

    Configuration options for Radarr itself are set within this structure.
    """

    def uses_trash_metadata(self) -> bool:
        if self.settings.quality.uses_trash_metadata():
            return True
        if self.settings.custom_formats.uses_trash_metadata():
            return True
        return False

    def post_init_render(self, secrets: RadarrSecrets) -> Self:
        copy = self.copy(deep=True)
        copy._post_init_render(secrets=secrets)
        return copy

    def _post_init_render(self, secrets: RadarrSecrets) -> None:
        if self.settings.quality.uses_trash_metadata():
            self.settings.quality._render()
        if self.settings.custom_formats.uses_trash_metadata():
            self.settings.custom_formats._post_init_render(secrets=secrets)
        self.settings.profiles.quality_profiles._render(
            custom_formats=self.settings.custom_formats.definitions,
        )

    @classmethod
    def from_remote(cls, secrets: RadarrSecrets) -> Self:
        with radarr_api_client(secrets=secrets) as api_client:
            version = radarr.SystemApi(api_client).get_system_status().version
        return cls(
            hostname=secrets.hostname,
            port=secrets.port,
            protocol=secrets.protocol,
            api_key=secrets.api_key,
            version=version,
            settings=RadarrSettings.from_remote(secrets),
        )

    def to_compose_service(self, compose_version: str, service_name: str) -> Dict[str, Any]:
        return {
            "image": f"{self.image}:{self.version or 'latest'}",
            "volumes": {service_name: "/config"},
        }


class RadarrConfig(RadarrInstanceConfig):
    """
    Radarr plugin global configuration class.
    """

    instances: Dict[str, RadarrInstanceConfig] = {}
    """
    Instance-specific Radarr configuration.

    Can only be defined on the global `radarr` configuration block.

    Globally specified configuration values apply to all instances.
    Configuration values specified on an instance-level take precedence at runtime.
    """
