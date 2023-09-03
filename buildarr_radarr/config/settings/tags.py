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
Tags settings configuration.
"""


from __future__ import annotations

from logging import getLogger
from typing import Dict, Set

import radarr

from buildarr.types import NonEmptyStr
from typing_extensions import Self

from ...api import radarr_api_client
from ...secrets import RadarrSecrets
from ..types import RadarrConfigBase

logger = getLogger(__name__)


class RadarrTagsSettings(RadarrConfigBase):
    """
    Tags are used to associate media files with certain resources (e.g. indexers).

    ```yaml
    radarr:
      settings:
        tags:
          definitions:
            - movies
            - anime-movies
    ```

    To be able to use those tags in Buildarr, they need to be defined
    in this configuration section.
    """

    definitions: Set[NonEmptyStr] = set()
    """
    Define tags that are used within Buildarr here.

    If they are not defined here, you may get errors resulting from non-existent
    tags from either Buildarr or Radarr.
    """

    # TODO: Auto-tagging.

    @classmethod
    def from_remote(cls, secrets: RadarrSecrets) -> Self:
        with radarr_api_client(secrets=secrets) as api_client:
            tags = radarr.TagApi(api_client).list_tag()
        return cls(definitions=set([tag.label for tag in tags]))

    def update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        # This only does creations and updates, as Radarr automatically cleans up unused tags.
        changed = False
        with radarr_api_client(secrets=secrets) as api_client:
            tag_api = radarr.TagApi(api_client)
            current_tags: Dict[str, int] = {tag.label: tag.id for tag in tag_api.list_tag()}
            if self.definitions:
                for i, tag in enumerate(self.definitions):
                    if tag in current_tags:
                        logger.debug("%s.definitions[%i]: %s (exists)", tree, i, repr(tag))
                    else:
                        logger.info("%s.definitions[%i]: %s -> (created)", tree, i, repr(tag))
                        tag_api.create_tag(radarr.TagResource(label=tag))
                        changed = True
        return changed
