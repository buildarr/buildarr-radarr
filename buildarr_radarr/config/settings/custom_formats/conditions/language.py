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


from typing import List, Literal, cast
from buildarr.config import RemoteMapEntry

from buildarr.types import NonEmptyStr
import radarr

from .base import Condition


class LanguageCondition(Condition):
    """ """

    type: Literal["language"] = "language"
    """ """

    language: NonEmptyStr
    """Evaluate against available languages in Radarr API."""

    _implementation: Literal["LanguageSpecification"] = "LanguageSpecification"

    @classmethod
    def _get_remote_map(
        cls,
        api_schema: radarr.CustomFormatSpecificationSchema,
    ) -> List[RemoteMapEntry]:
        return [
            (
                "language",
                "value",
                {
                    "decoder": lambda v: cls._language_decode(api_schema, v),
                    "encoder": lambda v: cls._language_encode(api_schema, v),
                    "is_field": True,
                }
            )
        ]

    @classmethod
    def _language_parse(cls, value: str) -> str:
        # Results:
        #   1. English -> english
        #   2. english -> english
        #   3. ENGLISH -> english
        #   4. Portuguese (Brazil) -> portuguese-brazil
        #   5. portuguese_brazil -> portuguese-brazil
        #   6. PORTUGUESE-BRAZIL -> portuguese-brazil
        return "-".join(
            value.lower().replace("_", "-").replace("()", "").split(" ", maxsplit=2),
        )

    @classmethod
    def _language_decode(
        cls,
        api_schema: radarr.CustomFormatSpecificationSchema,
        value: int,
    ) -> str:
        field: radarr.Field = next((f for f in api_schema.fields if f.name == "value"))
        for option in field.select_options:
            option = cast(radarr.SelectOption, option)
            if option.value == value:
                return cls._language_parse(option.name)
        else:
            supported_languages = ", ".join(f"{o.name} ({o.value})" for o in field.select_options)
            raise ValueError(
                f"Invalid custom format language value {value} during decoding"
                f", supported languages are: {supported_languages}"
            )

    @classmethod
    def _language_encode(
        cls,
        api_schema: radarr.CustomFormatSpecificationSchema,
        value: str,
    ) -> str:
        field: radarr.Field = next((f for f in api_schema.fields if f.name == "value"))
        for option in field.select_options:
            option = cast(radarr.SelectOption, option)
            if cls._language_parse(option.name) == value:
                return option.value
        else:
            supported_languages = ", ".join(
                (f"{o.name} ({cls._language_parse(o.name)})" for o in field.select_options),
            )
            raise ValueError(
                f"Invalid or unsupported custom format language name '{value}'"
                f", supported languages are: {supported_languages}"
            )
