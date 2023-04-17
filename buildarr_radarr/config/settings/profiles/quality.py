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
Radarr plugin quality profile configuration.
"""


from __future__ import annotations

from logging import getLogger
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Union

import radarr

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr
from pydantic import Field, validator
from typing_extensions import Annotated, Self

from ....api import radarr_api_client
from ....secrets import RadarrSecrets
from ...types import RadarrConfigBase

logger = getLogger(__name__)


class QualityGroup(RadarrConfigBase):
    """
    Quality group.

    Allows groups of quality definitions to be given the same prorioty in qualtity profiles.
    """

    name: NonEmptyStr
    members: Set[NonEmptyStr] = Field(..., min_items=1)

    def encode(self, group_id: int, api_qualities: Mapping[str, radarr.Quality]) -> Dict[str, Any]:
        return {
            "id": group_id,
            "name": self.name,
            "allowed": True,
            "items": [
                _quality_str_encoder(api_qualities, member, True) for member in self.members
            ],
        }


class QualityProfile(RadarrConfigBase):
    """
    The main things to consider when creating a quality profile are
    what quality settings to enable, and how to prioritise each.

    ```yaml
    ...
      quality_profiles:
        SDTV:
          upgrades_allowed: true
          upgrade_until_quality: "Bluray-1080p"
          qualities:
          - "Bluray-480p"
          - "DVD"
          - name: "WEB 480p"
            members:
              - "WEBDL-480p"
              - "WEBRip-480p"
          - "SDTV"
          custom_formats:
            "Name of Custom Format": 0
          language: "English"
    ```

    In Buildarr, the quality listed first (at the top) is given the highest priority, with
    subsequent qualities given lower priority. Qualities not explicitly defined are
    disabled (not downloaded).

    Radarr supports grouping multiple qualities together to give them the same priority.
    In Buildarr, these are expressed by giving a `name` to the group, and listing the qualities
    under the `members` attribute.

    For more insight into reasonable values for quality profiles,
    refer to these guides from [WikiArr](https://wiki.servarr.com/radarr/settings#quality-profiles)
    and TRaSH-Guides ([general](https://trash-guides.info/Radarr/radarr-setup-quality-profiles),
    [anime](https://trash-guides.info/Radarr/radarr-setup-quality-profiles-anime)).
    """

    upgrades_allowed: bool = False
    """
    Enable automatic upgrading if a higher quality version of the media file becomes available.

    If disabled, media files will not be upgraded after they have been downloaded.
    """

    qualities: Annotated[List[Union[NonEmptyStr, QualityGroup]], Field(min_items=1)]
    """
    The qualities to enable downloading episodes for. The order determines the priority
    (highest priority first, lowest priority last).

    Individual qualities can be specified using the name (e.g. `Bluray-480p`).

    Qualities can also be grouped together in a structure to give them the same
    priority level. A new version of the episode will not be downloaded if it is
    at least one of the qualities listed in the group, until a higher quality
    version is found.

    ```yaml
    ...
      qualities:
        - name: "WEB 480p"
          members:
            - "WEBDL-480p"
            - "WEBRip-480p"
    ```

    At least one quality must be specified.
    """

    upgrade_until_quality: Optional[NonEmptyStr] = None
    """
    The maximum quality level to upgrade an episode to.
    For a quality group, specify the group name.

    Once this quality is reached Radarr will no longer download episodes.

    This attribute is required if `upgrades_allowed` is set to `True`.
    """

    minimum_custom_format_score: int = 0
    """ """

    custom_formats: Dict[str, int] = {}
    """
    If not defined here, add it with a score of 0 to the request.
    """

    language: NonEmptyStr = "English"  # type: ignore[assignment]
    """ """

    @validator("qualities")
    def validate_qualities(
        cls,
        value: List[Union[str, QualityGroup]],
    ) -> List[Union[str, QualityGroup]]:
        quality_name_map: Dict[str, Union[str, QualityGroup]] = {}
        for quality in value:
            for name in quality.members if isinstance(quality, QualityGroup) else [quality]:
                if name in quality_name_map:
                    error_message = f"duplicate entries of quality value '{name}' exist ("
                    other = quality_name_map[name]
                    if isinstance(quality, str) and isinstance(quality, str):
                        error_message += "both are non-grouped quality values"
                    else:
                        error_message += (
                            f"one as part of quality group '{quality.name}', "
                            if isinstance(quality, QualityGroup)
                            else "one as a non-grouped quality value, "
                        )
                        error_message += (
                            f"another as part of quality group '{other.name}'"
                            if isinstance(other, QualityGroup)
                            else "another as a non-grouped quality value"
                        )
                    error_message += ")"
                    raise ValueError(error_message)
                quality_name_map[name] = quality
        return value

    @validator("upgrade_until_quality")
    def validate_upgrade_until_quality(
        cls,
        value: Optional[str],
        values: Dict[str, Any],
    ) -> Optional[str]:
        try:
            upgrades_allowed: bool = values["upgrades_allowed"]
            qualities: Sequence[Union[str, QualityGroup]] = values["qualities"]
        except KeyError:
            return value
        # If `upgrades_allowed` is `False`, set `upgrade_until_quality` to `None`
        # to make sure Buildarr ignores whatever it is currently set to
        # on the remote instance.
        if not upgrades_allowed:
            return None
        # Subsequent checks now assume that `upgrades_allowed` is `True`,
        # this parameter is required and defined to a valid value.
        if not value:
            raise ValueError("required if 'upgrades_allowed' is True")
        for quality in qualities:
            quality_name = quality.name if isinstance(quality, QualityGroup) else quality
            if value == quality_name:
                break
        else:
            raise ValueError("must be set to a value enabled in 'qualities'")
        return value

    @classmethod
    def _get_remote_map(
        cls,
        api_qualities: Mapping[str, radarr.Quality] = {},
        api_customformats: Mapping[str, radarr.CustomFormatResource] = {},
        api_languages: Mapping[str, radarr.LanguageResource] = {},
        group_ids: Mapping[str, int] = {},
    ) -> List[RemoteMapEntry]:
        return [
            ("upgrades_allowed", "upgradeAllowed", {}),
            (
                "qualities",
                "items",
                {
                    "decoder": lambda v: cls._qualities_decoder(v),
                    "encoder": lambda v: cls._qualities_encoder(api_qualities, group_ids, v),
                },
            ),
            (
                "upgrade_until_quality",
                "cutoff",
                {
                    "root_decoder": lambda vs: cls._upgrade_until_quality_decoder(
                        items=vs["items"],
                        cutoff=vs["cutoff"],
                    ),
                    "root_encoder": lambda vs: cls._upgrade_until_quality_encoder(
                        api_qualities=api_qualities,
                        group_ids=group_ids,
                        qualities=vs.qualities,
                        upgrade_until=vs.upgrade_until,
                    ),
                },
            ),
            ("minimum_custom_format_score", "cutoffFormatScore", {}),
            # TODO: Error handler for defined custom formats that don't exist.
            (
                "custom_formats",
                "formatItems",
                {
                    "decoder": lambda v: {f["name"]: f["score"] for f in v},
                    "encoder": lambda v: sorted(
                        [
                            {"format": api_customformat.id, "name": name, "score": v.get(name, 0)}
                            for name, api_customformat in api_customformats.items()
                        ],
                        key=lambda f: (-f["score"], f["name"]),
                    ),
                },
            ),
            # TODO: Error handler for defined languages that don't exist.
            (
                "language",
                "language",
                {
                    "decoder": lambda v: v["name"],
                    "equals": lambda a, b: a.lower() == b.lower(),
                    "encoder": lambda v: {
                        "id": api_languages[v.lower()].id,
                        "name": api_languages[v.lower()].name,
                    },
                },
            ),
        ]

    @classmethod
    def _upgrade_until_quality_decoder(
        cls,
        items: Sequence[Mapping[str, Any]],
        cutoff: int,
    ) -> str:
        for quality_item in items:
            quality: Mapping[str, Any] = (
                quality_item  # Quality group
                if "id" in quality_item
                else quality_item["quality"]  # Singular quality
            )
            if quality["id"] == cutoff:
                return quality["name"]
        raise RuntimeError(
            "Inconsistent Radarr instance state: "
            f"'cutoff' quality ID {cutoff} not found in 'items': {items}",
        )

    @classmethod
    def _upgrade_until_quality_encoder(
        cls,
        api_qualities: Mapping[str, radarr.Quality],
        group_ids: Mapping[str, int],
        qualities: Sequence[Union[str, QualityGroup]],
        upgrade_until: Optional[str],
    ) -> int:
        if not upgrade_until:
            quality = qualities[0]
            return (
                group_ids[quality.name]
                if isinstance(quality, QualityGroup)
                else api_qualities[quality].id
            )
        return (
            group_ids[upgrade_until]
            if upgrade_until in group_ids
            else api_qualities[upgrade_until].id
        )

    @classmethod
    def _qualities_decoder(
        cls,
        value: Sequence[Mapping[str, Any]],
    ) -> List[Union[str, QualityGroup]]:
        return [
            (
                QualityGroup(
                    name=quality["name"],
                    members=[member["quality"]["name"] for member in quality["items"]],
                )
                if quality["items"]
                else quality["quality"]["name"]
            )
            for quality in reversed(value)
            if quality["allowed"]
        ]

    @classmethod
    def _qualities_encoder(
        cls,
        api_qualities: Mapping[str, radarr.Quality],
        group_ids: Mapping[str, int],
        qualities: List[Union[str, QualityGroup]],
    ) -> List[Dict[str, Any]]:
        qualities_json: List[Dict[str, Any]] = []
        enabled_qualities: Set[str] = set()

        for quality in qualities:
            if isinstance(quality, QualityGroup):
                qualities_json.append(quality.encode(group_ids[quality.name], api_qualities))
                for member in quality.members:
                    enabled_qualities.add(member)
            else:
                qualities_json.append(_quality_str_encoder(api_qualities, quality, True))
                enabled_qualities.add(quality)

        for quality_name in api_qualities.keys():
            if quality_name not in enabled_qualities:
                qualities_json.append(_quality_str_encoder(api_qualities, quality_name, False))

        return list(reversed(qualities_json))

    @classmethod
    def _from_remote(cls, remote_attrs: Mapping[str, Any]) -> Self:
        return cls(**cls.get_local_attrs(cls._get_remote_map(), remote_attrs))

    def _create_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        api_qualities: Mapping[str, radarr.Quality],
        api_customformats: Mapping[str, radarr.CustomFormatResource],
        api_languages: Mapping[str, radarr.LanguageResource],
        profile_name: str,
    ) -> None:
        group_ids: Dict[str, int] = {
            quality_group.name: (1000 + i)
            for i, quality_group in enumerate(
                [q for q in self.qualities if isinstance(q, QualityGroup)],
                1,
            )
        }
        with radarr_api_client(secrets=secrets) as api_client:
            radarr.QualityProfileApi(api_client).create_quality_profile(
                quality_profile_resource=radarr.QualityProfileResource.from_dict(
                    {
                        "name": profile_name,
                        **self.get_create_remote_attrs(
                            tree,
                            self._get_remote_map(
                                api_qualities=api_qualities,
                                api_customformats=api_customformats,
                                api_languages=api_languages,
                                group_ids=group_ids,
                            ),
                        ),
                    },
                ),
            )

    def _update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        api_qualities: Mapping[str, radarr.Quality],
        api_customformats: Mapping[str, radarr.CustomFormatResource],
        api_languages: Mapping[str, radarr.LanguageResource],
        api_profile: radarr.QualityProfileResource,
    ) -> bool:
        group_ids: Dict[str, int] = {
            quality_group.name: (1000 + i)
            for i, quality_group in enumerate(
                [q for q in self.qualities if isinstance(q, QualityGroup)],
                1,
            )
        }
        updated, updated_attrs = self.get_update_remote_attrs(
            tree,
            remote,
            self._get_remote_map(
                api_qualities=api_qualities,
                api_customformats=api_customformats,
                api_languages=api_languages,
                group_ids=group_ids,
            ),
            check_unmanaged=True,
            set_unchanged=True,
        )
        if updated:
            with radarr_api_client(secrets=secrets) as api_client:
                radarr.QualityProfileApi(api_client).update_quality_profile(
                    id=str(api_profile.id),
                    quality_profile_resource=radarr.QualityProfileResource.from_dict(
                        {**api_profile.to_dict(), **updated_attrs},
                    ),
                )
            return True
        return False

    def _delete_remote(self, secrets: RadarrSecrets, profile_id: int) -> None:
        with radarr_api_client(secrets=secrets) as api_client:
            radarr.QualityProfileApi(api_client).delete_quality_profile(id=profile_id)


class RadarrQualityProfilesSettings(RadarrConfigBase):
    """
    Configuration parameters for controlling how Buildarr handles quality profiles.
    """

    delete_unmanaged: bool = False
    """
    Automatically delete quality profiles not defined in Buildarr.

    Out of the box Radarr provides some pre-defined quality profiles.
    Take care when enabling this option, as those will also be deleted.
    """

    definitions: Dict[str, QualityProfile] = {}
    """
    Define quality profiles to configure on Radarr here.

    If there are no quality profiles defined and `delete_unmanaged` is `False`,
    Buildarr will not modify existing quality profiles, but if `delete_unmanaged` is `True`,
    **Buildarr will delete all existing profiles. Be careful when using `delete_unmanaged`.**
    """

    @classmethod
    def from_remote(cls, secrets: RadarrSecrets) -> Self:
        with radarr_api_client(secrets=secrets) as api_client:
            return cls(
                definitions={
                    api_profile.name: QualityProfile._from_remote(api_profile.to_dict())
                    for api_profile in radarr.QualityProfileApi(api_client).list_quality_profile()
                },
            )

    def update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        updated = False
        with radarr_api_client(secrets=secrets) as api_client:
            api_profiles: Dict[str, radarr.QualityProfileResource] = {
                api_profile.name: api_profile
                for api_profile in radarr.QualityProfileApi(api_client).list_quality_profile()
            }
            api_qualities: Dict[str, radarr.Quality] = {
                api_qualitydefinition.title: api_qualitydefinition.quality
                for api_qualitydefinition in sorted(
                    radarr.QualityDefinitionApi(api_client).list_quality_definition(),
                    key=lambda q: q["weight"],
                    reverse=True,
                )
            }
            api_customformats: Dict[str, radarr.CustomFormatResource] = {
                api_customformat.name: api_customformat
                for api_customformat in radarr.CustomFormatApi(api_client).list_custom_format()
            }
            api_languages: Dict[str, radarr.LanguageResource] = {
                api_language.name_lower: api_language
                for api_language in radarr.LanguageApi(api_client).list_language()
            }
        for profile_name, profile in self.definitions.items():
            profile_tree = f"{tree}.definitions[{repr(profile_name)}]"
            if profile_name not in remote.definitions:
                profile._create_remote(
                    tree=profile_tree,
                    secrets=secrets,
                    api_qualities=api_qualities,
                    api_customformats=api_customformats,
                    api_languages=api_languages,
                    profile_name=profile_name,
                )
                updated = True
            elif profile._update_remote(
                tree=profile_tree,
                secrets=secrets,
                remote=remote.definitions[profile_name],
                api_qualities=api_qualities,
                api_customformats=api_customformats,
                api_languages=api_languages,
                api_profile=api_profiles[profile_name],
            ):
                updated = True
        return updated

    def delete_remote(self, tree: str, secrets: RadarrSecrets, remote: Self) -> bool:
        updated = False
        with radarr_api_client(secrets=secrets) as api_client:
            profile_ids: Dict[str, int] = {
                api_profile.name: api_profile.id
                for api_profile in radarr.QualityProfileApi(api_client).list_quality_profile()
            }
        for profile_name, profile in remote.definitions.items():
            if profile_name not in self.definitions:
                profile_tree = f"{tree}.definitions[{repr(profile_name)}]"
                if self.delete_unmanaged:
                    logger.info("%s: (...) -> (deleted)", profile_tree)
                    profile._delete_remote(
                        secrets=secrets,
                        profile_id=profile_ids[profile_name],
                    )
                    updated = True
                else:
                    logger.debug("%s: (...) (unmanaged)", profile_tree)
        return updated


def _quality_str_encoder(
    api_qualities: Mapping[str, radarr.Quality],
    quality_name: str,
    allowed: bool,
) -> Dict[str, Any]:
    return {"quality": api_qualities[quality_name], "items": [], "allowed": allowed}
