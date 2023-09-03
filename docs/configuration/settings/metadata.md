# Metadata

Radarr can output metadata alongside media files in a variety of formats,
to suit the media player you intend to use.

Multiple of these can be configured at a time.

To enable a metadata format, set `enable` to `true` in the configuration block in Buildarr.

## Emby (Legacy)

##### ::: buildarr_radarr.config.settings.metadata.emby_legacy.EmbyLegacyMetadata
    options:
      members:
        - movie_metadata

## Kodi (XBMC) / Emby

##### ::: buildarr_radarr.config.settings.metadata.kodi_emby.KodiEmbyMetadata
    options:
      members:
        - movie_metadata
        - movie_metadata_url
        - movie_metadata_language
        - movie_images
        - use_movie_nfo
        - add_collection_name

## Roksbox

##### ::: buildarr_radarr.config.settings.metadata.roksbox.RoksboxMetadata
    options:
      members:
        - movie_metadata
        - movie_images

## WDTV

##### ::: buildarr_radarr.config.settings.metadata.wdtv.WdtvMetadata
    options:
      members:
        - movie_metadata
        - movie_images
