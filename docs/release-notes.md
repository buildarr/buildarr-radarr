# Release Notes (Buildarr Radarr Plugin)

## [v0.1.1](https://github.com/buildarr/buildarr-radarr/releases/tag/v0.1.1) - 2023-09-09

This release fixes an issue where if you have unmanaged root folders on a Buildarr instance that are not defined in Buildarr, Buildarr would print a misleading log message about it being modified in some way.

These root folders are not being changed, and the logging has been improved to reflect that.

### Changed

* Improve CLI and secrets type handling ([#5](https://github.com/buildarr/buildarr-radarr/pull/5))
* Fix misleading root folder state logging ([#6](https://github.com/buildarr/buildarr-radarr/pull/6))


## [v0.1.0](https://github.com/buildarr/buildarr-radarr/releases/tag/v0.1.0) - 2023-09-09

First release of the Radarr plugin for Buildarr.
