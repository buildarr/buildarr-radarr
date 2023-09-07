# Download Clients

Radarr is linked to one or more *download clients* to actually handle downloading releases
that have been grabbed from indexers.

There are two types of download clients: Usenet clients, which grab releases from Usenet indexers,
and torrent download clients, which download (and subsequently seed) releases using the BitTorrent
P2P protocol.

```yaml
---

radarr:
  settings:
    download_clients:
      delete_unmanaged: true
      definitions:
        Transmission:  # Name of the download client
          type: transmission  # Type of download client
          enable: true  # Enable the download client in Radarr
          host: transmission
          port: 9091
          category: radarr
          # Define any other type-specific or global
          # download client attributes as needed.
        ...
```

In Buildarr, download clients are defined using a dictionary structure, as shown above.

The following parameters control how Buildarr configures download clients on Radarr instances.

##### ::: buildarr_radarr.config.settings.download_clients.RadarrDownloadClientsSettings
    options:
      members:
        - delete_unmanaged
        - definitions


## Aria2

Download client for torrent releases using the Aria2 download utility.

##### ::: buildarr_radarr.config.settings.download_clients.torrent.aria2.Aria2DownloadClient
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.download_clients.torrent.aria2.Aria2DownloadClient
    options:
      members:
        - hostname
        - port
        - use_ssl
        - rpc_path
        - secret_token

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - remove_completed_downloads
        - remove_failed_downloads
        - priority
        - tags


## Deluge

Download client for torrent releases using the Deluge torrent client.

##### ::: buildarr_radarr.config.settings.download_clients.torrent.deluge.DelugeDownloadClient
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.download_clients.torrent.deluge.DelugeDownloadClient
    options:
      members:
        - hostname
        - port
        - use_ssl
        - url_base
        - password
        - category
        - recent_priority
        - older_priority
        - add_paused

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - remove_completed_downloads
        - remove_failed_downloads
        - priority
        - tags


## Download Station (Torrent)

Download client for torrent releases using the Download Station download utility.

##### ::: buildarr_radarr.config.settings.download_clients.torrent.downloadstation.DownloadstationTorrentDownloadClient
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.download_clients.torrent.downloadstation.DownloadstationTorrentDownloadClient
    options:
      members:
        - hostname
        - port
        - use_ssl
        - username
        - password
        - category
        - directory

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - remove_completed_downloads
        - remove_failed_downloads
        - priority
        - tags


## Download Station (Usenet)

Download client for Usenet releases using the Download Station download utility.

##### ::: buildarr_radarr.config.settings.download_clients.usenet.downloadstation.DownloadstationUsenetDownloadClient
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.download_clients.usenet.downloadstation.DownloadstationUsenetDownloadClient
    options:
      members:
        - hostname
        - port
        - use_ssl
        - username
        - password
        - category
        - directory

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - remove_completed_downloads
        - remove_failed_downloads
        - priority
        - tags


## Flood

Download client for torrent releases using the Flood torrent client.

##### ::: buildarr_radarr.config.settings.download_clients.torrent.flood.FloodDownloadClient
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.download_clients.torrent.flood.FloodDownloadClient
    options:
      members:
        - hostname
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

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - remove_completed_downloads
        - remove_failed_downloads
        - priority
        - tags


## Freebox

Download client for torrent releases using a Freebox instance.

##### ::: buildarr_radarr.config.settings.download_clients.torrent.freebox.FreeboxDownloadClient
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.download_clients.torrent.freebox.FreeboxDownloadClient
    options:
      members:
        - host
        - port
        - use_ssl
        - api_url
        - app_id
        - app_token
        - destination_directory
        - category
        - recent_priority
        - older_priority
        - add_paused

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - remove_completed_downloads
        - remove_failed_downloads
        - priority
        - tags


## Hadouken

Download client for torrent releases using the Hadouken torrent client.

##### ::: buildarr_radarr.config.settings.download_clients.torrent.hadouken.HadoukenDownloadClient
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.download_clients.torrent.hadouken.HadoukenDownloadClient
    options:
      members:
        - hostname
        - port
        - use_ssl
        - url_base
        - username
        - password
        - category

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - remove_completed_downloads
        - remove_failed_downloads
        - priority
        - tags


## NZBGet

Download client for Usenet releases using the NZBGet Usenet client.

##### ::: buildarr_radarr.config.settings.download_clients.usenet.nzbget.NzbgetDownloadClient
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.download_clients.usenet.nzbget.NzbgetDownloadClient
    options:
      members:
        - hostname
        - port
        - use_ssl
        - url_base
        - username
        - password
        - category
        - recent_priority
        - older_priority
        - add_paused

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - remove_completed_downloads
        - remove_failed_downloads
        - priority
        - tags


## NZBVortex

Download client for Usenet releases using the NZBVortex Usenet client.

