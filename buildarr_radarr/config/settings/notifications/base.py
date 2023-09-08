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
Notification connection configuration base class.
"""


from __future__ import annotations

from logging import getLogger
from typing import Any, Dict, List, Mapping, Set

import radarr

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr
from typing_extensions import Self

from ....api import radarr_api_client
from ....secrets import RadarrSecrets
from ...types import RadarrConfigBase

logger = getLogger(__name__)


class NotificationTriggers(RadarrConfigBase):
    # Notification trigger configuration.

    on_grab: bool = False
    """
    Notify when movies are available for download and have been sent to a download client.
    """

    on_import: bool = False
    """
    Notify when movies are successfully imported (downloaded).
    """

    on_upgrade: bool = False
    """
    Notify when movies are upgraded to a better quality.
    """

    on_rename: bool = False
    """
    Notify when movies are renamed.
    """

    on_movie_added: bool = False
    """
    Notify when movies are added to Radarr's library to monitor.
    """

    on_movie_delete: bool = False
    """
    Notify when movies are deleted.
    """

    on_movie_file_delete: bool = False
    """
    Notify when movie files are deleted.
    """

    on_movie_file_delete_for_upgrade: bool = False
    """
    Notify when movie files are deleted for upgrades.
    """

    on_health_issue: bool = False
    """
    Notify on health check failures.
    """

    include_health_warnings: bool = False
    """
    When `on_health_issue` is enabled, notify for health check warnings in addition to errors.
    """

    on_health_restored: bool = False
    """
    Notify when health check failures have been resolved.
    """

    on_application_update: bool = False
    """
    Notify when Radarr gets updated to a new version.
    """

    on_manual_interaction_required: bool = False
    """
    Notify when manual interaction is required to resolve an issue.
    """

    _remote_map: List[RemoteMapEntry] = [
        ("on_grab", "onGrab", {}),
        ("on_import", "onDownload", {}),
        ("on_upgrade", "onUpgrade", {}),
        ("on_rename", "onRename", {}),
        ("on_movie_added", "onMovieAdded", {}),
        ("on_movie_delete", "onMovieDelete", {}),
        ("on_movie_file_delete", "onMovieFileDelete", {}),
        ("on_movie_file_delete_for_upgrade", "onMovieFileDeleteForUpgrade", {}),
        ("on_health_issue", "onHealthIssue", {}),
        ("include_health_warnings", "includeHealthWarnings", {}),
        ("on_health_restored", "onHealthRestored", {}),
        ("on_manual_interaction_required", "onManualInteractionRequired", {}),
        ("on_application_update", "onApplicationUpdate", {}),
    ]

    # TODO: Add a post_init_render to check if triggers are supported or not,
    # and force to False (and log a warning) if not.


class Notification(RadarrConfigBase):
    # Notification connection configuration base class.

    notification_triggers: NotificationTriggers = NotificationTriggers()
    """
    Notification triggers to enable on this notification connection.
    """

    tags: Set[NonEmptyStr] = set()
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
