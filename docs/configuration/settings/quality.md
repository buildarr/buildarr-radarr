# Quality

Quality definitions are used to set the permitted bit rates for each quality level.

These can either be set manually within Buildarr, or profiles can be imported from TRaSH-Guides.

```yaml
radarr:
  settings:
    quality:
      trash_id: aed34b9f60ee115dfa7918b742336277  # movie
      definitions:
        Bluray-480p: # "Quality" column name (not "Title")
          # title: null  # Optional. Set when you want to change the display name.
          min: 2
          preferred: 95
          max: 100
        # Add additional override quality definitions here
```

Quality definition profiles retrieved from TRaSH-Guides are automatically
kept up to date by Buildarr, with the latest values being pushed to Radarr
on an update run.

For more information, refer to the guides from
[WikiArr](https://wiki.servarr.com/Radarr/settings#quality-1)
and [TRaSH-Guides](https://trash-guides.info/Radarr/Radarr-Quality-Settings-File-Size/).

## TRaSH-Guides quality definition profiles

TRaSH-Guides provides [presets for Radarr quality definitions](https://github.com/TRaSH-/Guides/tree/master/docs/json/radarr/quality-size)
ideal for different use cases.

| Type    | Trash ID                          |
| ------- | --------------------------------- |
| `movie` | `aed34b9f60ee115dfa7918b742336277`|

Using only the Trash ID, Buildarr can import these profiles and use them
to configure the Radarr instance, making it much more convenient
to get started with a known-good configuration.

```yaml
radarr:
  settings:
    quality:
      trash_id: aed34b9f60ee115dfa7918b742336277  # movie
```

When using Buildarr daemon it will also automatically update the Radarr instance
whenever the guide's recommendations change, as it always uses the latest version
on each update run.

##### ::: buildarr_radarr.config.settings.quality.RadarrQualitySettings
    options:
      members:
        - trash_id

## Overriding quality definitions

##### ::: buildarr_radarr.config.settings.quality.QualityDefinition
    options:
      members:
        - title
        - min
        - preferred
        - max
