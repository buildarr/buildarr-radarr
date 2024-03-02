# Release Notes (Buildarr Radarr Plugin)

## [v0.2.5](https://github.com/buildarr/buildarr-radarr/releases/tag/v0.2.5) - 2024-03-02

This release fixes the following issues:

* Fixed an issue where the preferred bitrate in quality definitions was not being applied to Radarr instances. Thanks to **@ChadTaljaardt** for the contribution.
* Made username/password authentication optional for qBittorrent download clients, as qBittorrent allows API access without authentication in certain cases.

### Changed

* Add missing preferred quality size definition ([#47](https://github.com/buildarr/buildarr-radarr/pull/47))
* Update Poetry and lock file ([#51](https://github.com/buildarr/buildarr-radarr/pull/51))
* Make auth optional for qBittorrent download clients ([#53](https://github.com/buildarr/buildarr-radarr/pull/53))


## [v0.2.4](https://github.com/buildarr/buildarr-radarr/releases/tag/v0.2.4) - 2023-12-10

This release fixes the following issues:

* Add error handling for when an unsupported condition type is found in a dynamic (loaded from TRaSH-Guides) or remote custom format, so the error message is easier to understand.
    * Buildarr is not capable of ignoring remote custom formats with unsupported condition types defined on them at the moment, so return an error instead. If this happens, it is recommended to [create a bug report](https://github.com/buildarr/buildarr-radarr/issues/new).
* If an unsupported resource type (download client, indexer, notification) is found on the remote instance, ignore it (while logging the implementation name), instead of returning an error.

### Changed

* Improve handling of unsupported resource types ([#43](https://github.com/buildarr/buildarr-radarr/pull/43))


## [v0.2.3](https://github.com/buildarr/buildarr-radarr/releases/tag/v0.2.3) - 2023-12-02

This release adds support for defining a URL base for the Radarr instance in the Buildarr configuration, using the `url_base` host configuration attribute.

This allows Radarr instances with APIs available under a custom path (e.g. `http://localhost:7878/radarr`) to be managed by Buildarr.

### Changed

* Add Radarr instance URL base support ([#38](https://github.com/buildarr/buildarr-radarr/pull/38))


## [v0.2.2](https://github.com/buildarr/buildarr-radarr/releases/tag/v0.2.2) - 2023-11-27

This release fixes the following issues:

* Fix an attribute reading bug that was preventing management of the following download client types:
    * FreeBox
    * Hadouken
    * qBittorrent
    * rTorrent
    * uTorrent
    * NZBGet
    * NZBVortex
    * SABnzbd

### Changed

* Fix reading download client attributes ([#34](https://github.com/buildarr/buildarr-radarr/pull/34))


## [v0.2.1](https://github.com/buildarr/buildarr-radarr/releases/tag/v0.2.1) - 2023-11-13

This release fixes the following issues:

* Fix loading the default score of custom formats from TRaSH-Guides metadata, which was broken due to a deprecated metadata field Buildarr was using that was removed.
* Permanently fix Torznab/Newznab indexer category parsing by making it not error when an unknown category ID is found on the remote instance.
* Allow the Radarr-native category name (e.g. `Movies/BluRay`) to be defined directly in Buildarr, instead of the Buildarr-native names (e.g. `Movies-Bluray`). The old names are still supported.
* Fix managing the `remove_year` attribute on Newznab/Torznab indexers, which was being ignored in previous releases.
* Fix dumping Radarr instance configurations using the CLI, which was failing due to a validation regression introduced in the previous release.

The CLI command for dumping Radarr instance configurations has also been improved, and can now auto-fetch Radarr instance API keys by simply leaving the API key blank, and pressing Enter when prompted. Note that this will only work on Radarr instances that have authentication disabled.

As this release of the Radarr plugin uses the latest plugin API features, Buildarr v0.7.1 or later is required for this release.

### Changed

* Fix and improve configuration dumping ([#26](https://github.com/buildarr/buildarr-radarr/pull/26))
* Fix getting TRaSH-Guides custom format default score ([#28](https://github.com/buildarr/buildarr-radarr/pull/28))
* Fix Newznab/Torznab indexer bugs ([#25](https://github.com/buildarr/buildarr-radarr/pull/25))


## [v0.2.0](https://github.com/buildarr/buildarr-radarr/releases/tag/v0.2.0) - 2023-11-12

This release introduces basic support for managing Radarr V5 instances.

All configuration parameter types currently supported by this plugin can be used with Radarr V5.

In addition, Buildarr is capable of automatically configuring your Radarr V5 instances to use the `external` authentication mode,
making it easier to automatically integrate with external authentication providers that support forward auth, such as Authentik or KeyCloak.

Currently, Radarr V5 support has the following issues:

* Release Profiles are not yet implemented.
    * The Radarr V4 equivalent, indexer restrictions, are also not yet implemented.
* Due to an API specification change with Radarr V5, and resources managed by Buildarr that contain passwords or API keys cannot be idempotently updated at this time. Every time Buildarr runs, these resources will be updated. [See this GitHub issue](https://github.com/buildarr/buildarr-radarr/issues/20) for more information.

Other changes:

* Update the Radarr plugin so that it is compatible with [Buildarr v0.7.0](https://buildarr.github.io/release-notes/#v070-2023-11-12).

### Added

* Add basic Radarr V5 support ([#16](https://github.com/buildarr/buildarr-radarr/pull/16))

### Changed

* Add Buildarr v0.7.0 support ([#19](https://github.com/buildarr/buildarr-radarr/pull/19))
* Remove custom handlers for `NameEmail` attributes ([#21](https://github.com/buildarr/buildarr-radarr/pull/21))


## [v0.1.2](https://github.com/buildarr/buildarr-radarr/releases/tag/v0.1.2) - 2023-11-05

This release fixes the following issues:

* Allow the `Movies` category group to be defined on Newznab/Torznab indexers (and Prowlarr managed indexers)

### Changed

* Add support for the `Movies` category in Newznab/Torznab indexers ([#11](https://github.com/buildarr/buildarr-radarr/pull/11))


## [v0.1.1](https://github.com/buildarr/buildarr-radarr/releases/tag/v0.1.1) - 2023-09-09

This release fixes an issue where if you have unmanaged root folders on a Buildarr instance that are not defined in Buildarr, Buildarr would print a misleading log message about it being modified in some way.

These root folders are not being changed, and the logging has been improved to reflect that.

### Changed

* Improve CLI and secrets type handling ([#5](https://github.com/buildarr/buildarr-radarr/pull/5))
* Fix misleading root folder state logging ([#6](https://github.com/buildarr/buildarr-radarr/pull/6))


## [v0.1.0](https://github.com/buildarr/buildarr-radarr/releases/tag/v0.1.0) - 2023-09-09

First release of the Radarr plugin for Buildarr.
