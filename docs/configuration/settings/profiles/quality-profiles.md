# Quality Profiles

##### ::: buildarr_radarr.config.settings.profiles.quality_profiles.RadarrQualityProfilesSettings
    options:
      members:
        - delete_unmanaged
        - definitions

## Creating a quality profile

A basic quality profile looks something like this.

```yaml
...
  quality_profiles:
    SD:
      upgrades_allowed: true
      upgrade_until_quality: Bluray-480p
      qualities:
        - Bluray-480p
        - DVD
        - name: WEB 480p
          members:
            - WEBDL-480p
            - WEBRip-480p
      custom_formats:
        - name: remaster
          score: 0
      language: english
```

For more insight into reasonable values for quality profiles,
refer to these guides from [WikiArr](https://wiki.servarr.com/radarr/settings#quality-profiles)
and TRaSH-Guides ([general](https://trash-guides.info/Radarr/radarr-setup-quality-profiles),
[anime](https://trash-guides.info/Radarr/radarr-setup-quality-profiles-anime)).

##### ::: buildarr_radarr.config.settings.profiles.quality_profiles.QualityProfile
    options:
      members:
        - upgrades_allowed

## Quality Levels

Quality levels are used to prioritise media releases by resolution, bitrate and
distribution method.

```yaml
...
  qualities:
    - Bluray-480p
    - name: WEB 480p
      members:
        - WEBDL-480p
        - WEBRip-480p
```

In Buildarr, the quality listed first (at the top) is given the highest priority, with
subsequent qualities given lower priority. Quality levels not explicitly defined are
disabled (not downloaded).

Radarr supports grouping multiple qualities together to give them the same priority.
In Buildarr, these are expressed by giving a `name` to the group, and listing the
member quality levels under the `members` attribute.

For details on the available quality levels, refer to
[this guide](https://wiki.servarr.com/radarr/settings#qualities-defined) on WikiArr.

##### ::: buildarr_radarr.config.settings.profiles.quality_profiles.QualityProfile
    options:
      members:
        - upgrade_until_quality
        - qualities

## Custom Formats

##### ::: buildarr_radarr.config.settings.profiles.quality_profiles.QualityProfile
    options:
      members:
        - minimum_custom_format_score
        - upgrade_until_custom_format_score
        - custom_formats

##### ::: buildarr_radarr.config.settings.profiles.quality_profiles.CustomFormatScore
    options:
      members:
        - name
        - score

## Language

##### ::: buildarr_radarr.config.settings.profiles.quality_profiles.QualityProfile
    options:
      members:
        - language
