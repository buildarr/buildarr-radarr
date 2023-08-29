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


from __future__ import annotations

from typing import List, Dict, Union

import radarr

from buildarr.config import RemoteMapEntry
from pydantic import Field
from typing_extensions import Annotated, Self

from ....api import radarr_api_client
from ....secrets import RadarrSecrets
from ...types import RadarrConfigBase
from .conditions.edition import EditionCondition
from .conditions.indexer_flag import IndexerFlagCondition
from .conditions.language import LanguageCondition
from .conditions.quality_modifier import QualityModifierCondition
from .conditions.release_group import ReleaseGroupCondition
from .conditions.release_title import ReleaseTitleCondition
from .conditions.resolution import ResolutionCondition
from .conditions.size import SizeCondition
from .conditions.source import SourceCondition


ConditionType = Union[
    EditionCondition,
    IndexerFlagCondition,
    LanguageCondition,
    QualityModifierCondition,
    ReleaseGroupCondition,
    ReleaseTitleCondition,
    ResolutionCondition,
    SizeCondition,
    SourceCondition,
]

CONDITION_TYPE_MAP = {
    condition_type._implementation: condition_type  # type: ignore[attr-defined]
    for condition_type in (
        EditionCondition,
        IndexerFlagCondition,
        LanguageCondition,
        QualityModifierCondition,
        ReleaseGroupCondition,
        ReleaseTitleCondition,
        ResolutionCondition,
        SizeCondition,
        SourceCondition,
    )
}


class CustomFormat(RadarrConfigBase):
    """ """

    include_when_renaming: bool = False
    """
    Make available in the `{Custom Formats}` template when renaming media titles.
    """

    conditions: Dict[str, Annotated[ConditionType, Field(discriminator="type")]] = {}
    """ """

    _remote_map: List[RemoteMapEntry] = [
        ("include_when_renaming", "includeCustomFormatWhenRenaming", {}),
    ]

    @classmethod
    def _from_remote(
        cls,
        secrets: RadarrSecrets,
        api_customformat: radarr.CustomFormatResource,
    ) -> CustomFormat:
        with radarr_api_client(secrets=secrets) as api_client:
            api_condition_schemas: Dict[str, radarr.CustomFormatSpecificationSchema] = {
                schema.implementation: schema
                for schema in radarr.CustomFormatApi(api_client).get_custom_format_schema()
            }
        return cls(
            **cls.get_local_attrs(
                remote_map=cls._remote_map,
                remote_attrs=api_customformat.to_dict(),
            ),
            conditions={
                api_condition.name: CONDITION_TYPE_MAP[  # type: ignore[attr-defined]
                    api_condition.implementation
                ]._from_remote(
                    api_schema=api_condition_schemas[api_condition.implementation],
                    api_condition=api_condition,
                )
                for api_condition in api_customformat.specifications
            }
        )


class CustomFormatsSettings(RadarrConfigBase):
    """ """

    delete_unmanaged: bool = False
    """
    Automatically delete custom formats not defined in Buildarr.
    """

    definitions: Dict[str, CustomFormat] = {}
    """
    Define download clients under this attribute.
    """

    @classmethod
    def from_remote(cls, secrets: RadarrSecrets) -> Self:
        with radarr_api_client(secrets=secrets) as api_client:
            return cls(
                definitions={
                    api_customformat.name: CustomFormat._from_remote(
                        secrets=secrets,
                        api_customformat=api_customformat,
                    )
                    for api_customformat in radarr.CustomFormatApi(api_client).list_custom_format()
                },
            )
