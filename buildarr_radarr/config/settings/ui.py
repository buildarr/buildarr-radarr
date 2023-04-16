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
Radarr plugin UI settings configuration.
"""


from __future__ import annotations

from typing import Dict, List, Mapping

import radarr

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum
from pydantic import validator
from typing_extensions import Self

from ...api import radarr_api_client
from ...secrets import RadarrSecrets
from ...types import LowerCaseStr
from ..types import RadarrConfigBase


class FirstDayOfWeek(BaseEnum):
    sunday = 0
    monday = 1


class WeekColumnHeader(BaseEnum):
    month_first = "ddd M/D"
    month_first_padded = "ddd MM/DD"
    day_first = "ddd D/M"
    day_first_padded = "ddd DD/MM"


class RuntimeFormat(BaseEnum):
    hours_minutes = "hoursMinutes"
    minutes = "minutes"


class ShortDateFormat(BaseEnum):
    """
    Short date format enumeration for Radarr.
    """

    word_month_first = "MMM D YYYY"
    word_month_second = "DD MMM YYYY"
    slash_month_first = "MM/D/YYYY"
    slash_month_first_day_padded = "MM/DD/YYYY"
    slash_day_first = "DD/MM/YYYY"
    iso8601 = "YYYY-MM-DD"


class LongDateFormat(BaseEnum):
    """
    Long date format enumeration for Radarr.
    """

    month_first = "dddd, MMMM D YYYY"
    day_first = "dddd, D MMMM YYYY"


class TimeFormat(BaseEnum):
    """
    Time format enumeration for Radarr.
    """

    twelve_hour = "h(:mm)a"
    twentyfour_hour = "HH:mm"


class Theme(BaseEnum):
    """
    Theme enumeration for Radarr.
    """

    auto = "auto"
    light = "light"
    dark = "dark"


class RadarrUISettings(RadarrConfigBase):
    """
    Radarr user interface configuration can also be set directly from Buildarr.

    ```yaml
    radarr:
      settings:
        ui:
          first_day_of_week: "monday"
          week_column_header: "day-first"
          short_date_format: "word-month-second"
          long_date_format: "day-first"
          time_format: "twentyfour-hour"
          show_relative_dates: true
          enable_color_impaired_mode: false
          theme: "light"
          ui_language: "en"
    ```
    """

    # Calendar
    first_day_of_week: FirstDayOfWeek = FirstDayOfWeek.sunday
    """
    The first day of the week that Radarr will show in the calendar.

    Values:

    * `sunday` - Sunday
    * `monday` - Monday
    """

    week_column_header: WeekColumnHeader = WeekColumnHeader.month_first
    """
    The format of the date in columns when "Week" is the active view in the calendar.

    Values:

    * `month-first` - Print month first (e.g. Tue 3/25)
    * `month-first-padded` - Print month first with padded numbers (e.g. Tue 03/25)
    * `day-first` - Print day first with padded numbers (e.g. Tue 25/3)
    * `day-first-padded` - Print day first with padded numbers (e.g. Tue 25/03)
    """

    # Movies
    runtime_format: RuntimeFormat = RuntimeFormat.hours_minutes
    """
    The format of movie runtimes.

    Values:

    * `hours-minutes` - Show hours and minutes (e.g. 1h 15m)
    * `minutes` - Show minutes only (e.g. 75 mins)
    """

    # Dates
    short_date_format: ShortDateFormat = ShortDateFormat.word_month_first
    """
    The format of short dates in the user interface.

    Values:

    * `word-month-first` - Month as word, print month first (e.g. Mar 4 2014)
    * `word-month-second` - Month as word, print month second (e.g. 4 Mar 2014)
    * `slash-month-first` - Slash-separated date, print month first (e.g. 03/4/2014)
    * `slash-month-first-padded` - Slash-separated date, print month first (e.g. 03/04/2014)
    * `slash-day-first` - Slash-separated date, print day first (e.g. 04/03/2014)
    * `iso8601` - ISO-8601 date (e.g. 2014-03-04)
    """

    long_date_format: LongDateFormat = LongDateFormat.month_first
    """
    The format of long dates in the user interface.

    Values:

    * `month-first` - Print month first (e.g. Tuesday, March 4 2014)
    * `day-first` - Print day first (e.g. Tuesday, 4 March 2014)
    """

    time_format: TimeFormat = TimeFormat.twelve_hour
    """
    The format of time in the user information.

    Values:

    * `twelve-hour` - 12-hour time (e.g. 5pm/5:30pm)
    * `twentyfour-hour` - 24-hour time (e.g. 17:00/17:30)
    """

    show_relative_dates: bool = True
    """
    When set to `True`, Radarr will show relative dates (e.g. today, yesterday)
    instead of absolute dates (e.g. Monday, Tuesday ...).
    """

    # Style
    theme: Theme = Theme.light
    """
    The theme to use when browsing the Radarr UI.

    Values:

    * `light` (Light-coloured theme)
    * `dark` (Dark-coloured theme)
    """

    enable_color_impaired_mode: bool = False
    """
    Enable an altered view style to allow colour-impaired users to better distinguish
    colour-coded information.
    """

    # Language
    movie_info_language: LowerCaseStr = "Original"  # type: ignore[assignment]

    ui_language: LowerCaseStr = "English"  # type: ignore[assignment]
    """
    The display language for the Radarr UI.

    Specify the language using the two-character language code.
    """

    @validator("movie_info_language", "ui_language")
    def disallow_any(cls, value: str) -> str:
        if value == "any":
            raise ValueError(
                "reserved language value 'any' cannot be specified for this attribute",
            )
        return value

    @validator("ui_language")
    def disallow_original(cls, value: str) -> str:
        if value == "original":
            raise ValueError(
                "reserved language value 'original' cannot be specified for this attribute",
            )
        return value

    @classmethod
    def _get_remote_map(cls, language_ids: Mapping[str, int]) -> List[RemoteMapEntry]:
        return [
            ("first_day_of_week", "firstDayOfWeek", {}),
            ("week_column_header", "calendarWeekColumnHeader", {}),
            ("runtime_format", "movieRuntimeFormat", {}),
            ("short_date_format", "shortDateFormat", {}),
            ("long_date_format", "longDateFormat", {}),
            ("time_format", "timeFormat", {}),
            ("show_relative_dates", "showRelativeDates", {}),
            ("theme", "theme", {}),
            ("enable_color_impaired_mode", "enableColorImpairedMode", {}),
            (
                "movie_info_language",
                "movieInfoLanguage",
                {
                    "decoder": lambda v: next(
                        language_name
                        for language_id, language_name in language_ids.items()
                        if language_id == v
                    ),
                    "encoder": lambda v: language_ids[v],
                },
            ),
            (
                "ui_language",
                "uiLanguage",
                {
                    "decoder": lambda v: next(
                        language_name
                        for language_id, language_name in language_ids.items()
                        if language_id == v
                    ),
                    "encoder": lambda v: language_ids[v],
                },
            ),
        ]

    @classmethod
    def from_remote(cls, secrets: RadarrSecrets) -> Self:
        with radarr_api_client(secrets=secrets) as api_client:
            language_ids: Dict[str, int] = {
                api_language.name_lower: api_language.id
                for api_language in radarr.LanguageApi(api_client).list_language()
            }
            api_ui_config = radarr.UiConfigApi(api_client).get_ui_config()
        return cls(
            **cls.get_local_attrs(
                remote_map=cls._get_remote_map(language_ids=language_ids),
                remote_attrs=api_ui_config.to_dict(),
            ),
        )

    def update_remote(
        self,
        tree: str,
        secrets: RadarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        with radarr_api_client(secrets=secrets) as api_client:
            language_ids: Dict[str, int] = {
                api_language.name_lower: api_language.id
                for api_language in radarr.LanguageApi(api_client).list_language()
            }
            updated, remote_attrs = self.get_update_remote_attrs(
                tree=tree,
                remote=remote,
                remote_map=self._get_remote_map(language_ids=language_ids),
                check_unmanaged=check_unmanaged,
                set_unchanged=True,
            )
            if updated:
                ui_config_api = radarr.UiConfigApi(api_client)
                config_id = ui_config_api.get_ui_config().id
                ui_config_api.update_ui_config(
                    id=str(config_id),
                    ui_config_resource=radarr.UiConfigResource.from_dict(
                        {"id": config_id, **remote_attrs},
                    ),
                )
                return True
            return False
