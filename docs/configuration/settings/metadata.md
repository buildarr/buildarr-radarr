# Metadata

Metadata-related configuration for Radarr is defined here.

Optionally, Radarr can be configured to create metadata files alongside your media files
in a variety of formats, to suit the media player you intend to use.

```yaml
radarr:
  settings:
    metadata:
      certification_country: us
      emby_legacy:
        ...
      kodi_emby:
        ...
      roksbox:
        ...
      wdtv:
        ...
```

Multiple of these can be configured at a time.

##### ::: buildarr_radarr.config.settings.metadata.RadarrMetadataSettings
    options:
      members:
        - certification_country


## Emby (Legacy)

Output metadata files in the legacy Emby metadata format.

```yaml
radarr:
  settings:
    metadata:
      emby_legacy:
        enable: true
        movie_metadata: true
```

##### ::: buildarr_radarr.config.settings.metadata.base.Metadata
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.metadata.emby_legacy.EmbyLegacyMetadata
    options:
      members:
        - movie_metadata


## Kodi (XBMC) / Emby

Output metadata files in a format suitable for Kodi (XBMC) or Emby.

```yaml
radarr:
  settings:
    metadata:
      kodi_emby:
        enable: true
        movie_metadata: true
        movie_metadata_url: true
        movie_metadata_language: english
        movie_images: true
        use_movie_nfo: true
        add_collection_name: true
```

##### ::: buildarr_radarr.config.settings.metadata.base.Metadata
    options:
      members:
        - enable

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

Output metadata files in a format suitable for Roksbox.

```yaml
radarr:
  settings:
    metadata:
      roksbox:
        enable: true
        movie_metadata: true
        movie_images: true
```

##### ::: buildarr_radarr.config.settings.metadata.base.Metadata
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.metadata.roksbox.RoksboxMetadata
    options:
      members:
        - movie_metadata
        - movie_images


## WDTV

Output metadata files in a format suitable for WDTV.

```yaml
radarr:
  settings:
    metadata:
      wdtv:
        enable: true
        movie_metadata: true
        movie_images: true
```

##### ::: buildarr_radarr.config.settings.metadata.base.Metadata
    options:
      members:
        - enable

##### ::: buildarr_radarr.config.settings.metadata.wdtv.WdtvMetadata
    options:
      members:
        - movie_metadata
        - movie_images
