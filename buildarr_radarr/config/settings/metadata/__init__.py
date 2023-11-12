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
Metadata settings configuration.
"""


from __future__ import annotations

from typing import Dict, List

import radarr

from buildarr.config import RemoteMapEntry
from buildarr.types import LowerCaseNonEmptyStr
from typing_extensions import Self

from ....api import radarr_api_client
from ....secrets import RadarrSecrets
from ...types import RadarrConfigBase
from .emby_legacy import EmbyLegacyMetadata
from .kodi_emby import KodiEmbyMetadata
from .roksbox import RoksboxMetadata
from .wdtv import WdtvMetadata

METADATA_TYPE_MAP = {
    metadata_type._implementation: metadata_type  # type: ignore[attr-defined]
    for metadata_type in (EmbyLegacyMetadata, KodiEmbyMetadata, RoksboxMetadata, WdtvMetadata)
}


class RadarrMetadataSettings(RadarrConfigBase):
    # Radarr metadata settings.
    #
    # Implementation wise each metadata is a unique object, updated using separate requests.

    certification_country: LowerCaseNonEmptyStr = "us"  # type: ignore[assignment]
    """
    The country to use for movie certifications in Radarr.

    Use the two-letter ICAO country code, e.g. `us` for the United States.
    """

    emby_legacy: EmbyLegacyMetadata = EmbyLegacyMetadata()
    kodi_emby: KodiEmbyMetadata = KodiEmbyMetadata()
    roksbox: RoksboxMetadata = RoksboxMetadata()
    wdtv: WdtvMetadata = WdtvMetadata()

    _remote_map: List[RemoteMapEntry] = [("certification_country", "certificationCountry", {})]

    @classmethod
    def from_remote(cls, secrets: RadarrSecrets) -> Self:
        with radarr_api_client(secrets=secrets) as api_client:
            api_config = radarr.MetadataConfigApi(api_client).get_metadata_config()
            metadata_api = radarr.MetadataApi(api_client)
            api_metadata_schemas: Dict[str, radarr.MetadataResource] = {
                api_schema.implementation: api_schema
                for api_schema in metadata_api.list_metadata_schema()
            }
            api_metadatas: Dict[str, radarr.MetadataResource] = {
                api_metadata.implementation: api_metadata
                for api_metadata in metadata_api.list_metadata()
            }
        if EmbyLegacyMetadata._implementation not in api_metadatas:
            raise RuntimeError(
                "Unable to find Emby (Legacy) metadata on Radarr, database might be corrupt",
            )
        if KodiEmbyMetadata._implementation not in api_metadatas:
            raise RuntimeError(
                "Unable to find Kodi (XBMC)/Emby metadata on Radarr, database might be corrupt",
            )
        if RoksboxMetadata._implementation not in api_metadatas:
            raise RuntimeError(
                "Unable to find Roksbox metadata on Radarr, database might be corrupt",
            )
        if WdtvMetadata._implementation not in api_metadatas:
            raise RuntimeError(
                "Unable to find WDTV metadata on Radarr, database might be corrupt",
            )
        return cls(
            **cls.get_local_attrs(remote_map=cls._remote_map, remote_attrs=api_config.to_dict()),
            emby_legacy=EmbyLegacyMetadata._from_remote(
                api_schema=api_metadata_schemas[EmbyLegacyMetadata._implementation],
                api_metadata=api_metadatas[EmbyLegacyMetadata._implementation],
            ),
            kodi_emby=KodiEmbyMetadata._from_remote(
                api_schema=api_metadata_schemas[KodiEmbyMetadata._implementation],
                api_metadata=api_metadatas[KodiEmbyMetadata._implementation],
            ),
            roksbox=RoksboxMetadata._from_remote(
                api_schema=api_metadata_schemas[RoksboxMetadata._implementation],
                api_metadata=api_metadatas[RoksboxMetadata._implementation],
            ),
            wdtv=WdtvMetadata._from_remote(
                api_schema=api_metadata_schemas[WdtvMetadata._implementation],
                api_metadata=api_metadatas[WdtvMetadata._implementation],
            ),
        )

    def update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        with radarr_api_client(secrets=secrets) as api_client:
            api_config = radarr.MetadataConfigApi(api_client).get_metadata_config()
            metadata_api = radarr.MetadataApi(api_client)
            api_metadata_schemas: Dict[str, radarr.MetadataResource] = {
                api_schema.implementation: api_schema
                for api_schema in metadata_api.list_metadata_schema()
            }
            api_metadatas: Dict[str, radarr.MetadataResource] = {
                api_metadata.implementation: api_metadata
                for api_metadata in metadata_api.list_metadata()
            }
        if EmbyLegacyMetadata._implementation not in api_metadatas:
            raise RuntimeError(
                "Unable to find Emby (Legacy) metadata on Radarr, database might be corrupt",
            )
        if KodiEmbyMetadata._implementation not in api_metadatas:
            raise RuntimeError(
                "Unable to find Kodi (XBMC)/Emby metadata on Radarr, database might be corrupt",
            )
        if RoksboxMetadata._implementation not in api_metadatas:
            raise RuntimeError(
                "Unable to find Roksbox metadata on Radarr, database might be corrupt",
            )
        if WdtvMetadata._implementation not in api_metadatas:
            raise RuntimeError(
                "Unable to find WDTV metadata on Radarr, database might be corrupt",
            )
        config_changed, config_changed_attrs = self.get_update_remote_attrs(
            tree=tree,
            remote=remote,
            remote_map=self._remote_map,
            check_unmanaged=check_unmanaged,
        )
        if config_changed:
            with radarr_api_client(secrets=secrets) as api_client:
                radarr.MetadataConfigApi(api_client).update_metadata_config(
                    id=str(api_config.id),
                    metadata_config_resource=radarr.MetadataConfigResource.from_dict(
                        {**api_config.to_dict(), **config_changed_attrs},
                    ),
                )
        return any(
            [
                config_changed,
                self.emby_legacy._update_remote(
                    tree=f"{tree}.emby_legacy",
                    secrets=secrets,
                    remote=remote.emby_legacy,
                    api_schema=api_metadata_schemas[EmbyLegacyMetadata._implementation],
                    api_metadata=api_metadatas[EmbyLegacyMetadata._implementation],
                    check_unmanaged=check_unmanaged,
                ),
                self.kodi_emby._update_remote(
                    tree=f"{tree}.kodi_emby",
                    secrets=secrets,
                    remote=remote.kodi_emby,
                    api_schema=api_metadata_schemas[KodiEmbyMetadata._implementation],
                    api_metadata=api_metadatas[KodiEmbyMetadata._implementation],
                    check_unmanaged=check_unmanaged,
                ),
                self.roksbox._update_remote(
                    tree=f"{tree}.roksbox",
                    secrets=secrets,
                    remote=remote.roksbox,
                    api_schema=api_metadata_schemas[RoksboxMetadata._implementation],
                    api_metadata=api_metadatas[RoksboxMetadata._implementation],
                    check_unmanaged=check_unmanaged,
                ),
                self.wdtv._update_remote(
                    tree=f"{tree}.wdtv",
                    secrets=secrets,
                    remote=remote.wdtv,
                    api_schema=api_metadata_schemas[WdtvMetadata._implementation],
                    api_metadata=api_metadatas[WdtvMetadata._implementation],
                    check_unmanaged=check_unmanaged,
                ),
            ],
        )
