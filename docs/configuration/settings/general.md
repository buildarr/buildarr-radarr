# General

General configuration for Radarr are separated by category.

```yaml
radarr:
  settings:
    general:
      host:
        bind_address: "*"
        port: 7878
        url_base: null
        use_ssl: false
        instance_name: Radarr (Buildarr Example)
      security:
        authentication: none
      proxy:
        enable: false
      logging:
        log_level: "INFO"
      analytics:
        send_anonymous_usage_data: true
      updates:
        branch: master
        automatic: false
        mechanism: docker
      backup:
        folder: Backups
        interval: 7
        retention: 28
```

Some of the settings may affect Buildarr's ability to connect with the Prowlarr instance.
Take care when changing these settings.

## Host

##### ::: buildarr_radarr.config.settings.general.HostGeneralSettings
    options:
      members:
        - bind_address
        - port
        - ssl_port
        - use_ssl
        - ssl_cert_path
        - ssl_cert_password
        - url_base
        - instance_name

## Security

##### ::: buildarr_radarr.config.settings.general.SecurityGeneralSettings
    options:
      members:
        - authentication
        - username
        - password
        - certificate_validation

## Proxy

##### ::: buildarr_radarr.config.settings.general.ProxyGeneralSettings
    options:
      members:
        - enable
        - proxy_type
        - hostname
        - port
        - username
        - password
        - ignored_addresses
        - bypass_proxy_for_local_addresses

## Logging

##### ::: buildarr_radarr.config.settings.general.LoggingGeneralSettings
    options:
      members:
        - log_level

## Analytics

##### ::: buildarr_radarr.config.settings.general.AnalyticsGeneralSettings
    options:
      members:
        - send_anonymous_usage_data

## Updates

##### ::: buildarr_radarr.config.settings.general.UpdatesGeneralSettings
    options:
      members:
        - branch
        - automatic
        - mechanism
        - script_path

## Backup

##### ::: buildarr_radarr.config.settings.general.BackupGeneralSettings
    options:
      members:
        - folder
        - interval
        - retention
