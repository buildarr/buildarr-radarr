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
Radarr plugin notification connection configuration.
"""


from __future__ import annotations

from logging import getLogger
from typing import Any, Dict, List, Literal, Mapping, Optional, Set, Tuple, Type, Union

import radarr

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr, Password, Port
from pydantic import AnyHttpUrl, ConstrainedInt, Field, NameEmail, SecretStr
from typing_extensions import Annotated, Self

from ....api import radarr_api_client
from ....secrets import RadarrSecrets
from ...types import RadarrConfigBase

logger = getLogger(__name__)


class NotificationTriggers(RadarrConfigBase):
    """
    Notification connections are configured using the following syntax.

    ```yaml
    radarr:
      settings:
        notifications:
          delete_unmanaged: false # Optional
          definitions:
            Email: # Name of notification connection in Radarr.
              type: "email" # Required
              notification_triggers: # When to send notifications.
                on_health_issue: true
                include_health_warnings: false # Do not send on just warnings.
                on_application_update: true
              tags: # Tags can also be assigned to connections.
                - "example"
              # Connection-specific parameters.
              server: "smtp.example.com"
              port: 465
              use_encryption: true
              username: "radarr"
              password: "fake-password"
              from_address: "radarr@example.com"
              recipient_addresses:
                - "admin@example.com"
            # Add additional connections here.
    ```

    A `type` attribute must be defined so Buildarr knows what type of connection to make.
    Each connection has a unique value for `type` documented below.

    The triggers enabled on a connection are defined under `notification_triggers`.
    Tags can be assigned to connections, to only allow notifications relating
    to media under those tags.

    The `delete_unmanaged` flag on the outer `connect` block can be set
    to remove connections not defined in Buildarr.
    Take care when using this option, as it can remove connections
    automatically managed by other applications.

    The following notification triggers can be enabled.
    Some connection types only allow a subset of these to be enabled,
    check the documentation the specific connection type for more information.
    """

    on_health_issue: bool = False
    """
    Be notified on health check failures.
    """

    include_health_warnings: bool = False
    """
    Be notified on health warnings in addition to errors.

    Requires `on_health_issue` to be enabled to have any effect.
    """

    on_application_update: bool = False
    """
    Be notified when Radarr gets updated to a new version.
    """

    _remote_map: List[RemoteMapEntry] = [
        ("on_health_issue", "onHealthIssue", {}),
        ("include_health_warnings", "includeHealthWarnings", {}),
        ("on_application_update", "onApplicationUpdate", {}),
    ]


class Notification(RadarrConfigBase):
    """
    Base class for a Radarr notification connection.
    """

    notification_triggers: NotificationTriggers = NotificationTriggers()
    """
    Notification triggers to enable on this notification connection.
    """

    tags: List[NonEmptyStr] = []
    """
    Radarr tags to associate this notification connection with.
    """

    _implementation: str
    _remote_map: List[RemoteMapEntry]

    @classmethod
    def _get_base_remote_map(
        cls,
        tag_ids: Mapping[str, int],
    ) -> List[RemoteMapEntry]:
        return [
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
            notification_triggers=NotificationTriggers(
                **NotificationTriggers.get_local_attrs(
                    remote_map=NotificationTriggers._remote_map,
                    remote_attrs=remote_attrs,
                ),
            ),
            **cls.get_local_attrs(
                remote_map=cls._get_base_remote_map(tag_ids) + cls._remote_map,
                remote_attrs=remote_attrs,
            ),
        )

    def _get_api_schema(self, schemas: List[radarr.NotificationResource]) -> Dict[str, Any]:
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
        api_notification_schemas: List[radarr.NotificationResource],
        tag_ids: Mapping[str, int],
        notification_name: str,
    ) -> None:
        api_schema = self._get_api_schema(api_notification_schemas)
        set_attrs = {
            **self.notification_triggers.get_create_remote_attrs(
                tree=f"{tree}.notification_triggers",
                remote_map=self.notification_triggers._remote_map,
            ),
            **self.get_create_remote_attrs(
                tree=tree,
                remote_map=self._get_base_remote_map(tag_ids) + self._remote_map,
            ),
        }
        field_values: Dict[str, Any] = {
            field["name"]: field["value"] for field in set_attrs["fields"]
        }
        set_attrs["fields"] = [
            ({**f, "value": field_values[f["name"]]} if f["name"] in field_values else f)
            for f in api_schema["fields"]
        ]
        remote_attrs = {"name": notification_name, **api_schema, **set_attrs}
        with radarr_api_client(secrets=secrets) as api_client:
            radarr.NotificationApi(api_client).create_notification(
                notification_resource=radarr.NotificationResource.from_dict(remote_attrs),
            )

    def _update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        api_notification_schemas: List[radarr.NotificationResource],
        tag_ids: Mapping[str, int],
        api_notification: radarr.NotificationResource,
    ) -> bool:
        (
            triggers_updated,
            updated_triggers_attrs,
        ) = self.notification_triggers.get_update_remote_attrs(
            tree=tree,
            remote=remote.notification_triggers,
            remote_map=self.notification_triggers._remote_map,
        )
        base_updated, updated_base_attrs = self.get_update_remote_attrs(
            tree=tree,
            remote=remote,
            remote_map=self._get_base_remote_map(tag_ids) + self._remote_map,
        )
        if triggers_updated or base_updated:
            api_schema = self._get_api_schema(api_notification_schemas)
            api_notification_dict = api_notification.to_dict()
            updated_attrs = {**updated_triggers_attrs, **updated_base_attrs}
            if "fields" in updated_attrs:
                updated_field_values: Dict[str, Any] = {
                    field["name"]: field["value"] for field in updated_attrs["fields"]
                }
                remote_fields: Dict[str, Dict[str, Any]] = {
                    field["name"]: field for field in api_notification_dict["fields"]
                }
                updated_attrs["fields"] = [
                    (
                        {
                            **remote_fields[f["name"]],
                            "value": updated_field_values[f["name"]],
                        }
                        if f["name"] in updated_field_values
                        else remote_fields[f["name"]]
                    )
                    for f in api_schema["fields"]
                ]
            remote_attrs = {**api_notification_dict, **updated_attrs}
            with radarr_api_client(secrets=secrets) as api_client:
                radarr.NotificationApi(api_client).update_notification(
                    id=str(api_notification.id),
                    notification_resource=radarr.NotificationResource.from_dict(remote_attrs),
                )
            return True
        return False

    def _delete_remote(self, secrets: RadarrSecrets, notification_id: int) -> None:
        with radarr_api_client(secrets=secrets) as api_client:
            radarr.NotificationApi(api_client).delete_notification(id=notification_id)
