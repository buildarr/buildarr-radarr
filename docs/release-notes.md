# Release Notes (Buildarr Radarr Plugin)

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

* Add support for the `Movies` category in Newznab/Torznab indexers ([#11](https://github.com/buildarr/buildarr-prowlarr/pull/11))


## [v0.1.1](https://github.com/buildarr/buildarr-radarr/releases/tag/v0.1.1) - 2023-09-09

This release fixes an issue where if you have unmanaged root folders on a Buildarr instance that are not defined in Buildarr, Buildarr would print a misleading log message about it being modified in some way.

These root folders are not being changed, and the logging has been improved to reflect that.

### Changed

* Improve CLI and secrets type handling ([#5](https://github.com/buildarr/buildarr-radarr/pull/5))
* Fix misleading root folder state logging ([#6](https://github.com/buildarr/buildarr-radarr/pull/6))


## [v0.1.0](https://github.com/buildarr/buildarr-radarr/releases/tag/v0.1.0) - 2023-09-09

First release of the Radarr plugin for Buildarr.
