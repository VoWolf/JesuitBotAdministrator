import telebot.types

from modules.db.database import *
from modules.domain.UserChat.Chat import ChatInfo
from modules.domain.UserChat.user import User


class GetData:
    def __init__(self, message: telebot.types.Message):
        self.user: telebot.types.User = message.from_user
        self.chat: telebot.types.Chat = message.chat

        self.user_id: int = self.user.id
        self.username: str = self.user.username
        self.usernik: str = self.user.full_name

        self.chat_id: int = self.chat.id
        self.chat_type: str = self.chat.type

    def get_db_chat(self) -> Chat:
        """
        Безопасно возвращает чат (при отсутствии в дб создаст запись)
        :return:
        """
        try:
            return Chat.get(chat_id=self.chat_id)
        except IndexError:
            return self.add_chat()

    def get_db_user(self) -> TgUser:
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
            chat=self.get_db_chat()
        )

        return user_record

    @property
    def full_user_info(self):
        db_user = self.get_db_user()
        user_info: User = User(
            user_id=self.user_id,
            username=self.username,
            usernik=self.usernik,
            db_user=db_user
        )
        return user_info

    @property
    def full_chat_info(self):
        db_chat: Chat = self.get_db_chat()
        chat_info: ChatInfo = ChatInfo(
            db_chat
        )
        return chat_info
