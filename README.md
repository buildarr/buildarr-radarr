# Buildarr Radarr Plugin

[![PyPI](https://img.shields.io/pypi/v/buildarr-radarr)](https://pypi.org/project/buildarr-radarr) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/buildarr-radarr)  [![GitHub](https://img.shields.io/github/license/buildarr/buildarr-radarr)](https://github.com/buildarr/buildarr-radarr/blob/main/LICENSE) ![Pre-commit hooks](https://github.com/buildarr/buildarr-radarr/actions/workflows/pre-commit.yml/badge.svg) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The Buildarr Radarr plugin (`buildarr-radarr`) is a plugin for Buildarr that adds the capability to configure and manage [Radarr](http://radarr.video) instances.

Radarr is a PVR application which downloads, renames and manages the lifecycle of movies in your media library. In other words, it is to movies what [Sonarr](https://sonarr.tv) is to TV shoes. It can monitor for both upcoming and current releases and grab them when they become available, as well as upgrade to higher quality versions of monitored releases when a suitable version is available.

Currently, Radarr V4 and Radarr V5 are the supported versions. If you are using Radarr V3 or earlier, please upgrade in order to manage your instances with Buildarr.

## Installation

When using Buildarr as a [standalone application](https://buildarr.github.io/installation/#standalone-application), the Radarr plugin can simply be installed using `pip`:

```bash
pip install buildarr buildarr-radarr
```

When using Buildarr as a [Docker container](https://buildarr.github.io/installation/#docker), the Radarr plugin is bundled with the official container (`callum027/buildarr`), so there is no need to install it separately.

You can upgrade, or pin the version of the plugin to a specific version, within the container by setting the `$BUILDARR_INSTALL_PACKAGES` environment variable in the `docker run` command using `--env`/`-e`:

```bash
-e BUILDARR_INSTALL_PACKAGES="buildarr-radarr==<version>"
```

## Quick Start

To use the Radarr plugin, create a `radarr` block within `buildarr.yml`, and enter the connection information required for the Buildarr instance to connect to the Radarr instance you'd like to manage.

If authentication is disabled on your Radarr instance, Buildarr will automatically retrieve the API key from the instance, meaning that you do not need to define it in the configuration.

If authentication is enabled, manually retrieve the API key for Radarr by copying it from Settings -> General -> Security -> API Key, and pasting it into the configuration file as shown below.

```yaml
---

buildarr:
  watch_config: true

radarr:
  hostname: localhost  # Defaults to `radarr`, or the instance name for instance-specific configs.
  port: 7878  # Defaults to 7878.
  protocol:  http  # Defaults to `http`.
  api_key: ...  # Required if authentication is enabled. Auto-fetch if authentication is disabled.
```

Buildarr won't modify anything yet since no configuration has been defined, but you are able to test if Buildarr is able to connect to and authenticate with the Radarr instance.

Try a `buildarr run`. If the output is similar to the below output, Buildarr was able to connect to your Radarr instance.

```text
2023-09-02 18:46:05,366 buildarr:1 buildarr.cli.run [INFO] Buildarr version 0.6.0 (log level: INFO)
2023-09-02 18:46:05,366 buildarr:1 buildarr.cli.run [INFO] Loading configuration file '/config/buildarr.yml'
2023-09-02 18:46:05,403 buildarr:1 buildarr.cli.run [INFO] Finished loading configuration file
2023-09-02 18:46:05,417 buildarr:1 buildarr.cli.run [INFO] Loaded plugins: radarr (0.1.0)
2023-09-02 18:46:05,417 buildarr:1 buildarr.cli.run [INFO] Loading instance configurations
2023-09-02 18:46:05,422 buildarr:1 buildarr.cli.run [INFO] Finished loading instance configurations
2023-09-02 18:46:05,422 buildarr:1 buildarr.cli.run [INFO] Running with plugins: radarr
2023-09-02 18:46:05,422 buildarr:1 buildarr.cli.run [INFO] Resolving instance dependencies
2023-09-02 18:46:05,422 buildarr:1 buildarr.cli.run [INFO] Finished resolving instance dependencies
2023-09-02 18:46:05,422 buildarr:1 buildarr.cli.run [INFO] Fetching TRaSH metadata
2023-09-02 18:46:09,856 buildarr:1 buildarr.cli.run [INFO] Finished fetching TRaSH metadata
2023-09-02 18:46:09,856 buildarr:1 buildarr.cli.run [INFO] Rendering instance configuration dynamic attributes
2023-09-02 18:46:09,856 buildarr:1 buildarr.cli.run [INFO] Finished rendering instance configuration dynamic attributes
2023-09-02 18:46:09,856 buildarr:1 buildarr.cli.run [INFO] Loading secrets file from '/config/secrets.json'
2023-09-02 18:46:09,857 buildarr:1 buildarr.cli.run [INFO] Finished loading secrets file
2023-09-02 18:46:09,857 buildarr:1 buildarr.cli.run [INFO] <radarr> (default) Checking secrets
2023-09-02 18:46:09,869 buildarr:1 buildarr.cli.run [INFO] <radarr> (default) Connection test successful using cached secrets
2023-09-02 18:46:09,869 buildarr:1 buildarr.cli.run [INFO] <radarr> (default) Finished checking secrets
2023-09-02 18:46:09,870 buildarr:1 buildarr.cli.run [INFO] Saving updated secrets file to '/config/secrets.json'
2023-09-02 18:46:09,871 buildarr:1 buildarr.cli.run [INFO] Finished saving updated secrets file
2023-09-02 18:46:09,871 buildarr:1 buildarr.cli.run [INFO] Performing post-initialisation configuration render
2023-09-02 18:46:10,092 buildarr:1 buildarr.cli.run [INFO] Finished performing post-initialisation configuration render
2023-09-02 18:46:10,092 buildarr:1 buildarr.cli.run [INFO] Updating configuration on remote instances
2023-09-02 18:46:10,092 buildarr:1 buildarr.cli.run [INFO] <radarr> (default) Fetching remote configuration to check if updates are required
2023-09-02 18:46:10,446 buildarr:1 buildarr.cli.run [INFO] <radarr> (default) Finished fetching remote configuration
2023-09-02 18:46:10,522 buildarr:1 buildarr.cli.run [INFO] <radarr> (default) Updating remote configuration
2023-09-02 18:46:10,840 buildarr:1 buildarr.cli.run [INFO] <radarr> (default) Remote configuration is up to date
2023-09-02 18:46:10,840 buildarr:1 buildarr.cli.run [INFO] <radarr> (default) Finished updating remote configuration
2023-09-02 18:46:10,840 buildarr:1 buildarr.cli.run [INFO] Finished updating configuration on remote instances
2023-09-02 18:46:10,840 buildarr:1 buildarr.cli.run [INFO] Deleting unmanaged/unused resources on remote instances
2023-09-02 18:46:10,840 buildarr:1 buildarr.cli.run [INFO] <radarr> (default) Refetching remote configuration to delete unused resources
2023-09-02 18:46:11,171 buildarr:1 buildarr.cli.run [INFO] <radarr> (default) Finished refetching remote configuration
2023-09-02 18:46:11,263 buildarr:1 buildarr.cli.run [INFO] <radarr> (default) Deleting unmanaged/unused resources on the remote instance
2023-09-02 18:46:11,442 buildarr:1 buildarr.cli.run [INFO] <radarr> (default) Remote configuration is clean
2023-09-02 18:46:11,442 buildarr:1 buildarr.cli.run [INFO] <radarr> (default) Finished deleting unmanaged/unused resources on the remote instance
2023-09-02 18:46:11,442 buildarr:1 buildarr.cli.run [INFO] Finished deleting unmanaged/unused resources on remote instances
2023-09-02 18:46:11,442 buildarr:1 buildarr.cli.run [INFO] Deleting downloaded TRaSH metadata
2023-09-02 18:46:11,461 buildarr:1 buildarr.cli.run [INFO] Finished deleting downloaded TRaSH metadata
```

## Configuring your Buildarr instance

The following sections cover comprehensive configuration of a Radarr instance.

Note that these documents do not show how you *should* configure a Radarr instance. Rather, they show how you *can* configure a Radarr instance the way you want with Buildarr. For more information on how to optimally configure Radarr, you can refer to the excellent guides from [WikiArr](https://wiki.servarr.com/radarr) and [TRaSH-Guides](https://trash-guides.info/Radarr).

* [Host Configuration](https://buildarr.github.io/configuration/host)
* Settings
    * [Media Management](https://buildarr.github.io/configuration/settings/media-management)
    * Profiles
        * [Quality Profiles](https://buildarr.github.io/configuration/settings/profiles/quality-profiles)
        * [Delay Profiles](https://buildarr.github.io/configuration/settings/profiles/delay-profiles)
    * [Quality](https://buildarr.github.io/configuration/settings/quality)
    * [Custom Formats](https://buildarr.github.io/configuration/settings/custom-formats)
    * [Indexers](https://buildarr.github.io/configuration/settings/indexers)
    * [Download Clients](https://buildarr.github.io/configuration/settings/download-clients)
    * [Notifications (Connect)](https://buildarr.github.io/configuration/settings/notifications)
    * [Metadata](https://buildarr.github.io/configuration/settings/metadata)
    * [Tags](https://buildarr.github.io/configuration/settings/tags)
    * [General](https://buildarr.github.io/configuration/settings/general)
    * [UI](https://buildarr.github.io/configuration/settings/ui)

Configuration of the following resources are not yet supported by this plugin (but will be added in future versions):

* Import Lists

## Dumping an existing Radarr instance configuration

Buildarr is capable of dumping a running Radarr instance's configuration.

```text
$ buildarr radarr dump-config http://localhost:7878 > radarr.yml
Radarr instance API key: <Paste API key here>
```

The dumped YAML object can be placed directly under the `radarr` configuration block, or used as an [instance-specific configuration](https://buildarr.github.io/configuration/#multiple-instances-of-the-same-type).

All possible values are explicitly defined in this dumped configuration.

```yaml
hostname: localhost
port: 7878
protocol: http
api_key: 1a2b3c4d5e6f1a2b3c4d5e6f1a2b3c4d
image: lscr.io/linuxserver/radarr
version: 4.7.5.7809
settings:
  media_management:
    rename_movies: true
    replace_illegal_characters: true
    colon_replacement: space-dash-space
    standard_movie_format: '{Movie CleanTitle} - {Edition Tags }{[Custom Formats]
      }{[Quality Full] }{[MediaInfo 3D] }{[MediaInfo VideoDynamicRangeType] }[{Mediainfo
      AudioCodec}{ Mediainfo AudioChannels}]{ [Mediainfo VideoCodec]}{ [Release Group]}
      - Default'
    movie_folder_format: '{Movie CleanTitle} ({Release Year}) [imdbid-{ImdbId}]'
    create_missing_movie_folders: false
    delete_empty_folders: false
    skip_free_space_check: false
    minimum_free_space: 100
    use_hardlinks: true
    import_using_script: false
    import_script_path: null
    import_extra_files: false
    unmonitor_deleted_movies: false
    propers_and_repacks: do-not-prefer
    analyze_video_files: true
    rescan_folder_after_refresh: always
    change_file_date: none
    recycling_bin: null
    recycling_bin_cleanup: 28
    set_permissions: false
    chmod_folder: drwxr-xr-x
    chown_group: null
    root_folders:
      delete_unmanaged: false
      definitions: []
  profiles:
    quality_profiles:
      delete_unmanaged: false
      definitions:
        Movies:
          upgrades_allowed: true
          qualities:
          - Bluray-1080p
          - name: WEB 1080p
            members:
            - WEBRip-1080p
            - WEBDL-1080p
          - Bluray-720p
          - name: WEB 720p
            members:
            - WEBDL-720p
            - WEBRip-720p
          - Bluray-576p
          - Bluray-480p
          - name: WEB 480p
            members:
            - WEBDL-480p
            - WEBRip-480p
          - name: DVD-Video
            members:
            - DVD-R
            - DVD
          upgrade_until_quality: Bluray-1080p
          minimum_custom_format_score: 0
          upgrade_until_custom_format_score: 10000
          custom_formats:
          - name: 4k-remaster
            score: 25
          - name: remaster
            score: 25
          language: English
    delay_profiles:
      definitions:
      - preferred_protocol: torrent-prefer
        usenet_delay: 0
        torrent_delay: 1440
        bypass_if_highest_quality: true
        tags: []
      delete_unmanaged: false
  quality:
    trash_id: null
    definitions:
      Unknown:
        title: null
        min: 0.0
        preferred: 3.3
        max: null
      WORKPRINT:
        title: null
        min: 0.0
        preferred: 95.0
        max: 100.0
      CAM:
        title: null
        min: 0.0
        preferred: 95.0
        max: 100.0
      TELESYNC:
        title: null
        min: 0.0
        preferred: 95.0
        max: 100.0
      TELECINE:
        title: null
        min: 0.0
        preferred: 95.0
        max: 100.0
      REGIONAL:
        title: null
        min: 0.0
        preferred: 95.0
        max: 100.0
      DVDSCR:
        title: null
        min: 0.0
        preferred: 95.0
        max: 100.0
      SDTV:
        title: null
        min: 0.0
        preferred: 95.0
        max: 100.0
      DVD:
        title: null
        min: 0.0
        preferred: 95.0
        max: 100.0
      DVD-R:
        title: null
        min: 0.0
        preferred: 95.0
        max: 100.0
      WEBDL-480p:
        title: null
        min: 0.0
        preferred: 95.0
        max: 100.0
      WEBRip-480p:
        title: null
        min: 0.0
        preferred: 95.0
        max: 100.0
      Bluray-480p:
        title: null
        min: 0.0
        preferred: 95.0
        max: 100.0
      Bluray-576p:
        title: null
        min: 0.0
        preferred: 95.0
        max: 100.0
      HDTV-720p:
        title: null
        min: 17.1
        preferred: 95.0
        max: null
      WEBDL-720p:
        title: null
        min: 12.5
        preferred: 95.0
        max: null
      WEBRip-720p:
        title: null
        min: 12.5
        preferred: 95.0
        max: null
      Bluray-720p:
        title: null
        min: 25.7
        preferred: 95.0
        max: null
      HDTV-1080p:
        title: null
        min: 33.8
        preferred: 95.0
        max: null
      WEBDL-1080p:
        title: null
        min: 12.5
        preferred: 95.0
        max: null
      WEBRip-1080p:
        title: null
        min: 12.5
        preferred: 95.0
        max: null
      Bluray-1080p:
        title: null
        min: 50.8
        preferred: null
        max: null
      Remux-1080p:
        title: null
        min: 136.8
        preferred: null
        max: null
      HDTV-2160p:
        title: null
        min: 85.0
        preferred: null
        max: null
      WEBDL-2160p:
        title: null
        min: 34.5
        preferred: null
        max: null
      WEBRip-2160p:
        title: null
        min: 34.5
        preferred: null
        max: null
      Bluray-2160p:
        title: null
        min: 102.0
        preferred: null
        max: null
      Remux-2160p:
        title: null
        min: 187.4
        preferred: null
        max: null
      BR-DISK:
        title: null
        min: 0.0
        preferred: null
        max: null
      Raw-HD:
        title: null
        min: 0.0
        preferred: null
        max: null
  custom_formats:
    delete_unmanaged: false
    definitions:
      remaster:
        trash_id: null
        default_score: null
        include_when_renaming: false
        delete_unmanaged_conditions: false
        conditions:
          Not 4K Remaster:
            negate: true
            required: true
            type: release-title
            regex: 4K
          Remaster:
            negate: false
            required: true
            type: release-title
            regex: Remaster
      4k-remaster:
        trash_id: null
        default_score: null
        include_when_renaming: false
        delete_unmanaged_conditions: false
        conditions:
          4K:
            negate: false
            required: true
            type: release-title
            regex: 4k
          Not 4K Resolution:
            negate: true
            required: true
            type: resolution
            resolution: r2160p
          Remaster:
            negate: false
            required: true
            type: release-title
            regex: Remaster
  indexers:
    minimum_age: 0
    retention: 0
    maximum_size: 0
    rss_sync_interval: 60
    delete_unmanaged: false
    definitions:
      1337x (Prowlarr):
        enable_rss: true
        enable_automatic_search: true
        enable_interactive_search: true
        priority: 25
        download_client: null
        tags: []
        minimum_seeders: 2
        seed_ratio: null
        seed_time: null
        type: torznab
        base_url: http://prowlarr:9696/1/
        api_path: /api
        api_key: f6e5d4c3b2a10f6e5d4c3b2a10f6e5d4
        multi_languages: []
        categories:
        - MOVIES-FOREIGN
        - MOVIES-SD
        - MOVIES-DVD
        - MOVIES-HD
        additional_parameters: null
  download_clients:
    delete_unmanaged: false
    definitions:
      Transmission:
        enable: true
        priority: 1
        remove_completed: true
        tags: []
        host: transmission
        port: 9091
        use_ssl: false
        url_base: /transmission/
        username: null
        password: null
        category: null
        directory: /data/torrents/movies
        recent_priority: last
        older_priority: last
        add_paused: false
        type: transmission
  notifications:
    delete_unmanaged: false
    definitions: {}
  metadata:
    certification_country: us
    emby_legacy:
      enable: false
      movie_metadata: true
    kodi_emby:
      enable: false
      movie_metadata: true
      movie_metadata_url: false
      movie_metadata_language: english
      movie_images: true
      use_movie_nfo: false
      add_collection_name: true
    roksbox:
      enable: false
      movie_metadata: true
      movie_images: true
    wdtv:
      enable: false
      movie_metadata: true
      movie_images: true
  tags:
    definitions:
    - sup
  general:
    host:
      bind_address: '*'
      port: 7878
      ssl_port: 9898
      use_ssl: false
      ssl_cert_path: null
      ssl_cert_password: null
      url_base: null
      instance_name: Radarr
    security:
      authentication: none
      username: null
      password: null
      certificate_validation: enabled
    proxy:
      enable: false
      proxy_type: http
      hostname: null
      port: 8080
      username: null
      password: null
      ignored_addresses: []
      bypass_proxy_for_local_addresses: true
    logging:
      log_level: INFO
    analytics:
      send_anonymous_usage_data: false
    updates:
      branch: master
      automatic: false
      mechanism: docker
      script_path: null
    backup:
      folder: Backups
      interval: 7
      retention: 28
  ui:
    first_day_of_week: monday
    week_column_header: day-first
    runtime_format: hours-minutes
    short_date_format: slash-day-first
    long_date_format: day-first
    time_format: twentyfour-hour
    show_relative_dates: true
    theme: auto
    enable_color_impaired_mode: false
    movie_info_language: english
    ui_language: english
```
