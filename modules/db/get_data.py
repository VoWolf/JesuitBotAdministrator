import telebot.types

from modules.db.Tables.ChatTables import Chat, AutoDeleteTime, UserChat
from modules.db.Tables.TgUserTables import TgUser, UserStatistics, InactiveDays
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
        except IndexError:
            return ChatInfo(db_chat=self.add_chat())

    def add_chat(self) -> Chat:
        new_chat = Chat.create(
            chat_id=self.chat_id,
            chat_type=self.chat.type
        )
        AutoDeleteTime.create(
            autodelete_time=30,
            chat=new_chat
        )
        return new_chat

    @property
    def full_user_info(self):
        try:
            db_user = TgUser.get(telegram_id=self.user_id)
        except IndexError:
            db_user = self.add_user()
        return User(
            user_id=self.user_id,
            username=self.user.username,
            usernik=self.user.full_name,
            db_user=db_user
        )

    def add_user(self) -> TgUser:
        new_user = TgUser.create(
            telegram_id=self.user_id,
            user_nik=self.user.full_name,
            user_name=self.user.username,
            is_administrator_in_bot=False
        )
        UserStatistics.create(
            messages_per_day=1,
            messages_per_week=1,
            messages_per_mouth=1,
            messages_per_all_time=1,
            user=new_user
        )
        InactiveDays.create(
            warned_to_go=False,
            inactive_days_counter=0,
            free_days="",
            user=new_user
        )
        UserChat.create(
            user=new_user,
            chat=Chat.get(chat_id=self.chat_id)
        )
        return new_user

    @staticmethod
    def get_by_username(username) -> TgUser | None:
        try:
            return TgUser.get(user_name=username)
        except IndexError:
            return None
