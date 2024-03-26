import datetime

import telebot.types

from modules.db.Tables.ChatTables import Chat, UserChat
from modules.db.Tables.TgUserTables import TgUser, InactiveData
from modules.db.Tables.WalksTables import Walks, Place
from modules.db.TypeObjects.ChatObject import ChatInfo
from modules.db.TypeObjects.UserObject import User


class GetData:
    def __init__(self, message: telebot.types.Message):
        self.user: telebot.types.User = message.from_user
        self.user_id = self.user.id

        self.chat: telebot.types.Chat = message.chat
        self.chat_id = self.chat.id

    @property
    def full_chat_info(self):
        try:
            return ChatInfo(db_chat=Chat.get(chat_id=self.chat_id))
        except Exception as e:
            print(e)
            return ChatInfo(db_chat=self.add_chat())

    def add_chat(self) -> Chat:
        new_chat = Chat.create(
            chat_id=self.chat_id,
            chat_type=self.chat.type
        )
        return new_chat

    @property
    def full_user_info(self):
        try:
            db_user = TgUser.get(telegram_id=self.user_id)
        except Exception as e:
            print(e)
            db_user = self.add_user()
        return User(
            db_user=db_user
        )

    def add_user(self) -> TgUser:
        new_user = TgUser.create(
            telegram_id=self.user_id,
            user_nik=self.user.full_name,
            user_name=self.user.username,
            is_administrator_in_bot=False
        )
        InactiveData.create(
            warned_to_go=False,
            inactive_days_counter=0,
            warned_to_go_valid_until=datetime.datetime.now(),
            free_days="null",
            user=new_user
        )
        UserChat.create(
            user=new_user,
            chat=self.full_chat_info.chat_id
        )
        return new_user

    @staticmethod
    def get_by_username(username) -> TgUser | None:
        try:
            return TgUser.get(user_name=username)
        except IndexError:
            return None

    def add_walk(
            self,
            username: str,
            name: str,
            time_start: datetime,
            time_end: datetime,
            metro_thread: str,
            metro_station: str,
            location: str
    ) -> None:
        new_walk = Walks.create(
            name=name,
            time_start=time_start,
            time_end=time_end,
            people=username + ", ",
            chat=self.full_chat_info.db_chat
        )
        Place.create(
            city="Москва",
            metro_thread=metro_thread,
            metro_station=metro_station,
            location=location,
            walk=new_walk
        )
