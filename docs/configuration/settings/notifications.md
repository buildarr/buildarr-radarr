# Notifications (Connect)

Radarr supports pushing notifications to external applications and services.

The main uses cases for this are:

* Notifying users when media requests have been processed.
* Alerting administrators to issues with the operation of Radarr (e.g. indexers not working).

Notification connections are defined using a dictionary structure, where the name of the
definition becomes the name of the notification connection in Radarr.

```yaml
radarr:
  settings:
    notifications:
      delete_unmanaged: false
      definitions:
        Email:  # Name of notification connection in Radarr.
          type: email  # Required
          notification_triggers:  # When to send notifications.
            on_grab: true
            on_import: true
            on_upgrade: true
            on_rename: false
            on_movie_added: true
            on_movie_delete: true
            on_movie_file_delete: true
            on_movie_file_delete_for_upgrade: true
            on_health_issue: true
            include_health_warnings: true
            on_health_restored: true
            on_manual_interaction_required: true
            on_application_update: true
          # Connection-specific parameters.
          server: smtp.example.com
          port: 465
          use_encryption: true
          username: radarr
          password: fake-password
          from_address: radarr@example.com
          recipient_addresses:
            - admin@example.com
          # Tags can also be assigned to connections.
          tags:
            - anime-movies
        # Add additional connections here.
```

Radarr supports pushing notifications to applications for a variety of different
conditions. The conditions to notify can be configured using *notification triggers*.

Note that some connection types only support a subset of these notification triggers.
Check each notification connection type for a list of supported triggers.

The following settings determine how Buildarr manages notification connection
definitions in Radarr.

##### ::: buildarr_radarr.config.settings.notifications.RadarrNotificationsSettings
    options:
      members:
        - delete_unmanaged
        - definitions


## Apprise

Receive media update and health alert push notifications via an Apprise server.

##### ::: buildarr_radarr.config.settings.notifications.apprise.AppriseNotification
    options:
      members:
        - type
        - base_url
        - configuration_key
        - stateless_urls
        - notification_type
        - apprise_tags
        - username
        - password

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_movie_added
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update


## Boxcar

##### ::: buildarr_radarr.config.settings.notifications.boxcar.BoxcarNotification
    options:
      members:
        - type
        - access_token

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_movie_added
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update


## Custom Script

##### ::: buildarr_radarr.config.settings.notifications.custom_script.CustomScriptNotification
    options:
      members:
        - type
        - path
        - arguments

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_rename
        - on_movie_added
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update


## Discord

##### ::: buildarr_radarr.config.settings.notifications.discord.DiscordNotification
    options:
      members:
        - type
        - webhook_url
        - username
        - avatar
        - host
        - on_grab_fields
        - on_import_fields
        - on_manual_interaction_fields

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_rename
        - on_movie_added
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update


## Email

##### ::: buildarr_radarr.config.settings.notifications.email.EmailNotification
    options:
      members:
        - type
        - server
        - port
        - use_encryption
        - username
        - password
        - from_address
        - recipient_addresses
        - cc_addresses
        - bcc_addresses

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_movie_added
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update


## Emby / Jellyfin

##### ::: buildarr_radarr.config.settings.notifications.emby_jellyfin.EmbyJellyfinNotification
    options:
      members:
        - type
        - hostname
        - port
        - use_ssl
        - api_key
        - send_notifications
        - update_library

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_rename
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_application_update


## Gotify

##### ::: buildarr_radarr.config.settings.notifications.gotify.GotifyNotification
    options:
      members:
        - type
        - server
        - app_token
        - priority
        - include_movie_poster

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_movie_added
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update


## Join

##### ::: buildarr_radarr.config.settings.notifications.join.JoinNotification
    options:
      members:
        - type
        - api_key
        - device_names
        - priority

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_movie_added
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update


## Kodi (XBMC)

##### ::: buildarr_radarr.config.settings.notifications.kodi.KodiNotification
    options:
      members:
        - type
        - hostname
        - port
        - use_ssl
        - username
        - password
        - display_notification
        - display_time
        - clean_library
        - always_update

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_rename
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update


## Mailgun

##### ::: buildarr_radarr.config.settings.notifications.mailgun.MailgunNotification
    options:
      members:
        - type
        - api_key
        - use_eu_endpoint
        - from_address
        - sender_domain
        - recipient_addresses

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_movie_added
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update



## Notifiarr

