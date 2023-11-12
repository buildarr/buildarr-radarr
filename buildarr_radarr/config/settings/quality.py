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
Quality settings configuration.
"""


from __future__ import annotations

import json

from typing import Any, Dict, Mapping, Optional, cast

import radarr

from buildarr.config import ConfigTrashIDNotFoundError
from buildarr.state import state
from buildarr.types import TrashID
from pydantic import Field, validator
from typing_extensions import Self

from ...api import radarr_api_client
from ...secrets import RadarrSecrets
from ..types import RadarrConfigBase

QUALITYDEFINITION_MIN_MAX = 398
QUALITYDEFINITION_PREFERRED_MAX = 399
QUALITYDEFINITION_MAX = 400


class QualityDefinition(RadarrConfigBase):
    """
    If you would like to fine tune the parameters yourself, Buildarr
    supports configuring all quality definitions attributes manually.

    You can also combine this with a TRaSH-Guides profile using `trash_id`,
    to override specific quality definitions when values different from the profile
    are required.

    ```yaml
    radarr:
      settings:
        quality:
          # trash_id: ...  # When set, the below definitions override the values in this profile.
          definitions:
            Bluray-480p:
              min: 2
              preferred: null  # Max preferred
              max: null  # Unlimited
            DVD:
              title: DVD-480p
              min: 2
              preferred: 95
              max: 100
    ```
    """

    title: Optional[str] = None
    """
    The name of the quality in the GUI.

    If set to an empty string or `null`, it will always be set to the
    name of the quality itself. (e.g. For the `Bluray-480p` quality, the GUI title
    will also be `Bluray-480p`)
    """

    min: float = Field(..., ge=0, le=QUALITYDEFINITION_MIN_MAX)
    """
    The minimum allowed bitrate for a quality level, in megabytes per minute (MB/min).

    Must be set at least 1MB/min lower than `preferred`.
    The minimum value is `0`, and the maximum value is `398`.
    """

    preferred: Optional[float] = Field(..., ge=0, le=QUALITYDEFINITION_PREFERRED_MAX)
    """
    The maximum allowed bitrate for a quality level, in megabytes per minute (MB/min).

    Must be set at least 1MB/min higher than `min`, and 1MB/min lower than `max`.
    If set to `null` or `399`, prefer the highest possible bitrate.
    """

    max: Optional[float] = Field(..., ge=1, le=QUALITYDEFINITION_MAX)
    """
    The maximum allowed bitrate for a quality level, in megabytes per minute (MB/min).

    Must be set at least 1MB/min higher than `preferred`.
    If set to `null` or `400`, the maximum bit rate will be unlimited.
    """

    @validator("preferred")
    def validate_preferred(
        cls,
        value: Optional[float],
        values: Mapping[str, Any],
    ) -> Optional[float]:
        if value is None or value >= QUALITYDEFINITION_PREFERRED_MAX:
            return None
        try:
            quality_min: float = values["min"]
            if (value - quality_min) < 1:
                raise ValueError(
                    f"'preferred' ({value}) is not at least 1 greater than 'min' ({quality_min})",
                )
        except KeyError:
            # `min` only doesn't exist when it failed type validation.
            # If it doesn't exist, skip validation that uses it.
            pass
        return value

    @validator("max")
    def validate_max(
        cls,
        value: Optional[float],
        values: Mapping[str, Any],
    ) -> Optional[float]:
        if value is None or value >= QUALITYDEFINITION_MAX:
            return None
        try:
            try:
                quality_preferred = float(values["preferred"])
            except TypeError:
                quality_preferred = QUALITYDEFINITION_PREFERRED_MAX
            if (value - quality_preferred) < 1:
                raise ValueError(
                    f"'max' ({value}) is not "
                    f"at least 1 greater than 'preferred' ({quality_preferred})",
                )
        except KeyError:
            # `preferred` only doesn't exist when it failed type validation.
            # If it doesn't exist, skip validation that uses it.
            pass
        return value


class RadarrQualitySettings(RadarrConfigBase):
    # Quality definition settings configuration.
    #
    # For more information on how to configure this, refer to the plugin docs.

    trash_id: Optional[TrashID] = None
    """
    Trash ID of the TRaSH-Guides quality definition profile to load default values from.

    If there is an update in the profile, the quality definitions will be updated accordingly.
    """

    definitions: Dict[str, QualityDefinition] = {}
    """
    Explicitly set quality definitions here.

    The key of the definition is the "Quality" column of the Quality Definitions page
    in Radarr, **not** "Title".

    If `trash_id` is set, any values set here will override the default values provided
    from the TRaSH-Guides quality definition profile.

    If `trash_id` is not set, only explicitly defined quality definitions are managed,
    and quality definitions not set within Buildarr are left unmodified.
    """

    def uses_trash_metadata(self) -> bool:
        return bool(self.trash_id)

    def _render(self) -> None:
        if not self.trash_id:
            return
        for quality_file in (
            state.trash_metadata_dir / "docs" / "json" / "radarr" / "quality-size"
        ).iterdir():
            with quality_file.open() as f:
                quality_json = json.load(f)
                if cast(str, quality_json["trash_id"]).lower() == self.trash_id:
                    for definition_json in quality_json["qualities"]:
                        definition_name = definition_json["quality"]
                        if definition_name not in self.definitions:
                            self.definitions[definition_name] = QualityDefinition(
                                title=None,
                                min=definition_json["min"],
                                preferred=definition_json["preferred"],
                                max=definition_json["max"],
                            )
                    return
        raise ConfigTrashIDNotFoundError(
            f"Unable to find Radarr quality definition file with trash ID '{self.trash_id}'",
        )

    @classmethod
    def from_remote(cls, secrets: RadarrSecrets) -> Self:
        with radarr_api_client(secrets=secrets) as api_client:
            return cls(
                definitions={
                    api_qualitydefinition.quality.name: QualityDefinition(
                        title=(
                            api_qualitydefinition.title
                            if api_qualitydefinition.title != api_qualitydefinition.quality.name
                            else None
                        ),
                        min=api_qualitydefinition.min_size,
                        preferred=api_qualitydefinition.preferred_size,
                        max=api_qualitydefinition.max_size or None,
                    )
                    for api_qualitydefinition in radarr.QualityDefinitionApi(
                        api_client,
                    ).list_quality_definition()
                },
            )

    def update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        changed = False
        with radarr_api_client(secrets=secrets) as api_client:
            qualitydefinition_api = radarr.QualityDefinitionApi(api_client)
            api_qualitydefinitions = {
                api_qualitydefinition.quality.name: api_qualitydefinition
                for api_qualitydefinition in qualitydefinition_api.list_quality_definition()
            }
            for definition_name, local_definition in self.definitions.items():
                updated, remote_attrs = local_definition.get_update_remote_attrs(
                    tree=f"{tree}[{definition_name!r}]",
                    remote=remote.definitions[definition_name],
                    remote_map=[
                        ("title", "title", {"encoder": lambda v: v or definition_name}),
                        ("min", "minSize", {}),
                        ("max", "maxSize", {}),
                    ],
                    check_unmanaged=False,
                    set_unchanged=False,
                )
                if updated:
                    api_qualitydefinition = api_qualitydefinitions[definition_name]
                    qualitydefinition_api.update_quality_definition(
                        id=str(api_qualitydefinition.id),
                        quality_definition_resource=radarr.QualityDefinitionResource.from_dict(
                            {**api_qualitydefinition.to_dict(), **remote_attrs},
                        ),
                    )
                    changed = True
        return changed
