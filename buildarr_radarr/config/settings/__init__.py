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
Radarr plugin settings configuration.
"""


from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import Self

from ..types import RadarrConfigBase
from .apps import RadarrAppsSettings
from .download_clients import RadarrDownloadClientsSettings
from .general import RadarrGeneralSettings
from .indexers import RadarrIndexersSettings
from .notifications import RadarrNotificationsSettings
from .tags import RadarrTagsSettings
from .ui import RadarrUISettings

if TYPE_CHECKING:
    from ...secrets import RadarrSecrets


class RadarrSettings(RadarrConfigBase):
    """
    Radarr settings, used to configure a remote Radarr instance.
    """

    indexers: RadarrIndexersSettings = RadarrIndexersSettings()
    apps: RadarrAppsSettings = RadarrAppsSettings()
    download_clients: RadarrDownloadClientsSettings = RadarrDownloadClientsSettings()
    notifications: RadarrNotificationsSettings = RadarrNotificationsSettings()
    tags: RadarrTagsSettings = RadarrTagsSettings()
    general: RadarrGeneralSettings = RadarrGeneralSettings()
    ui: RadarrUISettings = RadarrUISettings()

    def update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        # Overload base function to guarantee execution order of section updates.
        # 1. Tags must be created before everything else.
        # 2. Apps/Sync Profiles must be created before Indexers.
        return any(
            [
                self.tags.update_remote(
                    f"{tree}.tags",
                    secrets,
                    remote.tags,
                    check_unmanaged=check_unmanaged,
                ),
                self.apps.update_remote(
                    f"{tree}.apps",
                    secrets,
                    remote.apps,
                    check_unmanaged=check_unmanaged,
                ),
                self.indexers.update_remote(
                    f"{tree}.indexers",
                    secrets,
                    remote.indexers,
                    check_unmanaged=check_unmanaged,
                ),
                self.download_clients.update_remote(
                    f"{tree}.download_clients",
                    secrets,
                    remote.download_clients,
                    check_unmanaged=check_unmanaged,
                ),
                self.notifications.update_remote(
                    f"{tree}.notifications",
                    secrets,
                    remote.notifications,
                    check_unmanaged=check_unmanaged,
                ),
                self.general.update_remote(
                    f"{tree}.general",
                    secrets,
                    remote.general,
                    check_unmanaged=check_unmanaged,
                ),
                self.ui.update_remote(
                    f"{tree}.ui",
                    secrets,
                    remote.ui,
                    check_unmanaged=check_unmanaged,
                ),
            ],
        )

    def delete_remote(self, tree: str, secrets: RadarrSecrets, remote: Self) -> bool:
        # Overload base function to guarantee execution order of section deletions.
        # 1. Indexers must be deleted before Apps/Sync Profiles.
        return any(
            [
                self.indexers.delete_remote(f"{tree}.indexers", secrets, remote.indexers),
                self.apps.delete_remote(f"{tree}.apps", secrets, remote.apps),
                self.download_clients.delete_remote(
                    f"{tree}.download_clients",
                    secrets,
                    remote.download_clients,
                ),
                self.notifications.delete_remote(
                    f"{tree}.notifications",
                    secrets,
                    remote.notifications,
                ),
                self.tags.delete_remote(f"{tree}.tags", secrets, remote.tags),
                self.general.delete_remote(f"{tree}.general", secrets, remote.general),
                self.ui.delete_remote(f"{tree}.ui", secrets, remote.ui),
            ],
        )