##### ::: buildarr_radarr.config.settings.download_clients.usenet.nzbvortex.NzbvortexDownloadClient
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.download_clients.usenet.nzbvortex.NzbvortexDownloadClient
    options:
      members:
        - hostname
        - port
        - use_ssl
        - url_base
        - api_key
        - category
        - recent_priority
        - older_priority

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - remove_completed_downloads
        - remove_failed_downloads
        - priority
        - tags


## Pneumatic

Download client for Usenet releases using the Pneumatic add-on for Kodi (XBMC).

##### ::: buildarr_radarr.config.settings.download_clients.usenet.pneumatic.PneumaticDownloadClient
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.download_clients.usenet.pneumatic.PneumaticDownloadClient
    options:
      members:
        - nzb_folder
        - strm_folder

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - remove_completed_downloads
        - remove_failed_downloads
        - priority
        - tags


## qBittorrent

Download client for torrent releases using the qBittorrent torrent client.

##### ::: buildarr_radarr.config.settings.download_clients.torrent.qbittorrent.QbittorrentDownloadClient
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.download_clients.torrent.qbittorrent.QbittorrentDownloadClient
    options:
      members:
        - hostname
        - port
        - use_ssl
        - url_base
        - username
        - password
        - category
        - postimport_category
        - recent_priority
        - older_priority
        - initial_state
        - sequential_order
        - first_and_last_first

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - remove_completed_downloads
        - remove_failed_downloads
        - priority
        - tags


## RTorrent (ruTorrent)

Download client for torrent releases using the RTorrent (ruTorrent) torrent client.

##### ::: buildarr_radarr.config.settings.download_clients.torrent.rtorrent.RtorrentDownloadClient
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.download_clients.torrent.rtorrent.RtorrentDownloadClient
    options:
      members:
        - hostname
        - port
        - use_ssl
        - url_base
        - username
        - password
        - category
        - postimport_category
        - directory
        - recent_priority
        - older_priority
        - add_stopped

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - remove_completed_downloads
        - remove_failed_downloads
        - priority
        - tags


## SABnzbd

Download client for Usenet releases using the SABnzbd Usenet client.

##### ::: buildarr_radarr.config.settings.download_clients.usenet.sabnzbd.SabnzbdDownloadClient
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.download_clients.usenet.sabnzbd.SabnzbdDownloadClient
    options:
      members:
        - hostname
        - port
        - use_ssl
        - url_base
        - api_key
        - category
        - recent_priority
        - older_priority

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - remove_completed_downloads
        - remove_failed_downloads
        - priority
        - tags


## Torrent Blackhole

Use `.torrent` files and watch folders to manage requests to an externally managed download client.

##### ::: buildarr_radarr.config.settings.download_clients.torrent.blackhole.TorrentBlackholeDownloadClient
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.download_clients.torrent.blackhole.TorrentBlackholeDownloadClient
    options:
      members:
        - torrent_folder
        - watch_folder
        - save_magnet_files
        - magnet_file_extension
        - read_only

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - remove_completed_downloads
        - remove_failed_downloads
        - priority
        - tags


## Transmission

Download client for torrent releases using the Transmission torrent client.

##### ::: buildarr_radarr.config.settings.download_clients.torrent.transmission.TransmissionDownloadClient
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.download_clients.torrent.transmission.TransmissionDownloadClientBase
    options:
      members:
        - hostname
        - port
        - use_ssl
        - url_base
        - username
        - password
        - category
        - directory
        - recent_priority
        - older_priority
        - add_paused

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - remove_completed_downloads
        - remove_failed_downloads
        - priority
        - tags


## Usenet Blackhole

Use `.nzb` files and watch folders to manage requests to an externally managed download client.

##### ::: buildarr_radarr.config.settings.download_clients.usenet.blackhole.UsenetBlackholeDownloadClient
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.download_clients.usenet.blackhole.UsenetBlackholeDownloadClient
    options:
      members:
        - nzb_folder
        - watch_folder

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - remove_completed_downloads
        - remove_failed_downloads
        - priority
        - tags


## uTorrent

##### ::: buildarr_radarr.config.settings.download_clients.torrent.utorrent.UtorrentDownloadClient
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.download_clients.torrent.utorrent.UtorrentDownloadClient
    options:
      members:
        - hostname
        - port
        - use_ssl
        - url_base
        - username
        - password
        - category
        - postimport_category
        - recent_priority
        - older_priority
        - initial_state

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - remove_completed_downloads
        - remove_failed_downloads
        - priority
        - tags


## Vuze

Download client for torrent releases using the Vuze torrent client.

##### ::: buildarr_radarr.config.settings.download_clients.torrent.vuze.VuzeDownloadClient
    options:
      members:
        - type

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.download_clients.torrent.transmission.TransmissionDownloadClientBase
    options:
      members:
        - hostname
        - port
        - use_ssl
        - url_base
        - username
        - password
        - category
        - directory
        - recent_priority
        - older_priority
        - add_paused

##### ::: buildarr_radarr.config.settings.download_clients.base.DownloadClient
    options:
      members:
        - remove_completed_downloads
        - remove_failed_downloads
        - priority
        - tags
