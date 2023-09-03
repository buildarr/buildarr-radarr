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
Delay profiles settings configuration.
"""


from __future__ import annotations

from logging import getLogger
from typing import Any, Dict, List, Mapping, Set

import radarr

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr
from pydantic import Field
from typing_extensions import Self

from ....api import radarr_api_client
from ....secrets import RadarrSecrets
from ...types import RadarrConfigBase

logger = getLogger(__name__)


class PreferredProtocol(BaseEnum):
    """
    Enumeration for enabled and preferred protocols in delay profiles.
    """

    usenet_prefer = 0
    torrent_prefer = 1
    usenet_only = 2
    torrent_only = 3

    @classmethod
    def decode(
        cls,
        usenet_enabled: bool,
        torrent_enabled: bool,
        preferred_protocol: str,
    ) -> PreferredProtocol:
        return {
            (True, True, "usenet"): PreferredProtocol.usenet_prefer,
            (True, True, "unknown"): PreferredProtocol.usenet_prefer,
            (True, True, "torrent"): PreferredProtocol.torrent_prefer,
            (True, False, "usenet"): PreferredProtocol.usenet_only,
            (True, False, "unknown"): PreferredProtocol.usenet_only,
            (False, True, "torrent"): PreferredProtocol.torrent_only,
            (False, True, "unknown"): PreferredProtocol.torrent_only,
        }[(usenet_enabled, torrent_enabled, preferred_protocol)]

    @property
    def usenet_enabled(self) -> bool:
        return self in (
            PreferredProtocol.usenet_only,
            PreferredProtocol.usenet_prefer,
            PreferredProtocol.torrent_prefer,
        )

    @property
    def torrent_enabled(self) -> bool:
        return self in (
            PreferredProtocol.torrent_only,
            PreferredProtocol.torrent_prefer,
            PreferredProtocol.usenet_prefer,
        )

    @property
    def preferred_protocol(self) -> str:
        return (
            "torrent"
            if self in (PreferredProtocol.torrent_prefer, PreferredProtocol.torrent_only)
            else "usenet"
        )


class DelayProfile(RadarrConfigBase):
    """
    The following parameters are available for configuring delay profiles.

    A preferred protocol must be specified for all delay profiles.
    Tags must be defined on all except the final profile (the default profile),
    where tags must not be defined.
    """

    preferred_protocol: PreferredProtocol
    """
    Choose which protocol(s) to use and which one is preferred
    when choosing between otherwise equal releases.

    Values:

    * `usenet-prefer` (Prefer Usenet)
    * `torrent-prefer` (Prefer Torrent)
    * `usenet-only` (Only Usenet)
    * `torrent-only` (Only Torrent)
    """

    usenet_delay: int = Field(0, ge=0)  # minutes
    """
    Delay (in minutes) to wait before grabbing Usenet releases.
    """

    torrent_delay: int = Field(0, ge=0)  # minutes
    """
    Delay (in minutes) to wait before grabbing torrent releases.
    """

    bypass_if_highest_quality: bool = False
    """
    Bypass the delay if a found release is the highest quality allowed
    in the quality profile that applies to it, and uses the preferred protocol
    as defined in this delay profile.
    """

    tags: Set[NonEmptyStr] = set()
    """
    Tags to assign to this delay profile.

    This delay profile will apply to movies with at least one matching tag.
    """

    @classmethod
    def _get_remote_map(
        cls,
        tag_ids: Mapping[str, int],
    ) -> List[RemoteMapEntry]:
        return [
            (
                "preferred_protocol",
                "enableUsenet",
                {
                    "root_decoder": lambda vs: PreferredProtocol.decode(
                        usenet_enabled=vs["enableUsenet"],
                        torrent_enabled=vs["enableTorrent"],
                        preferred_protocol=vs["preferredProtocol"],
                    ),
                    "encoder": lambda v: v.usenet_enabled,
                },
            ),
            (
                "preferred_protocol",
                "enableTorrent",
                {
                    "root_decoder": lambda vs: PreferredProtocol.decode(
                        usenet_enabled=vs["enableUsenet"],
                        torrent_enabled=vs["enableTorrent"],
                        preferred_protocol=vs["preferredProtocol"],
                    ),
                    "encoder": lambda v: v.torrent_enabled,
                },
            ),
            (
                "preferred_protocol",
                "preferredProtocol",
                {
                    "root_decoder": lambda vs: PreferredProtocol.decode(
                        usenet_enabled=vs["enableUsenet"],
                        torrent_enabled=vs["enableTorrent"],
                        preferred_protocol=vs["preferredProtocol"],
                    ),
                    "encoder": lambda v: v.preferred_protocol,
                },
            ),
            ("usenet_delay", "usenetDelay", {}),
            ("torrent_delay", "torrentDelay", {}),
            ("bypass_if_highest_quality", "bypassIfHighestQuality", {}),
            (
                "tags",
                "tags",
                {
                    "decoder": lambda v: set(
                        (tag for tag, tag_id in tag_ids.items() if tag_id in v),
                    ),
                    "encoder": lambda v: sorted(tag_ids[tag] for tag in v),
                },
            ),
        ]

    @classmethod
    def _from_remote(cls, tag_ids: Mapping[str, int], remote_attrs: Mapping[str, Any]) -> Self:
        return cls(
            **cls.get_local_attrs(cls._get_remote_map(tag_ids), remote_attrs),
        )

    def _create_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        tag_ids: Mapping[str, int],
        order: int,
    ) -> None:
        with radarr_api_client(secrets=secrets) as api_client:
            radarr.DelayProfileApi(api_client).create_delay_profile(
                delay_profile_resource=radarr.DelayProfileResource.from_dict(
                    {
                        "order": order,
                        **self.get_create_remote_attrs(tree, self._get_remote_map(tag_ids)),
                    },
                ),
            )

    def _update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: DelayProfile,
        tag_ids: Mapping[str, int],
        api_profile: radarr.DelayProfileResource,
        order: int,
    ) -> bool:
        updated, updated_attrs = self.get_update_remote_attrs(
            tree,
            remote,
            self._get_remote_map(tag_ids),
            check_unmanaged=True,
            set_unchanged=True,
        )
        if updated:
            with radarr_api_client(secrets=secrets) as api_client:
                radarr.DelayProfileApi(api_client).update_delay_profile(
                    id=str(api_profile.id),
                    delay_profile_resource=radarr.DelayProfileResource.from_dict(
                        {**api_profile.to_dict(), "order": order, **updated_attrs},
                    ),
                )
            return True
        return False

    def _delete_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        profile_id: int,
    ) -> None:
        logger.info("%s: (...) -> (deleted)", tree)
        with radarr_api_client(secrets=secrets) as api_client:
            radarr.DelayProfileApi(api_client).delete_delay_profile(profile_id)


class RadarrDelayProfilesSettings(RadarrConfigBase):
    """
    Delay profiles facilitate better release matching by delaying grabbing movies
    by a configured amount of time after release.

    This gives time for more releases to become available to your configured indexers,
    allowing Radarr to grab releases that better match your preferences.

    ```yaml
    radarr:
      settings:
        profiles:
          delay_profiles:
            # Set to `true` or `false` as desired. (Default `false`)
            # Works a bit differently to other profile types, see
            # the `delete_unmanaged` attribute docs.
            delete_unmanaged: true
            definitions:
              # Ordered in priority, highest priority first.
              - preferred_protocol: "torrent-prefer"
                usenet_delay: 1440
                torrent_delay: 1440
                bypass_if_highest_quality: true
                tags:
                  - "anime-movies"
              # Add additional delay profiles here as needed.
              ...
              # Default delay profile goes last, and MUST be defined
              # if you have defined any other delay profiles.
              - preferred_protocol: "usenet-prefer"
                usenet_delay: 0
                torrent_delay: 0
                bypass_if_highest_quality: false
                # Tags will be ignored for default delay profile.
    ```

    In Buildarr, delay profiles are defined using an ordered list structure,
    prioritised from first to last (top to bottom).

    The last delay profile in the list is assumed to be the default delay profile.
    Every non-default delay profile must have tags defined, and the
    default delay profile must have no tags defined.

    For more information, see this guide from
    [WikiArr](https://wiki.servarr.com/radarr/settings#delay-profiles).
    """

    delete_unmanaged = False
    """
    Controls how Buildarr manages existing delay profiles in Radarr when no delay profiles
    are defined in Buildarr.

    When set to `True` and there are no delay profiles defined in Buildarr,
    delete all delay profiles except the default delay profile (which can't be deleted).

    When set to `False` and there are no delay profiles defined in Buildarr,
    do not modify the existing delay profiles in Radarr at all.

    Due to the unique way delay profiles are structured, when they are defined in Buildarr,
    they always overwrite the existing delay profiles on the remote Radarr instance
    and configure it exactly as laid out in Buildarr, irrespective of this value.

    If unsure, leave this value set to `False`.
    """

    definitions: List[DelayProfile] = []
    """
    Define delay profiles to configure on Radarr here.

    The final delay profile in the list is assumed to be the default delay profile.
    """

    # TODO: Add a validator that checks that all profiles except the last one have tags.
    #       Ignore the tags on the default profile.

    @classmethod
    def from_remote(cls, secrets: RadarrSecrets) -> Self:
        with radarr_api_client(secrets=secrets) as api_client:
            api_profiles: List[radarr.DelayProfileResource] = sorted(
                radarr.DelayProfileApi(api_client).list_delay_profile(),
                key=lambda p: p.order,
                reverse=True,
            )
            tag_ids: Dict[str, int] = (
                {tag.label: tag.id for tag in radarr.TagApi(api_client).list_tag()}
                if any(api_profile.tags for api_profile in api_profiles)
                else {}
            )
        return cls(
            definitions=[
                DelayProfile._from_remote(tag_ids, api_profile.to_dict())
                for api_profile in api_profiles
            ],
        )

    def update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        if not self.delete_unmanaged and "definitions" not in self.__fields_set__:
            # TODO: Print current delay profile structure.
            if remote.definitions:
                logger.debug("%s.definitions: [...] (unmanaged)", tree)
            else:
                logger.debug("%s.definitions: [] (unmanaged)", tree)
            return False
        #
        changed = False
        #
        with radarr_api_client(secrets=secrets) as api_client:
            api_profiles: List[radarr.DelayProfileResource] = sorted(
                radarr.DelayProfileApi(api_client).list_delay_profile(),
                key=lambda p: p.order,
                reverse=True,
            )
            tag_ids: Dict[str, int] = (
                {tag.label: tag.id for tag in radarr.TagApi(api_client).list_tag()}
                if (
                    any(profile.tags for profile in self.definitions)
                    or any(profile.tags for profile in remote.definitions)
                )
                else {}
            )
        #
        num_local = len(self.definitions)
        num_remote = len(remote.definitions)
        max_num = max(num_local, num_remote)
        for max_index in range(max_num):
            local_index = num_local - max_num + max_index
            remote_index = num_remote - max_num + max_index
            # If the local index is negative, then there are more delay profiles
            # on the remote than there are defined in the local configuration.
            # Delete those extra delay profiles from the remote.
            if local_index < 0:
                remote.definitions[remote_index]._delete_remote(
                    tree=f"{tree}.definitions[{local_index}]",
                    secrets=secrets,
                    profile_id=api_profiles[remote_index].id,
                )
                changed = True
            # If the remote index is negative, then there are more delay profiles
            # defined locally than there are on the remote.
            # Create the missing delay profiles on the remote.
            elif remote_index < 0:
                self.definitions[local_index]._create_remote(
                    tree=f"{tree}.definitions[{local_index}]",
                    secrets=secrets,
                    tag_ids=tag_ids,
                    order=api_profiles[0].order + abs(remote_index),
                )
                changed = True
            # If none of the above conditions checked out, then the current index exists
            # in both the local configuration and the remote.
            # Check and update those delay profiles.
            elif self.definitions[local_index]._update_remote(
                tree=f"{tree}.definitions[{local_index}]",
                secrets=secrets,
                remote=remote.definitions[remote_index],
                tag_ids=tag_ids,
                api_profile=api_profiles[remote_index],
                order=api_profiles[remote_index].order,
            ):
                changed = True
        #
        return changed
