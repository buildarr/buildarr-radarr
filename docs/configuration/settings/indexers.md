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


## FileList

Monitor for new releases on the FileList.io private torrent tracker.

##### ::: buildarr_radarr.config.settings.indexers.torrent.filelist.FilelistIndexer
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - enable_rss
        - enable_automatic_search
        - enable_interactive_search
        - priority
        - download_client

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - tags


##### ::: buildarr_radarr.config.settings.indexers.torrent.base.TorrentIndexer

##### ::: buildarr_radarr.config.settings.indexers.torrent.filelist.FilelistIndexer
    options:
      members:
        - base_url
        - username
        - passkey
        - categories

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - tags


## HDBits

Monitor for new releases on the HDBits private torrent tracker.

##### ::: buildarr_radarr.config.settings.indexers.torrent.hdbits.HdbitsIndexer
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - enable_rss
        - enable_automatic_search
        - enable_interactive_search
        - priority
        - download_client

##### ::: buildarr_radarr.config.settings.indexers.torrent.base.TorrentIndexer

##### ::: buildarr_radarr.config.settings.indexers.torrent.hdbits.HdbitsIndexer
    options:
      members:
        - base_url
        - username
        - api_key

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - tags


## IPTorrents

Monitor for releases using the legacy API for the IPTorrents private torrent tracker.

!!! warning

    IPTorrents' legacy API does not support automatic searching.
    It is recommended to instead configure IPTorrents as a [Torznab indexer](#torznab).

##### ::: buildarr_radarr.config.settings.indexers.torrent.iptorrents.IptorrentsIndexer
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - enable_rss
        - enable_automatic_search
        - enable_interactive_search
        - priority
        - download_client

##### ::: buildarr_radarr.config.settings.indexers.torrent.base.TorrentIndexer

##### ::: buildarr_radarr.config.settings.indexers.torrent.iptorrents.IptorrentsIndexer
    options:
      members:
        - feed_url

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - tags


## Newznab

Monitor for new releases using a Newznab-compatible Usenet indexer.

##### ::: buildarr_radarr.config.settings.indexers.usenet.newznab.NewznabIndexer
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - enable_rss
        - enable_automatic_search
        - enable_interactive_search
        - priority
        - download_client

##### ::: buildarr_radarr.config.settings.indexers.usenet.newznab.NewznabIndexer
    options:
      members:
        - base_url
        - api_path
        - api_key
        - categories
        - remove_year
        - additional_parameters

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - tags


## Nyaa

Monitor for new releases on the configured Nyaa torrent tracker domain.

##### ::: buildarr_radarr.config.settings.indexers.torrent.nyaa.NyaaIndexer
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - enable_rss
        - enable_automatic_search
        - enable_interactive_search
        - priority
        - download_client

##### ::: buildarr_radarr.config.settings.indexers.torrent.base.TorrentIndexer

##### ::: buildarr_radarr.config.settings.indexers.torrent.nyaa.NyaaIndexer
    options:
      members:
        - website_url
        - anime_standard_format_search
        - additional_parameters

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - tags


## PassThePopcorn

Monitor for new releases using the PassThePopcorn private torrent tracker.

##### ::: buildarr_radarr.config.settings.indexers.torrent.passthepopcorn.PassthepopcornIndexer
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - enable_rss
        - enable_automatic_search
        - enable_interactive_search
        - priority
        - download_client

##### ::: buildarr_radarr.config.settings.indexers.torrent.base.TorrentIndexer

##### ::: buildarr_radarr.config.settings.indexers.torrent.passthepopcorn.PassthepopcornIndexer
    options:
      members:
        - base_url
        - api_user
        - api_key

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - tags


## TorrentPotato

Monitor for new releases using a legacy CouchPotato-compatible torrent tracker.

##### ::: buildarr_radarr.config.settings.indexers.torrent.torrentpotato.TorrentpotatoIndexer
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - enable_rss
        - enable_automatic_search
        - enable_interactive_search
        - priority
        - download_client

##### ::: buildarr_radarr.config.settings.indexers.torrent.base.TorrentIndexer

##### ::: buildarr_radarr.config.settings.indexers.torrent.torrentpotato.TorrentpotatoIndexer
    options:
      members:
        - base_url
        - username
        - passkey

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - tags


## Torrent RSS Feed

Monitor for new releases from a torrent tracker RSS feed.

!!! warning

    This indexer does not support automatic searching.
    It is recommended to use an indexer that natively communicates with a tracker using an API.

##### ::: buildarr_radarr.config.settings.indexers.torrent.rss.TorrentRssIndexer
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - enable_rss
        - enable_automatic_search
        - enable_interactive_search
        - priority
        - download_client

##### ::: buildarr_radarr.config.settings.indexers.torrent.base.TorrentIndexer

##### ::: buildarr_radarr.config.settings.indexers.torrent.rss.TorrentRssIndexer
    options:
      members:
        - feed_url
        - cookie
        - allow_zero_size

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - tags


## Torznab

Monitor for new releases using a Torznab-compatible torrent tracker or indexer application.

##### ::: buildarr_radarr.config.settings.indexers.torrent.torznab.TorznabIndexer
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - enable_rss
        - enable_automatic_search
        - enable_interactive_search
        - priority
        - download_client

##### ::: buildarr_radarr.config.settings.indexers.torrent.base.TorrentIndexer

##### ::: buildarr_radarr.config.settings.indexers.torrent.torznab.TorznabIndexer
    options:
      members:
        - base_url
        - api_path
        - api_key
        - categories
        - remove_year
        - additional_parameters

##### ::: buildarr_radarr.config.settings.indexers.base.Indexer
    options:
      members:
        - tags
