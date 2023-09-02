# Indexers

##### ::: buildarr_radarr.config.settings.indexers.RadarrIndexersSettings
    options:
      members:
        - minimum_age
        - retention
        - maximum_size
        - rss_sync_interval
        - delete_unmanaged
        - definitions

## Configuring indexers

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - enable_rss
        - enable_automatic_search
        - enable_interactive_search
        - priority
        - download_client
        - tags

## Newznab

##### ::: buildarr_radarr.config.settings.indexers.usenet.newznab.NewznabIndexer
    options:
      members:
        - type
        - url
        - api_path
        - password
        - categories
        - anime_categories
        - anime_standard_format_search
        - additional_parameters

## Torrent Indexers

##### ::: buildarr_radarr.config.settings.indexers.torrent.base.TorrentIndexer
    options:
      members:
        - minimum_seeders
        - seed_ratio
        - seed_time
        - seasonpack_seed_time

## Filelist

##### ::: buildarr_radarr.config.settings.indexers.torrent.filelist.FilelistIndexer
    options:
      members:
        - type
        - username
        - passkey
        - api_url
        - categories
        - anime_categories

## HDBits

##### ::: buildarr_radarr.config.settings.indexers.torrent.hdbits.HdbitsIndexer
    options:
      members:
        - type
        - username
        - api_key
        - api_url

## IP Torrents

##### ::: buildarr_radarr.config.settings.indexers.torrent.iptorrents.IptorrentsIndexer
    options:
      members:
        - type
        - feed_url

## Nyaa

##### ::: buildarr_radarr.config.settings.indexers.torrent.nyaa.NyaaIndexer
    options:
      members:
        - type
        - website_url
        - anime_standard_format_search
        - additional_parameters

## Rarbg

##### ::: buildarr_radarr.config.settings.indexers.torrent.rarbg.RarbgIndexer
    options:
      members:
        - type
        - api_url
        - ranked_only
        - captcha_token

## Torrent RSS Feed

##### ::: buildarr_radarr.config.settings.indexers.torrent.rss.TorrentRssIndexer
    options:
      members:
        - type
        - full_rss_feed_url
        - cookie
        - allow_zero_size

## Torznab

##### ::: buildarr_radarr.config.settings.indexers.torrent.torznab.TorznabIndexer
    options:
      members:
        - type
        - url
        - api_path
        - password
        - categories
        - anime_categories
        - anime_standard_format_search
        - additional_parameters
