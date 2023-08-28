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
from .download_clients import RadarrDownloadClientsSettings
from .general import RadarrGeneralSettings
from .indexers import RadarrIndexersSettings
from .lists import RadarrListsSettings
from .media_management import RadarrMediaManagementSettings
from .quality import RadarrQualitySettings
from .profiles import RadarrProfilesSettings
from .tags import RadarrTagsSettings
from .ui import RadarrUISettings

if TYPE_CHECKING:
    from ...secrets import RadarrSecrets


class RadarrSettings(RadarrConfigBase):
    """
    Radarr settings, used to configure a remote Radarr instance.
    """

    media_management: RadarrMediaManagementSettings = RadarrMediaManagementSettings()
    profiles: RadarrProfilesSettings = RadarrProfilesSettings()
    quality: RadarrQualitySettings = RadarrQualitySettings()
    custom_formats: RadarrCustomFormatsSettings = RadarrCustomFormatsSettings()
    indexers: RadarrIndexersSettings = RadarrIndexersSettings()
    download_clients: RadarrDownloadClientsSettings = RadarrDownloadClientsSettings()
    lists: RadarrListsSettings = RadarrListsSettings()
    connect: RadarrConnectSettings = RadarrConnectSettings()
    metadata: RadarrMetadataSettings = RadarrMetadataSettings()
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
        # 2. Qualities must be updated before quality profiles.
        # 3. Download clients must be created before indexers.
        return any(
            [
                self.tags.update_remote(
                    f"{tree}.tags",
                    secrets,
                    remote.tags,
                    check_unmanaged=check_unmanaged,
                ),
                self.quality.update_remote(
                    f"{tree}.quality",
                    secrets,
                    remote.quality,
                    check_unmanaged=check_unmanaged,
                ),
                self.download_clients.update_remote(
                    f"{tree}.download_clients",
                    secrets,
                    remote.download_clients,
                    check_unmanaged=check_unmanaged,
                ),
                self.indexers.update_remote(
                    f"{tree}.indexers",
                    secrets,
                    remote.indexers,
                    check_unmanaged=check_unmanaged,
                ),
                self.media_management.update_remote(
                    f"{tree}.media_management",
                    secrets,
                    remote.media_management,
                    check_unmanaged=check_unmanaged,
                ),
                self.profiles.update_remote(
                    f"{tree}.profiles",
                    secrets,
                    remote.profiles,
                    check_unmanaged=check_unmanaged,
                ),
                self.lists.update_remote(
                    f"{tree}.lists",
                    secrets,
                    remote.lists,
                    check_unmanaged=check_unmanaged,
                ),
                self.connect.update_remote(
                    f"{tree}.connect",
                    secrets,
                    remote.connect,
                    check_unmanaged=check_unmanaged,
                ),
                self.metadata.update_remote(
                    f"{tree}.metadata",
                    secrets,
                    remote.metadata,
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
        # 1. Indexers must be deleted before download clients.
        return any(
            [
                self.profiles.delete_remote(f"{tree}.profiles", secrets, remote.profiles),
                self.indexers.delete_remote(f"{tree}.indexers", secrets, remote.indexers),
                self.download_clients.delete_remote(
                    f"{tree}.download_clients",
                    secrets,
                    remote.download_clients,
                ),
                self.media_management.delete_remote(
                    f"{tree}.media_management",
                    secrets,
                    remote.media_management,
                ),
                self.lists.delete_remote(f"{tree}.lists", secrets, remote.lists),
                self.connect.delete_remote(f"{tree}.connect", secrets, remote.connect),
                self.tags.delete_remote(f"{tree}.tags", secrets, remote.tags),
                self.quality.delete_remote(f"{tree}.quality", secrets, remote.quality),
                self.metadata.delete_remote(f"{tree}.metadata", secrets, remote.metadata),
                self.general.delete_remote(f"{tree}.general", secrets, remote.general),
                self.ui.delete_remote(f"{tree}.ui", secrets, remote.ui),
            ],
        )
