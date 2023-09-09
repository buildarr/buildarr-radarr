# Copyright (C) 2023 Callum Dickinson
#
# Buildarr is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# Buildarr is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Buildarr.
# If not, see <https://www.gnu.org/licenses/>.


"""
Media management settings configuration.
"""


from __future__ import annotations

from logging import getLogger
from typing import Any, Dict, List, Optional, Set

import radarr

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr
from pydantic import Field
from typing_extensions import Self

from ...api import radarr_api_client
from ...secrets import RadarrSecrets
from ..types import RadarrConfigBase

logger = getLogger(__name__)


class ColonReplacement(BaseEnum):
    delete = "delete"
    dash = "dash"
    space_dash = "spaceDash"
    space_dash_space = "spaceDashSpace"


class PropersAndRepacks(BaseEnum):
    prefer_and_upgrade = "preferAndUpgrade"
    do_not_upgrade_automatically = "doNotUpgrade"
    do_not_prefer = "doNotPrefer"


class RescanFolderAfterRefresh(BaseEnum):
    always = "always"
    after_manual_refresh = "afterManual"
    never = "never"


class ChangeFileDate(BaseEnum):
    none = "none"
    in_cinemas_date = "cinemas"
    physical_release_date = "releease"


class ChmodFolder(BaseEnum):
    drwxr_xr_x = "755"
    drwxrwxr_x = "775"
    drwxrwx___ = "770"
    drwxr_x___ = "750"
    drwxrwxrwx = "777"

    @classmethod
    def validate(cls, v: Any) -> ChmodFolder:
        """
        Ensure that octal and decimal integers are both read properly by Buildarr.
        """
        try:
            return cls(oct(v)[2:] if isinstance(v, int) else v)
        except ValueError:
            try:
                return cls[v.replace("-", "_")]
            except (TypeError, KeyError):
                raise ValueError(f"Invalid {cls.__name__} name or value: {v}") from None


class RootFoldersSettings(RadarrConfigBase):
    """
    Root folders are paths used by Radarr as either a target folder
    for newly downloaded releases, or a source folder for Radarr to scan existing media.

    Root folders are assigned to releases when they are submitted for monitoring in Radarr.

    ```yaml
    radarr:
      settings:
        media_management:
          root_folders:
            delete_unmanaged: false
            definitions:
              - /path/to/movies
    ```
    """

    delete_unmanaged: bool = False
    """
    Delete root folders from the remote Radarr instance if
    they are not explicitly defined in Buildarr.

    Before enabling this option, ensure all the root folders
    you want Radarr to scan are defined in Buildarr,
    as Radarr might remove imported media from its database
    when root folder definitions are deleted.

    If unsure, leave set to the default of `false`.
    """

    definitions: Set[NonEmptyStr] = set()
    """
    Define root folder paths to add to Radarr here.
    """

    def update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        changed = False
        with radarr_api_client(secrets=secrets) as api_client:
            rootfolder_api = radarr.RootFolderApi(api_client)
            rootfolder_ids: Dict[str, int] = {
                api_rootfolder.path: api_rootfolder.id
                for api_rootfolder in rootfolder_api.list_root_folder()
            }
            for i, root_folder in enumerate(self.definitions):
                if root_folder in rootfolder_ids:
                    logger.debug("%s[%i]: %s (exists)", tree, i, repr(str(root_folder)))
                else:
                    logger.info("%s[%i]: %s -> (created)", tree, i, repr(str(root_folder)))
                    rootfolder_api.create_root_folder(
                        root_folder_resource=radarr.RootFolderResource(path=root_folder),
                    )
                    changed = True
        return changed

    def delete_remote(self, tree: str, secrets: RadarrSecrets, remote: Self) -> bool:
        changed = False
        with radarr_api_client(secrets=secrets) as api_client:
            rootfolder_api = radarr.RootFolderApi(api_client)
            rootfolder_ids: Dict[str, int] = {
                api_rootfolder.path: api_rootfolder.id
                for api_rootfolder in rootfolder_api.list_root_folder()
            }
            local_rootfolders = set(self.definitions)
            i = -1
            for root_folder, rootfolder_id in rootfolder_ids.items():
                if root_folder not in local_rootfolders:
                    if self.delete_unmanaged:
                        logger.info("%s[%i]: %s -> (deleted)", tree, i, repr(str(root_folder)))
                        rootfolder_api.delete_root_folder(id=rootfolder_id)
                        changed = True
                    else:
                        logger.debug("%s[%i]: %s (unmanaged)", tree, i, repr(str(root_folder)))
                    i -= 1
        return changed


