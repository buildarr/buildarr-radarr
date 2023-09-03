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
    definitions:
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

Custom formats allow for finer control of filtering and prioritising media releases.

Once you have created the custom formats you want to apply in the [Custom Formats](../custom-formats.md)
section, you can assign a score under the for that custom format within the context of the quality profile,
using the `custom_formats` attribute.

```yaml
...
  quality_profiles:
    definitions:
      HD:
        upgrades_allowed: true
        upgrade_until_quality: Bluray-1080p
        qualities:
          - Bluray-1080p
          - name: WEB 1080p
            members:
              - WEBDL-1080p
              - WEBRip-1080p
        minimum_custom_format_score: 0
        upgrade_until_custom_format_score: 10000
        custom_formats:
          # Wanted
          - name: remaster
            score: 25
          - name: 4k-remaster
            # If `score` is unset, use `default_score` as defined in the Buildarr custom format definition.
            # score: 25
          # Unwanted
          - name: br-disk
            score: -10000  # Inverse of maximum allowed score, to ensure it is never selected.
          - name: lq
            score: -10000
          - name: 3d
            score: -10000
        language: english
```

If a release matches that custom format, it is *applied* to the release, i.e. the score
associated with it is added to the total for that release.

If the assigned score is positive, it will increase the priority of the
release, while if it is negative, it will decrease the priority.
The sum of all applied custom format scores determines the priority of the release
(higher is better).

Custom formats that exist but have not been assigned a score, or assigned a score of 0,
are still evaluated against releases, but are purely informational in nature
and do not influence release selection.

### Settings

The following settings control how custom formats are applied to the quality profile.

##### ::: buildarr_radarr.config.settings.profiles.quality_profiles.QualityProfile
    options:
      members:
        - minimum_custom_format_score
        - upgrade_until_custom_format_score

### Score Definitions

##### ::: buildarr_radarr.config.settings.profiles.quality_profiles.CustomFormatScore
    options:
      members:
        - name
        - score

## Language

Quality profiles also allow for explicit filtering by media language.

Prioritisation based on language (e.g. prefer Japanese but also allow English),
however, should be done using custom formats.

##### ::: buildarr_radarr.config.settings.profiles.quality_profiles.QualityProfile
    options:
      members:
        - language
