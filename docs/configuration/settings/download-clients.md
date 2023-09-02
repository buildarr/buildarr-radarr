# Download Clients

##### ::: buildarr_radarr.config.settings.download_clients.RadarrDownloadClientsSettings
    options:
      members:
        - delete_unmanaged
        - definitions

## Configuring download clients

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - enable
        - priority
        - tags

## Usenet download clients

These download clients retrieve media using the [Usenet](https://en.wikipedia.org/wiki/Usenet) discussion and content delivery system.

## Download Station (Usenet)

##### ::: buildarr_radarr.config.settings.download_clients.usenet.downloadstation.DownloadstationUsenetDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - username
        - password
        - category
        - directory

## NZBGet

##### ::: buildarr_radarr.config.settings.download_clients.usenet.nzbget.NzbgetDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - url_base
        - username
        - password
        - category
        - client_priority
        - add_paused
        - category_mappings

## NZBVortex

##### ::: buildarr_radarr.config.settings.download_clients.usenet.nzbvortex.NzbvortexDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - url_base
        - api_key
        - category
        - client_priority
        - category_mappings

## Pneumatic

##### ::: buildarr_radarr.config.settings.download_clients.usenet.pneumatic.PneumaticDownloadClient
    options:
      members:
        - type
        - nzb_folder

## SABnzbd

##### ::: buildarr_radarr.config.settings.download_clients.usenet.sabnzbd.SabnzbdDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - url_base
        - api_key
        - category
        - client_priority
        - category_mappings

## Usenet Blackhole

##### ::: buildarr_radarr.config.settings.download_clients.usenet.blackhole.UsenetBlackholeDownloadClient
    options:
      members:
        - type
        - nzb_folder

## Torrent download clients

These download clients use the [BitTorrent](https://en.wikipedia.org/wiki/BitTorrent)
peer-to-peer file sharing protocol to retrieve media files.

## Aria2

##### ::: buildarr_radarr.config.settings.download_clients.torrent.aria2.Aria2DownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - rpc_path
        - secret_token

## Deluge

##### ::: buildarr_radarr.config.settings.download_clients.torrent.deluge.DelugeDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - url_base
        - password
        - category
        - client_priority
        - category_mappings

## Download Station (Torrent)

##### ::: buildarr_radarr.config.settings.download_clients.torrent.downloadstation.DownloadstationTorrentDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - username
        - password
        - category
        - directory

## Flood

##### ::: buildarr_radarr.config.settings.download_clients.torrent.flood.FloodDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - url_base
        - username
        - password
        - destination
        - flood_tags
        - additional_tags
        - add_paused
        - category_mappings

## Freebox

##### ::: buildarr_radarr.config.settings.download_clients.torrent.freebox.FreeboxDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - api_url
        - app_id
        - app_token
        - destination_directory
        - category
        - client_priority
        - add_paused
        - category_mappings

## Hadouken

##### ::: buildarr_radarr.config.settings.download_clients.torrent.hadouken.HadoukenDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - url_base
        - username
        - password
        - category
        - category_mappings

## qBittorrent

##### ::: buildarr_radarr.config.settings.download_clients.torrent.qbittorrent.QbittorrentDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - url_base
        - username
        - password
        - category
        - client_priority
        - initial_state
        - sequential_order
        - first_and_last_first
        - category_mappings

## RTorrent (ruTorrent)

##### ::: buildarr_radarr.config.settings.download_clients.torrent.rtorrent.RtorrentDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - url_base
        - username
        - password
        - category
        - client_priority
        - add_stopped
        - category_mappings

## Torrent Blackhole

##### ::: buildarr_radarr.config.settings.download_clients.torrent.blackhole.TorrentBlackholeDownloadClient
    options:
      members:
        - type
        - torrent_folder
        - save_magnet_files
        - magnet_file_extension
        - read_only

## Transmission/Vuze

Transmission and Vuze use the same configuration parameters.

To use Transmission, set the `type` attribute in the download client to `transmission`.

To use Vuze, set the `type` attribute in the download client to `vuze`.

##### ::: buildarr_radarr.config.settings.download_clients.torrent.transmission.TransmissionDownloadClientBase
    options:
      members:
        - host
        - port
        - use_ssl
        - url_base
        - username
        - password
        - category
        - directory
        - client_priority
        - add_paused

## uTorrent

##### ::: buildarr_radarr.config.settings.download_clients.torrent.utorrent.UtorrentDownloadClient
    options:
      members:
        - type
        - host
        - port
        - use_ssl
        - url_base
        - username
        - password
        - category
        - client_priority
        - initial_state
        - category_mappings
