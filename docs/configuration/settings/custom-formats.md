# Custom Formats

Custom formats are the primary method for controlling how releases are selected and prioritised in Radarr.

Criteria can be something as simple as a single preferred word, or as complex as multiple regular expressions
matching for a variety of complementing media attributes, and in any case, Radarr allows you to flexibly determine
how releases should be picked when managing movies.

!!! note

    For more information on how to use custom formats in Radarr, refer to
    [How to setup Quality Profiles](https://trash-guides.info/Radarr/radarr-setup-quality-profiles).

In Buildarr, custom formats can be configured using two different methods:
[importing from TRaSH-Guides](#importing-from-trash-guides), or [manually definitions](#manual-definitions).

```yaml
radarr:
  settings:
    custom_formats:
      delete_unmanaged: true
      definitions:
        # Import custom formats from TRaSH-Guides.
        remaster:
          trash_id: 570bc9ebecd92723d2d21500f4be314c
          # `default_score` is 25, as set in the TRaSH-Guides custom format.
        4k-remaster:
          trash_id: eca37840c13c6ef2dd0262b141a5482f
          default_score: 26  # Override default score from TRaSH-Guides custom format.
        # Manually define custom formats.
        br-disk:
          default_score: -10000
          conditions:
            br-disk:
              type: quality-modifier
              modifier: BRDISK
              negate: false
              required: false
        3d:
          # No `default_score` defined on manually defined custom format: default to 0.
          conditions:
            bluray-3d:
              type: release-title
              regex: '\\b(BluRay3D)\\b'
              negate: false
              required: false
```

The following attributes determine how custom formats are managed by Buildarr.

##### ::: buildarr_radarr.config.settings.custom_formats.RadarrCustomFormatsSettings
    options:
      members:
        - delete_unmanaged
        - definitions

## Quality Profiles

When using custom formats in quality profiles, they are assigned a score value to configure how releases are prioritised.

```yaml
radarr:
  settings:
    profiles:
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
              - name: remaster  # No `score` defined: Use `default_score` from the custom format.
              - name: 4k-remaster
              # Unwanted
              - name: br-disk
              - name: 3d
                score: -10000  # Inverse of maximum allowed score, to ensure it is never selected.
            language: english
```

For more information on how to use custom formats to filter and prioritise media in Buildarr,
check the [Quality Profiles](profiles/quality-profiles.md#custom-formats) documentation.

## Importing from TRaSH-Guides

TRaSH-Guides contains a large collection of pre-made
[custom formats](https://trash-guides.info/Radarr/Radarr-collection-of-custom-formats),
to make it easier for new users to get started with configuring Radarr correctly.

Buildarr makes it even easier by providing a convenient way to automatically
import these custom formats, using the `trash_id` attribute.

Simply create a custom format with any desired name, set the corresponding `trash_id` attribute,
and Buildarr will take care of everything.

Using Buildarr daemon, these custom formats are also kept automatically up to date
whenever they are changed in the guides, eliminating the need to manually check
and update your configuration.

```yaml
...
  custom_formats:
    delete_unmanaged: true
    definitions:
      # Import custom formats from TRaSH-Guides.
      remaster:
        trash_id: 570bc9ebecd92723d2d21500f4be314c
        # `default_score` is 25, as set in the TRaSH-Guides custom format.
      4k-remaster:
        trash_id: eca37840c13c6ef2dd0262b141a5482f
        default_score: 26  # Override default score from TRaSH-Guides custom format.
```

When using only the `trash_id` parameter, Buildarr will set the default score
and all conditions using sane defaults from TRaSH-Guides.

However, all aspects of a TRaSH-Guides imported custom format can be overridden
using the same parameters as available in [manually defining custom formats](#manual-definitions).
When overriding conditions, make sure to use the same name for the condition
as in the TRaSH-Guides definition.

##### ::: buildarr_radarr.config.settings.custom_formats.custom_format.CustomFormat
    options:
      members:
        - trash_id

## Manual Definitions

If the pre-made custom formats available online are not sufficient for your needs,
you can define a custom format completely manually in Buildarr, using the following syntax.

```yaml
...
  custom_formats:
    delete_unmanaged: true
    definitions:
      br-disk:
        default_score: -10000
        conditions:
          br-disk:
            type: quality-modifier
            modifier: BRDISK
            negate: false
            required: false
      3d:
        # No `default_score` defined on manually defined custom format: default to 0.
        include_when_renaming: true  # Set to false by default.
        delete_unmanaged_conditions: false  # Set to true by default, and should be most of the time.
        conditions:
          bluray-3d:
            type: release-title
            regex: '\\b(BluRay3D)\\b'
            negate: false
            required: false
```

##### ::: buildarr_radarr.config.settings.custom_formats.custom_format.CustomFormat
    options:
      members:
        - default_score
        - include_when_renaming
        - delete_unmanaged_conditions
        - conditions

The following sections document the custom format condition types available for use in Buildarr.

## Edition

Custom format condition for matching based on media edition.

```yaml
...
  custom_formats:
    definitions:
      edition:
        default_score: 0
        conditions:
          extended-edition:
            type: edition
            regex: '(?<!^|{)\\b(extended|uncut|directors|special|unrated|uncensored|cut|version|edition)(\\b|\\d)'
            negate: false
            required: false
```

##### ::: buildarr_radarr.config.settings.custom_formats.conditions.edition.EditionCondition
    options:
      members:
        - type
        - regex

##### ::: buildarr_radarr.config.settings.custom_formats.conditions.base.Condition
    options:
      members:
        - negate
        - required


## Indexer Flag

Custom format condition for matching based on indexer flags.

```yaml
...
  custom_formats:
    definitions:
      indexer-flags:
        default_score: 0
        conditions:
          freeleech:
            type: indexer-flag
            flag: g-freeleech
            negate: false
            required: false
```

##### ::: buildarr_radarr.config.settings.custom_formats.conditions.indexer_flag.IndexerFlagCondition
    options:
      members:
        - type
        - flag

##### ::: buildarr_radarr.config.settings.custom_formats.conditions.base.Condition
    options:
      members:
        - negate
        - required


## Language

Custom format condition for matching based on language.

```yaml
...
  custom_formats:
    definitions:
      english:
        default_score: 20
        conditions:
          english:
            type: language
            language: english
            negate: false
            required: false
      japanese:
        default_score: 10
        conditions:
          japanese:
            type: language
            language: japanese
            negate: false
            required: false
      portuguese:
        default_score: 0
        conditions:
          portuguese:
            type: language
            language: portuguese
            negate: false
            required: false
          portuguese-brazil:
            type: language
            language: portuguese-brazil
            negate: false
            required: false
```

##### ::: buildarr_radarr.config.settings.custom_formats.conditions.language.LanguageCondition
    options:
      members:
        - type
        - language

##### ::: buildarr_radarr.config.settings.custom_formats.conditions.base.Condition
    options:
      members:
        - negate
        - required


## Quality Modifier

Custom format condition for matching based on quality modifiers.

```yaml
...
  custom_formats:
    definitions:
      br-disk:
        default_score: -10000
        conditions:
          br-disk:
            type: quality-modifier
            modifier: BRDISK
            negate: false
            required: false
```

##### ::: buildarr_radarr.config.settings.custom_formats.conditions.quality_modifier.QualityModifierCondition
    options:
      members:
        - type
        - modifier

##### ::: buildarr_radarr.config.settings.custom_formats.conditions.base.Condition
    options:
      members:
        - negate
        - required


## Release Group

Custom format condition for matching based on release group.

```yaml
...
  custom_formats:
    definitions:
      release-groups:
        default_score: 1800
        conditions:
          chotab:
            type: release-group
            regex: '^(Chotab)$'
            negate: false
            required: false
          ctrlhd:
            type: release-group
            regex: '^(CtrlHD)$'
            negate: false
            required: false
```

##### ::: buildarr_radarr.config.settings.custom_formats.conditions.release_group.ReleaseGroupCondition
    options:
      members:
        - type
        - regex

##### ::: buildarr_radarr.config.settings.custom_formats.conditions.base.Condition
    options:
      members:
        - negate
        - required


## Release Title

Custom format condition for matching based on release title contents.

```yaml
...
  custom_formats:
    definitions:
      anime-groups:
        default_score: 500
        conditions:
          asakura:
            type: release-title
            regex: '\\[Asakura\\]|-Asakura\\b'
            negate: false
            required: false
          tenshi:
            type: release-title
            regex: '\\[tenshi\\]|-tenshi\\b'
            negate: false
            required: false
```

##### ::: buildarr_radarr.config.settings.custom_formats.conditions.release_title.ReleaseTitleCondition
    options:
      members:
        - type
        - regex

##### ::: buildarr_radarr.config.settings.custom_formats.conditions.base.Condition
    options:
      members:
        - negate
        - required


## Resolution

Custom format condition for matching based on media resolution.

```yaml
...
  custom_formats:
    definitions:
      1080p:
        default_score: 1000
        conditions:
          chotab:
            type: resolution
            resolution: r1080p
            negate: false
            required: false
      4k:
        default_score: -10000
        conditions:
          ctrlhd:
            type: resoltuion
            resolution: r2160p
            negate: false
            required: false
```

##### ::: buildarr_radarr.config.settings.custom_formats.conditions.resolution.ResolutionCondition
    options:
      members:
        - type
        - resolution

##### ::: buildarr_radarr.config.settings.custom_formats.conditions.base.Condition
    options:
      members:
        - negate
        - required


## Size

Custom format condition for matching based on media file size.

```yaml
...
  custom_formats:
    definitions:
      allowed-size:
        default_score: 1000
        conditions:
          allowed-size:
            type: size
            min: 10  # GB
            max: 20  # GB
            negate: false
            required: false
```

##### ::: buildarr_radarr.config.settings.custom_formats.conditions.size.SizeCondition
    options:
      members:
        - type
        - min
        - max

##### ::: buildarr_radarr.config.settings.custom_formats.conditions.base.Condition
    options:
      members:
        - negate
        - required


## Source

Custom format condition for matching based on media source type.

```yaml
...
  custom_formats:
    definitions:
      allowed-sources:
        default_score: 0
        conditions:
          blu-ray:
            type: source
            source: BLURAY
            negate: false
            required: true
```

##### ::: buildarr_radarr.config.settings.custom_formats.conditions.source.SourceCondition
    options:
      members:
        - type
        - source

##### ::: buildarr_radarr.config.settings.custom_formats.conditions.base.Condition
    options:
      members:
        - negate
        - required
