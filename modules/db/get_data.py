from typing import Union

import telebot.types

from modules.constants.users import OWNER
from modules.db.database import *


class GetData:
    def __init__(self, message: telebot.types.Message):
        self.user: telebot.types.User = message.from_user
        self.chat: telebot.types.Chat = message.chat

        self.user_id: int = self.user.id
        self.username: str = self.user.username
        self.usernik: str = self.user.full_name

        self.chat_id: int = self.chat.id
        self.chat_type: str = self.chat.type

    def get_chat(self) -> Chat:
        """
        Безопасно возвращает чат (при отсутствии в дб создаст запись)
        :return:
        """
        try:
            return Chat.get(chat_id=self.chat_id)
        except IndexError:
            return self.add_chat()

    def get_user(self) -> TgUser:
        """
        Возвращает пользователя, при отсутствии в дб создает запись
        :return:
        """
        try:
            return TgUser.get(telegram_id=self.user_id)
        except IndexError:
            return self.add_user()

    def add_chat(self) -> Chat:
        """
        Создает записи в таблицах Chat и AutoDeleteTime, добавляет новый чат
        :return:
        """
        new_chat = Chat.create(
            chat_id=self.chat_id,
            chat_type=self.chat_type
        )

        AutoDeleteTime.create(
            autodelete_time=30,
            chat=new_chat
        )

        return new_chat

    def add_user(self) -> TgUser:
        """
        Создает записи в таблицах TgUser, UserStatistics и UserChat, добавляет нового пользователя
        :return:
        """
        user_record = TgUser.create(
            telegram_id=self.user_id,
            user_nik=self.usernik,
            user_name=self.username,
            is_administrator_in_bot=False
        ).id

        UserStatistics.create(
            messages_per_day=1,
            messages_per_week=1,
            messages_per_all_time=1,
            user=user_record
        )

        UserChat.create(
            user=user_record,
            chat=self.get_chat()
        )

        return user_record

    @property
    def full_user_info(self):
        db_user = self.get_user()
        user_info: dict[Union[int, str, bool, list]] = {
            "user_id": self.user_id,
            "username": self.username,
            "usernik": self.usernik,
            "is_administrator_in_bot": db_user.is_administrator_in_bot,
            "is_owner": self.username in OWNER,
            "statistics": {
                "per_day": db_user.statistics.messages_per_day,
                "per_week": db_user.statistics.messages_per_week,
                "per_all_time": db_user.statistics.messages_per_all_time,
            },
            "chats_in": db_user.chats
        }
        return user_info
