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

import prowlarr

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr, Password, Port
from pydantic import AnyHttpUrl, ConstrainedInt, Field, NameEmail, SecretStr
from typing_extensions import Annotated, Self

from ...api import prowlarr_api_client
from ...secrets import RadarrSecrets
from ..types import RadarrConfigBase

logger = getLogger(__name__)


NotificationType = Union[
    AppriseNotification,
    BoxcarNotification,
    CustomscriptNotification,
    DiscordNotification,
    EmailNotification,
    GotifyNotification,
    JoinNotification,
    MailgunNotification,
    NotifiarrNotification,
    NtfyNotification,
    ProwlNotification,
    PushbulletNotification,
    PushoverNotification,
    SendgridNotification,
    SlackNotification,
    TelegramNotification,
    TwitterNotification,
    WebhookNotification,
]

NOTIFICATION_TYPE_MAP: Dict[str, Type[Notification]] = {
    notification_type._implementation.lower(): notification_type
    for notification_type in (
        AppriseNotification,
        BoxcarNotification,
        CustomscriptNotification,
        DiscordNotification,
        EmailNotification,
        GotifyNotification,
        JoinNotification,
        MailgunNotification,
        NotifiarrNotification,
        NtfyNotification,
        ProwlNotification,
        PushbulletNotification,
        PushoverNotification,
        SendgridNotification,
        SlackNotification,
        TelegramNotification,
        TwitterNotification,
        WebhookNotification,
    )
}


class RadarrNotificationsSettings(RadarrConfigBase):
    """
    Manage notification connections in Radarr.
    """

    delete_unmanaged: bool = False
    """
    Automatically delete connections not configured in Buildarr.

    Take care when enabling this option, as this can remove connections automatically
    managed by other applications.
    """

    definitions: Dict[str, Annotated[NotificationType, Field(discriminator="type")]] = {}
    """
    Notification connections are defined here.
    """

    @classmethod
    def from_remote(cls, secrets: RadarrSecrets) -> Self:
        with prowlarr_api_client(secrets=secrets) as api_client:
            api_notifications = prowlarr.NotificationApi(api_client).list_notification()
            tag_ids: Dict[str, int] = (
                {tag.label: tag.id for tag in prowlarr.TagApi(api_client).list_tag()}
                if any(api_notification.tags for api_notification in api_notifications)
                else {}
            )
        return cls(
            definitions={
                api_notification.name: NOTIFICATION_TYPE_MAP[
                    api_notification.implementation.lower()
                ]._from_remote(
                    tag_ids=tag_ids,
                    remote_attrs=api_notification.to_dict(),
                )
                for api_notification in api_notifications
            },
        )

    def update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        # Track whether or not any changes have been made on the remote instance.
        changed = False
        # Pull API objects and metadata required during the update operation.
        with prowlarr_api_client(secrets=secrets) as api_client:
            notification_api = prowlarr.NotificationApi(api_client)
            api_notification_schemas = notification_api.list_notification_schema()
            api_notifications: Dict[str, prowlarr.NotificationResource] = {
                api_notification.name: api_notification
                for api_notification in notification_api.list_notification()
            }
            tag_ids: Dict[str, int] = (
                {tag.label: tag.id for tag in prowlarr.TagApi(api_client).list_tag()}
                if any(api_notification.tags for api_notification in self.definitions.values())
                or any(api_notification.tags for api_notification in remote.definitions.values())
                else {}
            )
        # Compare local definitions to their remote equivalent.
        # If a local definition does not exist on the remote, create it.
        # If it does exist on the remote, attempt an an in-place modification,
        # and set the `changed` flag if modifications were made.
        for notification_name, notification in self.definitions.items():
            notification_tree = f"{tree}.definitions[{repr(notification_name)}]"
            if notification_name not in remote.definitions:
                notification._create_remote(
                    tree=notification_tree,
                    secrets=secrets,
                    api_notification_schemas=api_notification_schemas,
                    tag_ids=tag_ids,
                    notification_name=notification_name,
                )
                changed = True
            elif notification._update_remote(
                tree=notification_tree,
                secrets=secrets,
                remote=remote.definitions[notification_name],  # type: ignore[arg-type]
                api_notification_schemas=api_notification_schemas,
                tag_ids=tag_ids,
                api_notification=api_notifications[notification_name],
            ):
                changed = True
        # Return whether or not the remote instance was changed.
        return changed

    def delete_remote(self, tree: str, secrets: RadarrSecrets, remote: Self) -> bool:
        # Track whether or not any changes have been made on the remote instance.
        changed = False
        # Pull API objects and metadata required during the update operation.
        with prowlarr_api_client(secrets=secrets) as api_client:
            notification_ids: Dict[str, int] = {
                api_notification.name: api_notification.id
                for api_notification in prowlarr.NotificationApi(api_client).list_notification()
            }
        # Traverse the remote definitions, and see if there are any remote definitions
        # that do not exist in the local configuration.
        # If `delete_unmanaged` is enabled, delete it from the remote.
        # If `delete_unmanaged` is disabled, just add a log entry acknowledging
        # the existence of the unmanaged definition.
        for notification_name, notification in remote.definitions.items():
            if notification_name not in self.definitions:
                notification_tree = f"{tree}.definitions[{repr(notification_name)}]"
                if self.delete_unmanaged:
                    logger.info("%s: (...) -> (deleted)", notification_tree)
                    notification._delete_remote(
                        secrets=secrets,
                        notification_id=notification_ids[notification_name],
                    )
                    changed = True
                else:
                    logger.debug("%s: (...) (unmanaged)", notification_tree)
        # Return whether or not the remote instance was changed.
        return changed
