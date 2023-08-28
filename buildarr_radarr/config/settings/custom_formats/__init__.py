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


from typing import Dict, Union

from pydantic import Field
from typing_extensions import Annotated

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


class CustomFormat(RadarrConfigBase):
    """ """

    include_when_renaming: bool = False
    """
    Make available in the `{Custom Formats}` template when renaming media titles.
    """

    conditions: Dict[str, Annotated[ConditionType, Field(discriminator="type")]] = {}
    """ """
