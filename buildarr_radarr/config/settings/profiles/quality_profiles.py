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
Quality profiles settings configuration.
"""


from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Sequence, Set, Union, cast

import radarr

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr
from pydantic import Field, validator
from typing_extensions import Annotated, Self

from ....api import radarr_api_client
from ....secrets import RadarrSecrets
from ...types import RadarrConfigBase
from ...util import language_parse

if TYPE_CHECKING:
    from ..custom_formats.custom_format import CustomFormat

logger = getLogger(__name__)


class QualityGroup(RadarrConfigBase):
    name: NonEmptyStr
    members: Set[NonEmptyStr] = Field(..., min_items=1)

    def encode(self, group_id: int, api_qualities: Mapping[str, radarr.Quality]) -> Dict[str, Any]:
        return {
            "id": group_id,
            "name": self.name,
            "allowed": True,
            "items": [_quality_str_encoder(api_qualities, member, True) for member in self.members],
        }


class CustomFormatScore(RadarrConfigBase):
    """
    Custom format score definitions in quality profiles can have the
    following attributes assigned to them.
    """

    name: NonEmptyStr
    """
    The name of the custom format to assign a score to. Required.
    """

    score: Optional[int] = None
    """
    The score to add to the release if the custom format is applied.

    If not defined, Buildarr will use the `default_score` attribute
    from the custom format definition.
    This allows for defining a common score for a custom format
    shared between multiple quality profiles.

    If `default_score` is not defined, the score will be set to `0` (ignore this custom format).
    """


class QualityProfile(RadarrConfigBase):
    # Quality profile definition configuration.
    #
    # For more information on how to configure this, refer to the plugin docs.

    upgrades_allowed: bool = False
    """
    Enable automatic upgrading if a higher quality version of the media file becomes available.

    If disabled, media files will not be upgraded after they have been downloaded.
    """

    qualities: Annotated[List[Union[NonEmptyStr, QualityGroup]], Field(min_items=1)]
    """
    The quality levels (or quality groups) to enable downloading releases for.
    The order determines the priority (highest priority first, lowest priority last).

    At least one quality level must be specified.
    """

    upgrade_until_quality: Optional[NonEmptyStr] = None
    """
    The maximum quality level (or quality group) to upgrade a movie to.

    Once this quality is reached, Radarr will no longer upgrade movie releases
    based on quality level.

    This attribute is required if `upgrades_allowed` is set to `true`.
    """

    minimum_custom_format_score: int = 0
    """
    The minimum sum of custom format scores matching a release
    for the release to be considered for download.

    If the score sum is below this number, it will not be downloaded.
    """

    upgrade_until_custom_format_score: int = 0
    """
    The maximum sum of custom format scores to upgrade a movie to.

    Once this number is reached, Radarr will no longer upgrade movie releases
    based on custom format score.

    This must be greater than or equal to `minimum_custom_format_score`.
    """

    custom_formats: List[CustomFormatScore] = []
    """
    Map scores for each custom format applicable to a quality profile here.
    """

    language: NonEmptyStr = "english"  # type: ignore[assignment]
    """
    The desired media language, written in English.

    Use the `any` keyword to allow any language.
    Use the `original` keyword to require the original language of the media.

    All languages supported by your Radarr instance version can be defined here.

    !!! note

        When prioritising by language using custom formats, this attribute should be set to `any`.

    Examples:

    * `english`
    * `portuguese-brazil`
    """

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

    @validator("upgrade_until_custom_format_score")
    def validate_upgrade_until_custom_format_score(cls, value: int, values: Dict[str, Any]) -> int:
        try:
            minimum_custom_format_score = values["minimum_custom_format_score"]
        except KeyError:
            return value
        if value < minimum_custom_format_score:
            raise ValueError(
                (
                    f"value ({value}) must be greater than "
                    f"'minimum_custom_format_score' ({minimum_custom_format_score})"
                ),
            )
        return value

    @validator("custom_formats")
    def validate_custom_format(cls, value: List[CustomFormatScore]) -> List[CustomFormatScore]:
        custom_format_names: Dict[str, Optional[int]] = {}
        custom_formats: List[CustomFormatScore] = []
        for cf in value:
            if cf.name in custom_format_names:
                first_score = custom_format_names[cf.name]
                # Just ignore the duplicate definition if the score is the same.
                if first_score == cf.score:
                    continue
                raise ValueError(
                    (
                        f"more than one score defined for custom format '{cf.name}'"
                        f" (scores: {first_score}, {cf.score})"
                    ),
                )
            custom_format_names[cf.name] = cf.score
            custom_formats.append(cf)
        return custom_formats

    @validator("language")
    def validate_language(cls, value: str) -> str:
        return language_parse(value)

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
                        upgrade_until_quality=vs.upgrade_until_quality,
                    ),
                },
            ),
            ("minimum_custom_format_score", "minFormatScore", {}),
            ("upgrade_until_custom_format_score", "cutoffFormatScore", {}),
            # TODO: Error handler for defined custom formats that don't exist.
            (
                "custom_formats",
                "formatItems",
                {
                    "decoder": lambda v: cls._custom_formats_decoder(v),
                    "encoder": lambda v: cls._custom_formats_encoder(api_customformats, v),
                },
            ),
            # TODO: Error handler for defined languages that don't exist.
            (
                "language",
                "language",
                {
                    "decoder": lambda v: v["name"],
                    "encoder": lambda v: {
                        "id": api_languages[v].id,
                        "name": api_languages[v].name,
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
        upgrade_until_quality: Optional[str],
    ) -> int:
        if not upgrade_until_quality:
            quality = qualities[0]
            return (
                group_ids[quality.name]
                if isinstance(quality, QualityGroup)
                else api_qualities[quality].id
            )
        return (
            group_ids[upgrade_until_quality]
            if upgrade_until_quality in group_ids
            else api_qualities[upgrade_until_quality].id
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
                    members=set([member["quality"]["name"] for member in quality["items"]]),
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
    def _custom_formats_decoder(
        cls,
        api_customformat_scores: List[Mapping[str, Any]],
    ) -> List[CustomFormatScore]:
        return sorted(
            (
                CustomFormatScore(name=api_cfs["name"], score=api_cfs["score"])
                for api_cfs in api_customformat_scores
                if api_cfs["score"] != 0
            ),
            key=lambda cfs: (-cast(int, cfs.score), cfs.name),
        )

    @classmethod
    def _custom_formats_encoder(
        cls,
        api_customformats: Mapping[str, radarr.CustomFormatResource],
        customformat_scores: List[CustomFormatScore],
    ) -> List[Dict[str, Any]]:
        customformat_names: Set[str] = set()
        custom_formats: List[Dict[str, Any]] = []
        for cfs in customformat_scores:
            custom_formats.append(
                {"format": api_customformats[cfs.name].id, "name": cfs.name, "score": cfs.score},
            )
            customformat_names.add(cfs.name)
        for customformat_name, api_customformat in api_customformats.items():
            if customformat_name not in customformat_names:
                custom_formats.append(
                    {"format": api_customformat.id, "name": customformat_name, "score": 0},
                )
                customformat_names.add(customformat_name)
        return custom_formats

    def _render(self, custom_formats: Dict[str, CustomFormat]) -> None:
        custom_format_scores: List[CustomFormatScore] = []
        for cfs in self.custom_formats:
            custom_format = custom_formats[cfs.name]
            if cfs.score is not None:
                score = cfs.score
            else:
                score = (
                    custom_format.default_score if custom_format.default_score is not None else 0
                )
            if score != 0:
                custom_format_scores.append(
                    CustomFormatScore(name=cfs.name, score=score),
                )
        self.custom_formats = sorted(
            custom_format_scores,
            key=lambda cfs: (-cast(int, cfs.score), cfs.name),
        )

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
    Quality profiles are used by Radarr as the guideline for
    desired quality when searching for releases.

    When media is requested for download in Radarr, the user selects a quality profile
    to use. Once all available releases have been found, the release that most closely
    matches the quality profile will be selected for download.

    With a quality profile you can prioritise media releases by
    the desired quality level, arbitrary conditions using custom formats,
    or language. Parameters for upgrading existing media to higher quality versions
    are also defined here.

    ```yaml
    radarr:
      settings:
        profiles:
          quality_profiles:
            delete_unmanaged: false
            definitions:
              # Add Quality profiles here.
              # The name of the block becomes the name of the quality profile.
              HD/SD:
                upgrades_allowed: true
                upgrade_until_quality: Bluray-1080p
                qualities:
                  - Bluray-1080p  # Quality definition name.
                  - name: WEB 1080p  # Group quality definitions of equal priority.
                    members:
                      - WEBRip-1080p
                    -   WEBDL-1080p
                  - Bluray-720p
                  - name: WEB 720p
                    members:
                      - WEBRip-720p
                      - WEBDL-720p
                  - Bluray-576p
                  - Bluray-480p
                  - name: WEB 480p
                    members:
                      - WEBRip-480p
                      - WEBDL-480p
                  - name: DVD-Video
                    members:
                      - DVD-R
                      - DVD
                minimum_custom_format_score: 0
                upgrade_until_custom_format_score: 10000
                custom_formats:
                  - name: remaster  # Use the `default_score` field in the custom format definition.
                  - name: 4k-remaster
                    score: 100  # Explicitly set score for the custom format in the profile.
                language: english
    ```

    In Buildarr, quality profiles are defined using a dictonary structure,
    where the name of the definition becomes the name of the quality profile in Radarr.
    """

    delete_unmanaged: bool = False
    """
    Automatically delete quality profiles not defined in Buildarr.

    Out of the box Radarr provides some pre-defined quality profiles.
    **If there are no quality profiles defined in Buildarr and
    `delete_unmanaged` is `true`, Buildarr will delete all existing profiles.
    Be careful when using `delete_unmanaged`.**
    """

    definitions: Dict[str, QualityProfile] = {}
    """
    Define quality profiles to configure on Radarr here.
    """

    def _render(self, custom_formats: Dict[str, CustomFormat]) -> None:
        for profile in self.definitions.values():
            profile._render(custom_formats=custom_formats)

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
                language_parse(api_language.name): api_language
                for api_language in radarr.LanguageApi(api_client).list_language()
            }
        for profile_name, profile in self.definitions.items():
            profile_tree = f"{tree}.definitions[{profile_name!r}]"
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
                profile_tree = f"{tree}.definitions[{profile_name!r}]"
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
