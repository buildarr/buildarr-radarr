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
Download client configuration base class.
"""


from __future__ import annotations

from logging import getLogger
from typing import Any, Dict, List, Mapping, Set

import radarr

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr
from pydantic import PositiveInt
from typing_extensions import Self

from ....api import radarr_api_client
from ....secrets import RadarrSecrets
from ...types import RadarrConfigBase

logger = getLogger(__name__)


class DownloadClient(RadarrConfigBase):
    """
    Download clients are defined using the following format.
    Here is an example of a Transmission download client being configured.

    ```yaml
    ---

    radarr:
      settings:
        download_clients:
          definitions:
            Transmission: # Name of the download client
              type: "transmission" # Type of download client
              enable: true # Enable the download client in Radarr
              host: "transmission"
              port: 9091
              category: "radarr"
              # Define any other type-specific or global
              # download client attributes as needed.
    ```

    Every download client definition must have the correct `type` value defined,
    to tell Buildarr what type of download client to configure.
    The name of the download client definition is just a name, and has no meaning.

    `enable` can be set to `False` to keep the download client configured on Radarr,
    but disabled so that it is inactive.

    The below attributes can be defined on any type of download client.
    """

    enable: bool = True
    """
    When `True`, this download client is active and Radarr is able to send requests to it.
    """

    priority: PositiveInt = 1
    """
    Download client priority.

    Clients with a lower value are prioritised.
    Round-robin is used for clients with the same priority.
    """

    # removeCompletedDownloads
    remove_completed: bool = True
    """ """

    tags: Set[NonEmptyStr] = set()
    """
    Radarr tags to assign to the download clients.
    Only media under those tags will be assigned to this client.

    If no tags are assigned, all media can use the client.
    """

    _implementation: str
    _remote_map: List[RemoteMapEntry] = []

    @classmethod
    def _get_base_remote_map(cls, tag_ids: Mapping[str, int]) -> List[RemoteMapEntry]:
        return [
            ("enable", "enable", {}),
            ("priority", "priority", {}),
            (
                "tags",
                "tags",
                {
                    "decoder": lambda v: set(
                        (tag for tag, tag_id in tag_ids.items() if tag_id in v),
                    ),
                    "encoder": lambda v: sorted(tag_ids[tag] for tag in v),
                },
            ),
        ]

    @classmethod
    def _from_remote(cls, tag_ids: Mapping[str, int], remote_attrs: Mapping[str, Any]) -> Self:
        return cls(
            **cls.get_local_attrs(
                cls._get_base_remote_map(tag_ids=tag_ids) + cls._remote_map,
                remote_attrs,
            ),
        )

    def _get_api_schema(self, schemas: List[radarr.DownloadClientResource]) -> Dict[str, Any]:
        return {
            k: v
            for k, v in next(
                s for s in schemas if s.implementation.lower() == self._implementation.lower()
            )
            .to_dict()
            .items()
            if k not in ["id", "name"]
        }

    def _create_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        api_downloadclient_schemas: List[radarr.DownloadClientResource],
        tag_ids: Mapping[str, int],
        downloadclient_name: str,
    ) -> None:
        api_schema = self._get_api_schema(api_downloadclient_schemas)
        set_attrs = self.get_create_remote_attrs(
            tree=tree,
            remote_map=self._get_base_remote_map(tag_ids=tag_ids) + self._remote_map,
        )
        field_values: Dict[str, Any] = {
            field["name"]: field["value"] for field in set_attrs["fields"]
        }
        set_attrs["fields"] = [
            ({**f, "value": field_values[f["name"]]} if f["name"] in field_values else f)
            for f in api_schema["fields"]
        ]
        remote_attrs = {"name": downloadclient_name, **api_schema, **set_attrs}
        with radarr_api_client(secrets=secrets) as api_client:
            radarr.DownloadClientApi(api_client).create_download_client(
                download_client_resource=radarr.DownloadClientResource.from_dict(remote_attrs),
            )

    def _update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        tag_ids: Mapping[str, int],
        api_downloadclient: radarr.DownloadClientResource,
    ) -> bool:
        updated, updated_attrs = self.get_update_remote_attrs(
            tree=tree,
            remote=remote,
            remote_map=self._get_base_remote_map(tag_ids=tag_ids) + self._remote_map,
            set_unchanged=True,
        )
        if updated:
            if "fields" in updated_attrs:
                updated_fields: Dict[str, Any] = {
                    field["name"]: field["value"] for field in updated_attrs["fields"]
                }
                updated_attrs["fields"] = [
                    (
                        {**f, "value": updated_fields[f["name"]]}
                        if f["name"] in updated_fields
                        else f
                    )
                    for f in api_downloadclient.to_dict()["fields"]
                ]
            remote_attrs = {**api_downloadclient.to_dict(), **updated_attrs}
            with radarr_api_client(secrets=secrets) as api_client:
                radarr.DownloadClientApi(api_client).update_download_client(
                    id=str(api_downloadclient.id),
                    download_client_resource=radarr.DownloadClientResource.from_dict(
                        remote_attrs,
                    ),
                )
            return True
        return False

    def _delete_remote(self, secrets: RadarrSecrets, downloadclient_id: int) -> None:
        with radarr_api_client(secrets=secrets) as api_client:
            radarr.DownloadClientApi(api_client).delete_download_client(id=downloadclient_id)
