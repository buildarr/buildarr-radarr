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
            on_application_update: true
            on_manual_interaction_required: true
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
        - on_application_update
        - on_manual_interaction_required






## Apprise

Receive media update and health alert push notifications via an Apprise server.

##### ::: buildarr_radarr.config.settings.notifications.apprise.AppriseNotification
    options:
      members:
        - type
        - base_url
        - configuration_key
        - stateless_urls
        - apprise_tags
        - auth_username
        - auth_password

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
        - on_application_update
        - on_manual_interaction_required


## Boxcar

##### ::: buildarr_radarr.config.settings.notifications.boxcar.BoxcarNotification
    options:
      members:
        - type
        - access_token

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
        - on_application_update
        - on_manual_interaction_required


## Custom Script

##### ::: buildarr_radarr.config.settings.notifications.custom_script.CustomScriptNotification
    options:
      members:
        - type
        - path

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
        - on_application_update
        - on_manual_interaction_required


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
        - on_application_update
        - on_manual_interaction_required


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
        - on_application_update
        - on_manual_interaction_required


## Emby / Jellyfin

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
        - on_application_update
        - on_manual_interaction_required


## Join

##### ::: buildarr_radarr.config.settings.notifications.join.JoinNotification
    options:
      members:
        - type
        - api_key
        - device_names
        - priority

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
        - on_application_update
        - on_manual_interaction_required


## Kodi (XBMC)

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
        - on_manual_interaction_required


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
        - on_application_update
        - on_manual_interaction_required



## Notifiarr

##### ::: buildarr_radarr.config.settings.notifications.notifiarr.NotifiarrNotification
    options:
      members:
        - type
        - api_key

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
        - on_application_update
        - on_manual_interaction_required


## ntfy

##### ::: buildarr_radarr.config.settings.notifications.ntfy.NtfyNotification
    options:
      members:
        - type
        - server_url
        - username
        - password
        - priority
        - topics
        - ntfy_tags
        - click_url

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
        - on_application_update
        - on_manual_interaction_required


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
        - on_application_update
        - on_manual_interaction_required


## Pushbullet

##### ::: buildarr_radarr.config.settings.notifications.pushbullet.PushbulletNotification
    options:
      members:
        - type
        - api_key
        - device_ids
        - channel_tags
        - sender_id

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
        - on_application_update
        - on_manual_interaction_required


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
        - on_application_update
        - on_manual_interaction_required


## Pushsafer

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
        - on_application_update
        - on_manual_interaction_required



## SendGrid

##### ::: buildarr_radarr.config.settings.notifications.sendgrid.SendgridNotification
    options:
      members:
        - type
        - api_key
        - from_address
        - recipient_addresses

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
        - on_application_update
        - on_manual_interaction_required


## Signal

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
        - on_application_update
        - on_manual_interaction_required


## Simplepush

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
        - on_application_update
        - on_manual_interaction_required


## Slack

##### ::: buildarr_radarr.config.settings.notifications.slack.SlackNotification
    options:
      members:
        - type
        - webhook_url
        - username
        - icon
        - channel

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
        - on_manual_interaction_required


## Telegram

##### ::: buildarr_radarr.config.settings.notifications.telegram.TelegramNotification
    options:
      members:
        - type
        - bot_token
        - chat_id
        - send_silently

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
        - on_application_update
        - on_manual_interaction_required


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
        - on_application_update
        - on_manual_interaction_required
