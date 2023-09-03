# Notifications (Connect)

Radarr supports pushing notifications to external applications and services.

These are not only for Radarr to communicate with the outside world, they can also be useful
for monitoring since the user can be alerted, by a service of their choice, when
some kind of event (or problem) occurs.

## Configuration

##### ::: buildarr_radarr.config.settings.notifications.base.NotificationTriggers
    options:
      members:
        - on_health_issue
        - include_health_warnings
        - on_application_update

## Apprise

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

## Boxcar

##### ::: buildarr_radarr.config.settings.notifications.boxcar.BoxcarNotification
    options:
      members:
        - type
        - access_token

## Custom Script

##### ::: buildarr_radarr.config.settings.notifications.custom_script.CustomScriptNotification
    options:
      members:
        - type
        - path

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

## Gotify

##### ::: buildarr_radarr.config.settings.notifications.gotify.GotifyNotification
    options:
      members:
        - type
        - server
        - app_token
        - priority

## Join

##### ::: buildarr_radarr.config.settings.notifications.join.JoinNotification
    options:
      members:
        - type
        - api_key
        - device_names
        - priority

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

## Notifiarr

##### ::: buildarr_radarr.config.settings.notifications.notifiarr.NotifiarrNotification
    options:
      members:
        - type
        - api_key

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

## Prowl

##### ::: buildarr_radarr.config.settings.notifications.prowl.ProwlNotification
    options:
      members:
        - type
        - api_key
        - priority

## Pushbullet

##### ::: buildarr_radarr.config.settings.notifications.pushbullet.PushbulletNotification
    options:
      members:
        - type
        - api_key
        - device_ids
        - channel_tags
        - sender_id

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

## SendGrid

##### ::: buildarr_radarr.config.settings.notifications.sendgrid.SendgridNotification
    options:
      members:
        - type
        - api_key
        - from_address
        - recipient_addresses

## Slack

##### ::: buildarr_radarr.config.settings.notifications.slack.SlackNotification
    options:
      members:
        - type
        - webhook_url
        - username
        - icon
        - channel

## Telegram

##### ::: buildarr_radarr.config.settings.notifications.telegram.TelegramNotification
    options:
      members:
        - type
        - bot_token
        - chat_id
        - send_silently

## Twitter

##### ::: buildarr_radarr.config.settings.notifications.twitter.TwitterNotification
    options:
      members:
        - type
        - consumer_key
        - consumer_secret
        - access_token
        - access_token_secret
        - mention
        - direct_message

## Webhook

##### ::: buildarr_radarr.config.settings.notifications.webhook.WebhookNotification
    options:
      members:
        - type
        - webhook_url
        - method
        - username
        - password
