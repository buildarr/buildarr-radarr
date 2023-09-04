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
Indexer configuration base class.
"""


from __future__ import annotations

from logging import getLogger
from typing import Any, Dict, List, Mapping, Optional, Set

import radarr

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr
from pydantic import Field, validator
from typing_extensions import Self

from ....api import radarr_api_client
from ....secrets import RadarrSecrets
from ...types import RadarrConfigBase
from ...util import language_parse

logger = getLogger(__name__)


class Indexer(RadarrConfigBase):
    # Indexer configuration base class.

    enable_rss: bool = True
    """
    If enabled, use this indexer to watch for files that are wanted and missing
    or have not yet reached their cutoff.
    """

    enable_automatic_search: bool = True
    """
    If enabled, use this indexer for automatic searches, including Search on Add.
    """

    enable_interactive_search: bool = True
    """
    If enabled, use this indexer for manual interactive searches.
    """

    priority: int = Field(25, ge=1, le=50)
    """
    Priority of this indexer to prefer one indexer over another in release tiebreaker scenarios.

    1 is highest priority and 50 is lowest priority.
    """

    download_client: Optional[NonEmptyStr] = None
    """
    The name of the download client to use for grabs from this indexer.

    If unset, use any compatible download client.
    """

    multi_languages: Set[NonEmptyStr] = set()
    """
    The list of languages normally found on a multi-release grabbed from this indexer.

    The special value `original` can also be specified,
    to include the original language of the media.
    """

    tags: Set[NonEmptyStr] = set()
    """
    Only monitor releases that match at least one of the defined tags.

    If unset, monitor all releases using this indexer.
    """

    _implementation: str
    _remote_map: List[RemoteMapEntry] = []

    @validator("multi_languages")
    def validate_multi_languages(cls, value: Set[str]) -> Set[str]:
        return set(language_parse(language) for language in value)

    @classmethod
    def _get_base_remote_map(
        cls,
        api_schema: radarr.IndexerResource,
        downloadclient_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
    ) -> List[RemoteMapEntry]:
        return [
            ("enable_rss", "enableRss", {}),
            ("enable_automatic_search", "enableAutomaticSearch", {}),
            ("enable_interactive_search", "enableInteractiveSearch", {}),
            ("priority", "priority", {}),
            (
                "download_client",
                "downloadClientId",
                {
                    "decoder": lambda v: (
                        next(dc for dc, dc_id in downloadclient_ids.items() if dc_id == v)
                        if v
                        else None
                    ),
                    "encoder": lambda v: downloadclient_ids[v] if v else 0,
                },
            ),
            (
                "multi_languages",
                "multiLanguages",
                {
                    "decoder": lambda v: set(cls._language_decode(api_schema, la) for la in v),
                    "encoder": lambda v: sorted(cls._language_encode(api_schema, la) for la in v),
                    "is_field": True,
                },
            ),
            (
                "tags",
                "tags",
                {
                    "decoder": lambda v: [tag for tag, tag_id in tag_ids.items() if tag_id in v],
                    "encoder": lambda v: [tag_ids[tag] for tag in v],
                },
            ),
        ]

    @classmethod
    def _get_remote_map(
        cls,
        api_schema: radarr.IndexerResource,
        downloadclient_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
    ) -> List[RemoteMapEntry]:
        return []

    @classmethod
    def _language_decode(cls, api_schema: radarr.IndexerResource, value: str) -> str:
        field: radarr.Field = next(f for f in api_schema.fields if f.name == "multiLanguages")
        select_options: List[radarr.SelectOption] = field.select_options
        for option in select_options:
            option_name: str = option.name
            option_value: int = option.value
            if option_value == value:
                return option_name.lower()
        supported_languages = ", ".join(f"{o.name.lower()} ({o.value})" for o in select_options)
        raise ValueError(
            f"Invalid custom format quality language value {value} during decoding"
            f", supported quality languages are: {supported_languages}",
        )

    @classmethod
    def _language_encode(cls, api_schema: radarr.IndexerResource, value: str) -> int:
        field: radarr.Field = next(f for f in api_schema.fields if f.name == "multiLanguages")
        select_options: List[radarr.SelectOption] = field.select_options
        for option in select_options:
            option_name: str = option.name
            option_value: int = option.value
            if option_name.lower() == value:
                return option_value
        supported_languages = ", ".join(o.name.lower() for o in select_options)
        raise ValueError(
            f"Invalid or unsupported custom format language name '{value}'"
            f", supported languages are: {supported_languages}",
        )

    @classmethod
    def _from_remote(
        cls,
        api_schema: radarr.IndexerResource,
        downloadclient_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
        api_indexer: radarr.IndexerResource,
    ) -> Self:
        return cls(
            **cls.get_local_attrs(
                remote_map=(
                    cls._get_base_remote_map(
                        api_schema=api_schema,
                        downloadclient_ids=downloadclient_ids,
                        tag_ids=tag_ids,
                    )
                    + cls._get_remote_map(
                        api_schema=api_schema,
                        downloadclient_ids=downloadclient_ids,
                        tag_ids=tag_ids,
                    )
                    + cls._remote_map
                ),
                remote_attrs=api_indexer.to_dict(),
            ),
        )

    def _create_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        api_schema: radarr.IndexerResource,
        downloadclient_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
        indexer_name: str,
    ) -> None:
        set_attrs = self.get_create_remote_attrs(
            tree=tree,
            remote_map=(
                self._get_base_remote_map(
                    api_schema=api_schema,
                    downloadclient_ids=downloadclient_ids,
                    tag_ids=tag_ids,
                )
                + self._get_remote_map(
                    api_schema=api_schema,
                    downloadclient_ids=downloadclient_ids,
                    tag_ids=tag_ids,
                )
                + self._remote_map
            ),
        )
        field_values: Dict[str, Any] = {
            field["name"]: field["value"] for field in set_attrs["fields"]
        }
        set_attrs["fields"] = [
            ({**f, "value": field_values[f["name"]]} if f["name"] in field_values else f)
            for f in api_schema["fields"]
        ]
        remote_attrs = {"name": indexer_name, **api_schema, **set_attrs}
        with radarr_api_client(secrets=secrets) as api_client:
            radarr.IndexerApi(api_client).create_indexer(
                indexer_resource=radarr.IndexerResource.from_dict(remote_attrs),
            )

    def _update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        api_schema: radarr.IndexerResource,
        downloadclient_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
        api_indexer: radarr.IndexerResource,
    ) -> bool:
        updated, updated_attrs = self.get_update_remote_attrs(
            tree=tree,
            remote=remote,
            remote_map=(
                self._get_base_remote_map(
                    api_schema=api_schema,
                    downloadclient_ids=downloadclient_ids,
                    tag_ids=tag_ids,
                )
                + self._get_remote_map(
                    api_schema=api_schema,
                    downloadclient_ids=downloadclient_ids,
                    tag_ids=tag_ids,
                )
                + self._remote_map
            ),
        )
        if updated:
            if "fields" in updated_attrs:
                updated_fields: Dict[str, Any] = {
                    field["name"]: field["value"] for field in updated_attrs["fields"]
                }
                updated_attrs["fields"] = [
                    (
                        {**f, "value": updated_fields[f["name"]]}
                        if f["name"] in updated_fields
                        else f
                    )
                    for f in api_indexer.to_dict()["fields"]
                ]
            remote_attrs = {**api_indexer.to_dict(), **updated_attrs}
            with radarr_api_client(secrets=secrets) as api_client:
                radarr.IndexerApi(api_client).update_indexer(
                    id=str(api_indexer.id),
                    indexer_resource=radarr.IndexerResource.from_dict(remote_attrs),
                )
            return True
        return False

    def _delete_remote(self, secrets: RadarrSecrets, indexer_id: int) -> None:
        with radarr_api_client(secrets=secrets) as api_client:
            radarr.IndexerApi(api_client).delete_indexer(id=indexer_id)