##### ::: buildarr_radarr.config.settings.notifications.notifiarr.NotifiarrNotification
    options:
      members:
        - type
        - api_key

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_rename
        - on_movie_added
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update


## ntfy

##### ::: buildarr_radarr.config.settings.notifications.ntfy.NtfyNotification
    options:
      members:
        - type
        - base_url
        - access_token
        - username
        - password
        - priority
        - topics
        - ntfy_tags
        - click_url

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_movie_added
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update


## Plex Media Server

Buildarr is unable to manage Plex Media Server notification connections at this time, due to Plex requiring external authentication using OAuth2.

Please add the Plex Media Server notification connection manually in the Radarr UI.

!!! warning

    Ensure `delete_unmanaged` is set to `false` in Buildarr, otherwise the Plex Media Server notification connection will be removed from Radarr whenever Buildarr performs an update run.


## Prowl

##### ::: buildarr_radarr.config.settings.notifications.prowl.ProwlNotification
    options:
      members:
        - type
        - api_key
        - priority

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_movie_added
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update


## Pushbullet

##### ::: buildarr_radarr.config.settings.notifications.pushbullet.PushbulletNotification
    options:
      members:
        - type
        - api_key
        - device_ids
        - channel_tags
        - sender_id

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_movie_added
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update


## Pushover

##### ::: buildarr_radarr.config.settings.notifications.pushover.PushoverNotification
    options:
      members:
        - type
        - user_key
        - api_key
        - devices
        - priority
        - retry
        - expire
        - sound

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_movie_added
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update


## Pushsafer

##### ::: buildarr_radarr.config.settings.notifications.pushsafer.PushsaferNotification
    options:
      members:
        - type
        - api_key
        - device_ids
        - priority
        - retry
        - expire
        - sound
        - vibration
        - icon
        - icon_color

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_movie_added
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update



## SendGrid

##### ::: buildarr_radarr.config.settings.notifications.sendgrid.SendgridNotification
    options:
      members:
        - type
        - api_key
        - from_address
        - recipient_addresses

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_movie_added
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update


## Signal

##### ::: buildarr_radarr.config.settings.notifications.signal.SignalNotification
    options:
      members:
        - type
        - hostname
        - port
        - use_ssl
        - sender_number
        - receiver_id
        - username
        - password

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_movie_added
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update


## Simplepush

##### ::: buildarr_radarr.config.settings.notifications.simplepush.SimplepushNotification
    options:
      members:
        - type
        - api_key
        - event

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_movie_added
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update


## Slack

##### ::: buildarr_radarr.config.settings.notifications.slack.SlackNotification
    options:
      members:
        - type
        - webhook_url
        - username
        - icon
        - channel

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_rename
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update


## Synology Indexer

##### ::: buildarr_radarr.config.settings.notifications.synology_indexer.SynologyIndexerNotification
    options:
      members:
        - type
        - update_library

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_import
        - on_upgrade
        - on_rename
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade


## Telegram

##### ::: buildarr_radarr.config.settings.notifications.telegram.TelegramNotification
    options:
      members:
        - type
        - bot_token
        - chat_id
        - send_silently

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_movie_added
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update


## Trakt

Buildarr is unable to manage Trakt notification connections at this time, due to Plex requiring external authentication using OAuth2.

Please add the Trakt notification connection manually in the Radarr UI.

!!! warning

    Ensure `delete_unmanaged` is set to `false` in Buildarr, otherwise the Trakt notification connection will be removed from Radarr whenever Buildarr performs an update run.


## Twitter

Buildarr is unable to manage Twitter notification connections at this time, due to Plex requiring external authentication using OAuth2.

Please add the Twitter notification connection manually in the Radarr UI.

!!! warning

    Ensure `delete_unmanaged` is set to `false` in Buildarr, otherwise the Twitter notification connection will be removed from Radarr whenever Buildarr performs an update run.


## Webhook

##### ::: buildarr_radarr.config.settings.notifications.webhook.WebhookNotification
    options:
      members:
        - type
        - webhook_url
        - method
        - username
        - password

##### ::: buildarr_radarr.config.settings.notifications.base.Notification
    options:
      members:
        - tags

##### Supported Notification Triggers

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_grab
        - on_import
        - on_upgrade
        - on_rename
        - on_movie_added
        - on_movie_delete
        - on_movie_file_delete
        - on_movie_file_delete_for_upgrade
        - on_health_issue
        - include_health_warnings
        - on_health_restored
        - on_manual_interaction_required
        - on_application_update
