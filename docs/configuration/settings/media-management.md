# Media Management

Naming, file management and root folder configuration.

```yaml
radarr:
  settings:
    media_management:
      rename_movies: true
      replace_illegal_characters: true
      colon_replacement: space-dash-space
      standard_movie_format: "\
        {Movie CleanTitle} - \
        {Edition Tags }\
        {[Custom Formats] }\
        {[Quality Full] }\
        {[MediaInfo 3D] }\
        {[MediaInfo VideoDynamicRangeType] }\
        [{Mediainfo AudioCodec}{ Mediainfo AudioChannels}]\
        { [Mediainfo VideoCodec]}\
        { [Release Group]} - \
        Default"
      movie_folder_format: '{Movie CleanTitle} ({Release Year}) [imdbid-{ImdbId}]'
      create_missing_movie_folders: false
      delete_empty_folders: false
      skip_free_space_check: false
      minimum_free_space: 100  # MB
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
      recycling_bin_cleanup: 28  # days
      set_permissions: false
      chmod_folder: drwxr-xr-x
      chown_group: null
      root_folders:
        delete_unmanaged: true
        definitions:
          - /path/to/movies
```

For more information on how to configure these options correctly, refer to these guides from [WikiArr](https://wiki.servarr.com/radarr/settings#media-management) and [TRaSH-Guides](https://trash-guides.info/Radarr/Radarr-recommended-naming-scheme).

## Settings

##### ::: buildarr_radarr.config.settings.media_management.RadarrMediaManagementSettings
    options:
      members:
        - rename_movies
        - replace_illegal_characters
        - colon_replacement
        - standard_movie_format
        - movie_folder_format
        - create_missing_movie_folders
        - delete_empty_folders
        - skip_free_space_check
        - minimum_free_space
        - use_hardlinks
        - import_using_script
        - import_script_path
        - import_extra_files
        - unmonitor_deleted_movies
        - propers_and_repacks
        - analyze_video_files
        - rescan_folder_after_refresh
        - change_file_date
        - recycling_bin
        - recycling_bin_cleanup
        - set_permissions
        - chmod_folder
        - chown_group

## Root Folders

##### ::: buildarr_radarr.config.settings.media_management.RootFoldersSettings
    options:
      members:
        - delete_unmanaged
        - definitions
