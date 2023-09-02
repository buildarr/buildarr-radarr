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
Custom format condition base class.
"""


from __future__ import annotations

from typing import Any, Dict, List, Tuple

import radarr

from buildarr.config import RemoteMapEntry
from typing_extensions import Self

from ....types import RadarrConfigBase


class Condition(RadarrConfigBase):
    # Custom format condition base class.
    #
    # Implements fields common to all condition types, and the Radarr API functions.

    negate: bool = False
    """
    When set to `true`, negates the condition on the custom format.

    If a condition with this field set to `true` matches, the custom format
    will **not** apply to the media.
    """

    required: bool = False
    """
    When set to `true`, this condition **must** match in order for the custom format to apply
    to media.

    If this field is `false` on all conditions in a custom format, it will apply
    if any one of the defined conditions match.
    """

    _implementation: str
    _base_remote_map: List[RemoteMapEntry] = [
        ("negate", "negate", {}),
        ("required", "required", {}),
    ]
    _remote_map: List[RemoteMapEntry] = []

    @classmethod
    def _get_remote_map(cls, api_schema_dict: Dict[str, Any]) -> List[RemoteMapEntry]:
        return []

    @classmethod
    def _from_remote(
        cls,
        api_schema_dict: Dict[str, Any],
        api_condition: radarr.CustomFormatSpecificationSchema,
    ) -> Self:
        return cls(
            **cls.get_local_attrs(
                remote_map=(
                    cls._base_remote_map + cls._get_remote_map(api_schema_dict) + cls._remote_map
                ),
                remote_attrs=api_condition.to_dict(),
            ),
        )

    def _create_remote(
        self,
        tree: str,
        api_schema_dict: Dict[str, Any],
        condition_name: str,
    ) -> Dict[str, Any]:
        set_attrs = self.get_create_remote_attrs(
            tree=tree,
            remote_map=(
                self._base_remote_map + self._get_remote_map(api_schema_dict) + self._remote_map
            ),
        )
        field_values: Dict[str, Any] = {
            field["name"]: field["value"] for field in set_attrs["fields"]
        }
        set_attrs["fields"] = [
            ({**f, "value": field_values[f["name"]]} if f["name"] in field_values else f)
            for f in api_schema_dict["fields"]
        ]
        return {"name": condition_name, **api_schema_dict, **set_attrs}

    def _update_remote(
        self,
        tree: str,
        api_schema_dict: Dict[str, Any],
        remote: Self,
        api_condition: radarr.CustomFormatSpecificationSchema,
    ) -> Tuple[bool, Dict[str, Any]]:
        updated, updated_attrs = self.get_update_remote_attrs(
            tree=tree,
            remote=remote,
            remote_map=(
                self._base_remote_map + self._get_remote_map(api_schema_dict) + self._remote_map
            ),
        )
        if updated:
            remote_attrs = api_condition.to_dict()
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
                    for f in remote_attrs["fields"]
                ]
            return (True, {**remote_attrs, **updated_attrs})
        return (False, api_condition.to_dict())
