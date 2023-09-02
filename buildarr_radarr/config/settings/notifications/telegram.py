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
Telegram notification connection configuration.
"""


from __future__ import annotations

from typing import List, Literal

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr, Password

from .base import Notification


class TelegramNotification(Notification):
    """
    Send media update and health alert messages to a Telegram chat room.
    """

    type: Literal["telegram"] = "telegram"
    """
    Type value associated with this kind of connection.
    """

    bot_token: Password
    """
    The bot token assigned to this application.
    """

    chat_id: NonEmptyStr
    """
    The ID of the chat room to send messages to.

    You must start a conversation with the bot or add it to your group to receive messages.
    """

    send_silently: bool = False
    """
    Sends the message silently. Users will receive a notification with no sound.
    """

    _implementation: str = "Telegram"
    _remote_map: List[RemoteMapEntry] = [
        ("bot_token", "botToken", {"is_field": True}),
        ("chat_id", "chatId", {"is_field": True}),
        ("send_silently", "sendSilently", {"is_field": True}),
    ]
