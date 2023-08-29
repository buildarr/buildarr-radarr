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
Prowlarr plugin notification connection configuration.
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
from ...secrets import ProwlarrSecrets
from ..types import ProwlarrConfigBase


class BoxcarNotification(Notification):
    """
    Receive media update and health alert push notifications via Boxcar.
    """

    type: Literal["boxcar"] = "boxcar"
    """
    Type value associated with this kind of connection.
    """

    access_token: Password
    """
    Access token for authenticating with Boxcar.
    """

    _implementation: str = "Boxcar"
    _remote_map: List[RemoteMapEntry] = [("access_token", "token", {"is_field": True})]


class CustomscriptNotification(Notification):
    """
    Execute a local script on the Prowlarr instance when events occur.
    """

    type: Literal["customscript"] = "customscript"
    """
    Type value associated with this kind of connection.
    """

    path: NonEmptyStr
    """
    Path of the script to execute.
    """

    _implementation: str = "CustomScript"
    _remote_map: List[RemoteMapEntry] = [("path", "path", {"is_field": True})]


class DiscordNotification(Notification):
    """
    Send media update and health alert messages to a Discord server.
    """

    type: Literal["discord"] = "discord"
    """
    Type value associated with this kind of connection.
    """

    webhook_url: AnyHttpUrl
    """
    Discord server webhook URL.
    """

    username: Optional[str] = None
    """
    The username to post as.

    If unset, blank or set to `None`, use the default username set to the webhook URL.
    """

    avatar: Optional[str] = None
    """
    Change the avatar that is used for messages from this connection.

    If unset, blank or set to `None`, use the default avatar for the user.
    """

    # Name override, None -> use machine_name
    host: Optional[str] = None
    """
    Override the host name that shows for this notification.

    If unset, blank or set to `None`, use the machine name.
    """

    on_grab_fields: Set[OnGrabField] = {
        OnGrabField.overview,
        OnGrabField.rating,
        OnGrabField.genres,
        OnGrabField.quality,
        OnGrabField.size,
        OnGrabField.links,
        OnGrabField.release,
        OnGrabField.poster,
        OnGrabField.fanart,
    }
    """
    Set the fields that are passed in for this 'on grab' notification.
    By default, all fields are passed in.

    Values:

    * `overview`
    * `rating`
    * `genres`
    * `quality`
    * `group`
    * `size`
    * `links`
    * `release`
    * `poster`
    * `fanart`

    Example:

    ```yaml
    ...
      connect:
        definitions:
          Discord:
            type: "discord"
            webhook_url: "https://..."
            on_grab_fields:
              - "overview"
              - "quality"
              - "release"
    ```
    """

    on_import_fields: Set[OnImportField] = {
        OnImportField.overview,
        OnImportField.rating,
        OnImportField.genres,
        OnImportField.quality,
        OnImportField.codecs,
        OnImportField.group,
        OnImportField.size,
        OnImportField.languages,
        OnImportField.subtitles,
        OnImportField.links,
        OnImportField.release,
        OnImportField.poster,
        OnImportField.fanart,
    }
    """
    Set the fields that are passed in for this 'on import' notification.
    By default, all fields are passed in.

    Values:

    * `overview`
    * `rating`
    * `genres`
    * `quality`
    * `codecs`
    * `group`
    * `size`
    * `languages`
    * `subtitles`
    * `links`
    * `release`
    * `poster`
    * `fanart`

    Example:

    ```yaml
    ...
      connect:
        definitions:
          Discord:
            type: "discord"
            webhook_url: "https://..."
            on_import_fields:
              - "overview"
              - "quality"
              - "release"
    ```
    """

    _implementation: str = "Discord"
    _remote_map: List[RemoteMapEntry] = [
        ("webhook_url", "webHookUrl", {"is_field": True}),
        (
            "username",
            "username",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        (
            "avatar",
            "avatar",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        (
            "host",
            "host",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        (
            "on_grab_fields",
            "grabFields",
            {"is_field": True, "encoder": lambda v: sorted(f.value for f in v)},
        ),
        (
            "on_import_fields",
            "importFields",
            {"is_field": True, "encoder": lambda v: sorted(f.value for f in v)},
        ),
    ]


class EmailNotification(Notification):
    """
    Send media update and health alert messages to an email address.
    """

    type: Literal["email"] = "email"
    """
    Type value associated with this kind of connection.
    """

    server: NonEmptyStr
    """
    Hostname or IP address of the SMTP server to send outbound mail to.
    """

    port: Port = 587  # type: ignore[assignment]
    """
    The port number on the SMTP server to use to submit mail.

    The default is to use STARTTLS on the standard SMTP submission port.
    """

    use_encryption: bool = True
    """
    Whether or not to use encryption when sending mail to the SMTP server.

    If the port number is set to 465, SMTPS (implicit TLS) will be used.
    Any other port number will result in STARTTLS being used.

    The default is to enable encryption.
    """

    username: NonEmptyStr
    """
    SMTP username of the account to send the mail from.
    """

    password: Password
    """
    SMTP password of the account to send the mail from.
    """

    from_address: NameEmail
    """
    Email address to send the mail as.

    RFC-5322 formatted mailbox addresses are also supported,
    e.g. `Prowlarr Notifications <prowlarr@example.com>`.
    """

    recipient_addresses: Annotated[List[NameEmail], Field(min_items=1, unique_items=True)]
    """
    List of email addresses to directly address the mail to.

    At least one address must be provided.
    """

    cc_addresses: Annotated[List[NameEmail], Field(unique_items=True)] = []
    """
    Optional list of email addresses to copy (CC) the mail to.
    """

    bcc_addresses: Annotated[List[NameEmail], Field(unique_items=True)] = []
    """
    Optional list of email addresses to blind copy (BCC) the mail to.
    """

    _implementation: str = "Email"
    _remote_map: List[RemoteMapEntry] = [
        ("server", "server", {"is_field": True}),
        ("port", "port", {"is_field": True}),
        ("use_encryption", "requireEncryption", {"is_field": True}),
        ("username", "username", {"is_field": True}),
        ("password", "password", {"is_field": True}),
        ("from_address", "from", {"is_field": True}),
        ("recipient_addresses", "to", {"is_field": True}),
        ("cc_addresses", "cc", {"is_field": True}),
        ("bcc_addresses", "bcc", {"is_field": True}),
    ]


class GotifyNotification(Notification):
    """
    Send media update and health alert push notifications via a Gotify server.
    """

    type: Literal["gotify"] = "gotify"
    """
    Type value associated with this kind of connection.
    """

    server: AnyHttpUrl
    """
    Gotify server URL. (e.g. `http://gotify.example.com:1234`)
    """

    app_token: Password
    """
    App token to use to authenticate with Gotify.
    """

    priority: GotifyPriority = GotifyPriority.normal
    """
    Gotify notification priority.

    Values:

    * `min`
    * `low`
    * `normal`
    * `high`
    """

    _implementation: str = "Gotify"
    _remote_map: List[RemoteMapEntry] = [
        ("server", "server", {"is_field": True}),
        ("app_token", "appToken", {"is_field": True}),
        ("priority", "priority", {"is_field": True}),
    ]


class JoinNotification(Notification):
    """
    Send media update and health alert push notifications via Join.
    """

    type: Literal["join"] = "join"
    """
    Type value associated with this kind of connection.
    """

    api_key: Password
    """
    API key to use to authenticate with Join.
    """

    # Deprecated, only uncomment if absolutely required by Prowlarr
    # device_ids: Set[int] = set()

    device_names: Set[NonEmptyStr] = set()
    """
    List of full or partial device names you'd like to send notifications to.

    If unset or empty, all devices will receive notifications.
    """

    priority: JoinPriority = JoinPriority.normal
    """
    Join push notification priority.

    Values:

    * `silent`
    * `quiet`
    * `normal`
    * `high`
    * `emergency`
    """

    _implementation: str = "Join"
    _remote_map: List[RemoteMapEntry] = [
        ("api_key", "apiKey", {"is_field": True}),
        # ("device_ids", "deviceIds", {"is_field": True}),
        (
            "device_names",
            "deviceNames",
            {
                "is_field": True,
                "decoder": lambda v: (
                    set(d.strip() for d in v.split(",")) if v and v.strip() else set()
                ),
                "encoder": lambda v: ",".join(sorted(v)) if v else "",
            },
        ),
        ("priority", "priority", {"is_field": True}),
    ]


class MailgunNotification(Notification):
    """
    Send media update and health alert emails via the Mailgun delivery service.
    """

    type: Literal["mailgun"] = "mailgun"
    """
    Type value associated with this kind of connection.
    """

    api_key: Password
    """
    API key to use to authenticate with Mailgun.
    """

    use_eu_endpoint: bool = False
    """
    Send mail via the EU endpoint instead of the US one.
    """

    from_address: NameEmail
    """
    Email address to send the mail as.

    RFC-5322 formatted mailbox addresses are also supported,
    e.g. `Sonarr Notifications <sonarr@example.com>`.
    """

    sender_domain: NonEmptyStr
    """
    The domain from which the mail will be sent.
    """

    recipient_addresses: Annotated[List[NameEmail], Field(min_items=1, unique_items=True)]
    """
    The recipient email addresses of the notification mail.

    At least one recipient address is required.
    """

    _implementation: str = "Mailgun"
    _remote_map: List[RemoteMapEntry] = [
        ("api_key", "apiKey", {"is_field": True}),
        ("use_eu_endpoint", "useEuEndpoint", {"is_field": True}),
        ("from_address", "from", {"is_field": True}),
        ("sender_domain", "senderDomain", {"is_field": True}),
        ("recipient_addresses", "recipients", {"is_field": True}),
    ]


class NotifiarrNotification(Notification):
    """
    Send media update and health alert emails via the Notifiarr notification service.
    """

    type: Literal["notifiarr"] = "notifiarr"
    """
    Type value associated with this kind of connection.
    """

    api_key: Password
    """
    API key to use to authenticate with Notifiarr.
    """

    _implementation: str = "Notifiarr"
    _remote_map: List[RemoteMapEntry] = [("api_key", "apiKey", {"is_field": True})]


class NtfyNotification(Notification):
    """
    Send media update and health alert emails via the ntfy.sh notification service,
    or a self-hosted server using the same software.
    """

    type: Literal["ntfy"] = "ntfy"
    """
    Type value associated with this kind of connection.
    """

    server_url: Optional[AnyHttpUrl] = None
    """
    Custom ntfy server URL.

    Leave blank, set to `null` or undefined to use the public server (`https://ntfy.sh`).
    """

    username: Optional[str] = None
    """
    Username to use to authenticate, if required.
    """

    password: Optional[SecretStr] = None
    """
    Password to use to authenticate, if required.
    """

    priority: NtfyshPriority = NtfyshPriority.default
    """
    Values:

    * `min`
    * `low`
    * `default`
    * `high`
    * `max`
    """

    topics: Set[NonEmptyStr] = set()
    """
    List of Topics to send notifications to.
    """

    ntfy_tags: Set[NonEmptyStr] = set()
    """
    Optional list of tags or [emojis](https://ntfy.sh/docs/emojis) to use.
    """

    click_url: Optional[AnyHttpUrl] = None
    """
    Optional link for when the user clicks the notification.
    """

    _implementation: str = "Ntfy"
    _remote_map: List[RemoteMapEntry] = [
        (
            "server_url",
            "serverUrl",
            {
                "is_field": True,
                "decoder": lambda v: v or None,
                "encoder": lambda v: str(v) if v else "",
            },
        ),
        (
            "username",
            "userName",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        (
            "password",
            "password",
            {
                "is_field": True,
                "decoder": lambda v: SecretStr(v) if v else None,
                "encoder": lambda v: v.get_secret_value() if v else "",
            },
        ),
        ("priority", "priority", {"is_field": True}),
        ("topics", "topics", {"is_field": True, "encoder": sorted}),
        ("ntfy_tags", "tags", {"is_field": True, "encoder": sorted}),
        (
            "click_url",
            "clickUrl",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
    ]


class ProwlNotification(Notification):
    """
    Send media update and health alert push notifications to a Prowl client.
    """

    type: Literal["prowl"] = "prowl"
    """
    Type value associated with this kind of connection.
    """

    api_key: Password
    """
    API key to use when authenticating with Prowl.
    """

    priority: ProwlPriority = ProwlPriority.normal
    """
    Prowl push notification priority.

    Values:

    * `verylow`
    * `low`
    * `normal`
    * `high`
    * `emergency`
    """

    _implementation: str = "Prowl"
    _remote_map: List[RemoteMapEntry] = [
        ("api_key", "apiKey", {"is_field": True}),
        ("priority", "priority", {"is_field": True}),
    ]


class PushbulletNotification(Notification):
    """
    Send media update and health alert push notifications to 1 or more Pushbullet devices.
    """

    type: Literal["pushbullet"] = "pushbullet"
    """
    Type value associated with this kind of connection.
    """

    api_key: Password
    """
    API key to use when authenticating with Pushbullet.
    """

    device_ids: List[NonEmptyStr] = []
    """
    List of device IDs to send notifications to.

    If unset or empty, send to all devices.
    """

    channel_tags: List[NonEmptyStr] = []
    """
    List of Channel Tags to send notifications to.
    """

    sender_id: Optional[str] = None
    """
    The device ID to send notifications from
    (`device_iden` in the device's URL on [pushbullet.com](https://pushbullet.com)).

    Leave unset, blank or set to `None` to send from yourself.
    """

    _implementation: str = "Pushbullet"
    _remote_map: List[RemoteMapEntry] = [
        ("api_key", "apiKey", {"is_field": True}),
        ("device_ids", "deviceIds", {"is_field": True}),
        ("channel_tags", "channelTags", {"is_field": True}),
        (
            "sender_id",
            "senderId",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
    ]


class PushoverNotification(Notification):
    """
    Send media update and health alert push notifications to 1 or more Pushover devices.
    """

    type: Literal["pushover"] = "pushover"
    """
    Type value associated with this kind of connection.
    """

    user_key: Annotated[SecretStr, Field(min_length=30, max_length=30)]
    """
    User key to use to authenticate with your Pushover account.
    """

    api_key: Annotated[SecretStr, Field(min_length=30, max_length=30)]
    """
    API key assigned to Prowlarr in Pushover.
    """

    devices: Set[NonEmptyStr] = set()
    """
    List of device names to send notifications to.

    If unset or empty, send to all devices.
    """

    priority: PushoverPriority = PushoverPriority.normal
    """
    Pushover push notification priority.

    Values:

    * `silent`
    * `quiet`
    * `normal`
    * `high`
    * `emergency`
    """

    retry: Union[Literal[0], PushoverRetry] = 0
    """
    Interval to retry emergency alerts, in seconds.

    Minimum 30 seconds. Set to 0 to disable retrying emergency alerts.
    """

    # TODO: Enforce "expire > retry if retry > 0" constraint
    expire: int = Field(0, ge=0, le=86400)
    """
    Threshold for retrying emergency alerts, in seconds.
    If `retry` is set, this should be set to a higher value.

    Maximum 86400 seconds (1 day).
    """

    sound: Optional[str] = None
    """
    Notification sound to use on devices.

    Leave unset, blank or set to `None` to use the default.
    """

    _implementation: str = "Pushover"
    _remote_map: List[RemoteMapEntry] = [
        ("user_key", "userKey", {"is_field": True}),
        ("api_key", "apiKey", {"is_field": True}),
        ("devices", "devices", {"is_field": True, "encoder": lambda v: sorted(v)}),
        ("priority", "priority", {"is_field": True}),
        ("retry", "retry", {"is_field": True}),
        ("expire", "expire", {"is_field": True}),
        (
            "sound",
            "sound",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
    ]


class SendgridNotification(Notification):
    """
    Send media update and health alert emails via the SendGrid delivery service.
    """

    type: Literal["sendgrid"] = "sendgrid"
    """
    Type value associated with this kind of connection.
    """

    api_key: Password
    """
    API key to use to authenticate with SendGrid.
    """

    from_address: NameEmail
    """
    Email address to send the mail as.

    RFC-5322 formatted mailbox addresses are also supported,
    e.g. `Prowlarr Notifications <prowlarr@example.com>`.
    """

    recipient_addresses: Annotated[List[NameEmail], Field(min_items=1, unique_items=True)]
    """
    The recipient email addresses of the notification mail.

    At least one recipient address is required.
    """

    _implementation: str = "SendGrid"
    _remote_map: List[RemoteMapEntry] = [
        ("api_key", "apiKey", {"is_field": True}),
        ("from_address", "from", {"is_field": True}),
        ("recipient_addresses", "recipients", {"is_field": True}),
    ]


class SlackNotification(Notification):
    """
    Send media update and health alert messages to a Slack channel.
    """

    type: Literal["slack"] = "slack"
    """
    Type value associated with this kind of connection.
    """

    webhook_url: AnyHttpUrl
    """
    Webhook URL for the Slack channel to send to.
    """

    username: NonEmptyStr
    """
    Username to post as.
    """

    icon: Optional[str] = None
    """
    The icon that is used for messages from this integration (emoji or URL).

    If unset, blank or set to `None`, use the default for the user.
    """

    channel: Optional[str] = None
    """
    If set, overrides the default channel in the webhook.
    """

    _implementation: str = "Slack"
    _remote_map: List[RemoteMapEntry] = [
        ("webhook_url", "webHookUrl", {"is_field": True}),
        ("username", "username", {"is_field": True}),
        (
            "icon",
            "icon",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        (
            "channel",
            "channel",
            {"is_field": True, "decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
    ]


class TelegramNotification(Notification):
    """
    Send media update and health alert messages to a Telegram chat room.
    """

    type: Literal["telegram"] = "telegram"
    """
    Type value associated with this kind of connection.
    """

    bot_token: Password
    """
    The bot token assigned to the Prowlarr instance.
    """

    chat_id: NonEmptyStr
    """
    The ID of the chat room to send messages to.

    You must start a conversation with the bot or add it to your group to receive messages.
    """

    send_silently: bool = False
    """
    Sends the message silently. Users will receive a notification with no sound.
    """

    _implementation: str = "Telegram"
    _remote_map: List[RemoteMapEntry] = [
        ("bot_token", "botToken", {"is_field": True}),
        ("chat_id", "chatId", {"is_field": True}),
        ("send_silently", "sendSilently", {"is_field": True}),
    ]