class RadarrMediaManagementSettings(RadarrConfigBase):
    # Naming, file management and root folder configuration.
    #
    # For more information on how to configure this, check the plugin documentation.

    # Movie Naming
    rename_movies: bool = False
    """
    Rename imported files to the defined standard format.

    Radarr will use the existing file name if renaming is disabled.
    """

    replace_illegal_characters: bool = True
    """
    Replace illegal characters within the file name.

    If set to `false`, Radarr will remove them instead.
    """

    colon_replacement: ColonReplacement = ColonReplacement.delete
    """
    Replace or delete full colons (`:`) in release titles with alternative characters
    when saving files.

    Values:

    * `delete` - Delete without replacement (e.g. `One:Two` → `OneTwo`) (default)
    * `dash` - Replace with a dash (e.g. `One:Two` → `One-Two`)
    * `dash-space` - Replace with a dash and a space (e.g. `One:Two` → `One- Two`)
    * `space-dash-space` - Replace with a space-separated dash (e.g. `One:Two` → `One - Two`)
    """

    standard_movie_format: NonEmptyStr = (
        "{Movie Title} ({Release Year}) {Quality Full}"  # type: ignore[assignment]
    )
    """
    File renaming format for a standard movie file.
    """

    movie_folder_format: NonEmptyStr = "{Movie Title} ({Release Year})"  # type: ignore[assignment]
    """
    Renaming format for a movie folder.
    """

    # Folders
    create_missing_movie_folders: bool = False
    """
    Create missing movie folders during disk scan.
    """

    delete_empty_folders: bool = False
    """
    Delete empty media folders during disk scan and when episode files are deleted.
    """

    # Importing
    skip_free_space_check: bool = False
    """
    Skip the free space check for the movie root folder.

    Only enable when Radarr is unable to detect free space from your series root folder.
    """

    minimum_free_space: int = Field(100, ge=100)  # MB
    """
    Prevent import if it would leave less than the specified amount of disk space available
    (in megabytes).

    Minimum value is 100 MB.
    """

    use_hardlinks: bool = True
    """
    Use hard links when trying to copy downloaded media files from torrents
    that are still being seeded.

    Using hard links saves a large amount of disk space due to having only one physical copy
    of the data accessible from multiple locations.

    However, using hard links requires that the following conditions are met in your setup:

    * Torrent folders and root folders are on the same physical filesystem.
    * When using containers, both containers use the same directory tree structure for all folders
      (e.g. `/path/to/torrents` and `/path/to/movies` must be located at the same paths
      according to both containers).

    !!! note

        Occasionally, file locks may prevent renaming files that are being seeded.
        You may temporarily disable seeding and use Radarr's rename function as a work around.
    """

    import_using_script: bool = False
    """
    Copy files for importing using a script (e.g. for transcoding).
    """

    import_script_path: Optional[str] = None
    """
    The path to the script for use for importing.

    Required when `import_using_script` is set to `true`.
    """

    import_extra_files: bool = False
    """
    Import matching extra files (subtitles, `.nfo` file, etc) after importing an episode file.
    """

    # File Management
    unmonitor_deleted_movies: bool = False
    """
    When set to `true`, movies deleted from disk are automatically unmonitored in Radarr.
    """

    propers_and_repacks: PropersAndRepacks = PropersAndRepacks.prefer_and_upgrade
    """
    Whether or not to automatically upgrade to Propers/Repacks.

    Values:

    * `prefer-and-upgrade` - Automatically upgrade to propers/repacks
    * `do-not-upgrade-automatically` - Prefer propers/repacks,
      but do not upgrade to them automatically
    * `do-not-prefer` - Sort by custom format score over propers/repacks
    """

    analyze_video_files: bool = True
    """
    Extract video information such as resolution, runtime and codec information
    from files.

    This requires Radarr to read parts of the file, which may cause high disk
    or network activity during scans.
    """

    rescan_folder_after_refresh: RescanFolderAfterRefresh = RescanFolderAfterRefresh.always
    """
    Rescan the movie folder after refreshing the series.

    Values:

    * `always`
    * `after-manual-refresh`
    * `never`

    !!! warning

        Radarr will not automatically detect changes to files
        unless this attribute is set to `always`.
    """

    change_file_date: ChangeFileDate = ChangeFileDate.none
    """
    Change file date on import/rescan.

    Values:

    * `none`
    * `in-cinemas-date`
    * `physical-release-date`
    """

    recycling_bin: Optional[NonEmptyStr] = None
    """
    Episode files will go here when deleted instead of being permanently deleted.
    """

    recycling_bin_cleanup: int = Field(7, ge=0)  # days
    """
    Files in the recycle bin older than the selected number of days
    will be cleaned up automatically.

    Set to `0` to disable automatic cleanup.
    """

    # Permissions
    set_permissions: bool = False
    """
    Set whether or not `chmod` should run when files are imported/renamed.

    If you're unsure what this and the `chmod`/`chown` series of attributes do,
    do not alter them.
    """

    chmod_folder: ChmodFolder = ChmodFolder.drwxr_xr_x
    """
    Permissions to set on media folders and files during import/rename.
    File permissions are set without execute bits.

    This only works if the user running Radarr is the owner of the file.
    Ideally, the download client should already set these permissions appropriately.

    Values:

    * `drwxr-xr-x`/`755`
    * `drwxrwxr-x`/`775`
    * `drwxrwx---`/`770`
    * `drwxr-x---`/`750`
    * `drwxrwxrwx`/`777`
    """

    chown_group: Optional[str] = None
    """
    Group name or GID. Use GID for remote file systems.

    This only works if the user running Radarr is the owner of the file.
    Ideally, the download client should be using  the same group as Radarr.
    """

    root_folders: RootFoldersSettings = RootFoldersSettings()
    """
    Root folder settings should be defined here.
    """

    _naming_remote_map: List[RemoteMapEntry] = [
        # Episode Naming
        ("rename_movies", "renameMovies", {}),
        ("replace_illegal_characters", "replaceIllegalCharacters", {}),
        ("colon_replacement", "colonReplacementFormat", {}),
        ("standard_movie_format", "standardMovieFormat", {}),
        ("movie_folder_format", "movieFolderFormat", {}),
    ]
    _mediamanagement_remote_map: List[RemoteMapEntry] = [
        # Folders
        ("create_missing_movie_folders", "createEmptyMovieFolders", {}),
        ("delete_empty_folders", "deleteEmptyFolders", {}),
        # Importing
        ("skip_free_space_check", "skipFreeSpaceCheckWhenImporting", {}),
        ("minimum_free_space", "minimumFreeSpaceWhenImporting", {}),
        ("use_hardlinks", "copyUsingHardlinks", {}),
        ("import_using_script", "useScriptImport", {}),
        (
            "import_script_path",
            "scriptImportPath",
            {"decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        ("import_extra_files", "importExtraFiles", {}),
        # File Management
        ("unmonitor_deleted_movies", "autoUnmonitorPreviouslyDownloadedMovies", {}),
        ("propers_and_repacks", "downloadPropersAndRepacks", {}),
        ("analyze_video_files", "enableMediaInfo", {}),
        ("rescan_folder_after_refresh", "rescanAfterRefresh", {}),
        ("change_file_date", "fileDate", {}),
        (
            "recycling_bin",
            "recycleBin",
            {"decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
        ("recycling_bin_cleanup", "recycleBinCleanupDays", {}),
        # Permissions
        ("set_permissions", "setPermissionsLinux", {}),
        ("chmod_folder", "chmodFolder", {}),
        (
            "chown_group",
            "chownGroup",
            {"decoder": lambda v: v or None, "encoder": lambda v: v or ""},
        ),
    ]

    @classmethod
    def from_remote(cls, secrets: RadarrSecrets) -> Self:
        with radarr_api_client(secrets=secrets) as api_client:
            api_naming_config = radarr.NamingConfigApi(api_client).get_naming_config()
            api_mediamanagement_config = radarr.MediaManagementConfigApi(
                api_client,
            ).get_media_management_config()
        return cls(
            # Episode Naming
            **cls.get_local_attrs(
                remote_map=cls._naming_remote_map,
                remote_attrs=api_naming_config.to_dict(),
            ),
            # All other sections except Root Folders
            **cls.get_local_attrs(
                remote_map=cls._mediamanagement_remote_map,
                remote_attrs=api_mediamanagement_config.to_dict(),
            ),
            # Root Folders
            root_folders=RootFoldersSettings.from_remote(secrets=secrets),
        )

    def update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        return any(
            [
                # Episode Naming
                self._update_remote_naming(
                    tree=tree,
                    secrets=secrets,
                    remote=remote,
                    check_unmanaged=check_unmanaged,
                ),
                # All other sections except Root Folders
                self._update_remote_mediamanagement(
                    tree=tree,
                    secrets=secrets,
                    remote=remote,
                    check_unmanaged=check_unmanaged,
                ),
                # Root Folders
                self.root_folders.update_remote(
                    tree=f"{tree}.root_folders",
                    secrets=secrets,
                    remote=remote.root_folders,
                    check_unmanaged=check_unmanaged,
                ),
            ],
        )

    def _update_remote_naming(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        updated, updated_attrs = self.get_update_remote_attrs(
            tree=tree,
            remote=remote,
            remote_map=self._naming_remote_map,
            check_unmanaged=check_unmanaged,
            set_unchanged=True,
        )
        if updated:
            with radarr_api_client(secrets=secrets) as api_client:
                naming_api = radarr.NamingConfigApi(api_client)
                api_naming_config = naming_api.get_naming_config()
                naming_api.update_naming_config(
                    id=str(api_naming_config.id),
                    naming_config_resource=radarr.NamingConfigResource.from_dict(
                        {**api_naming_config.to_dict(), **updated_attrs},
                    ),
                )
            return True
        return False

    def _update_remote_mediamanagement(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        updated, updated_attrs = self.get_update_remote_attrs(
            tree,
            remote,
            self._mediamanagement_remote_map,
            check_unmanaged=check_unmanaged,
            set_unchanged=True,
        )
        if updated:
            with radarr_api_client(secrets=secrets) as api_client:
                mediamanagement_api = radarr.MediaManagementConfigApi(api_client)
                api_mediamanagement_config = mediamanagement_api.get_media_management_config()
                mediamanagement_api.update_media_management_config(
                    id=str(api_mediamanagement_config.id),
                    media_management_config_resource=(
                        radarr.MediaManagementConfigResource.from_dict(
                            {**api_mediamanagement_config.to_dict(), **updated_attrs},
                        )
                    ),
                )
            return True
        return False
