"""Объявляет класс бота (Cerberus)"""

import random
import string

from modules.db.database import Chats
from modules.instances.bot_instance import bot
from message_form import MessageForm


class Cerberus:
    """Класс бота"""

    def __init__(self, message):
        self.message = message
        self.chat_id = message.chat.id
        self.msg = MessageForm(message=message)

    def send(
            self,
            text: str,
            chats_pare: Chats,
            admin_chat: bool = False,
            user_chat: bool = False,
            parse: bool = False,
            buttons: list | None = None
    ) -> None:
        """
        Отправляет новое сообщение в указанный чат
        """
        bot.send_message(
            chat_id=c
        )

    def reply(self, text: str) -> None:
        """
        Отвечает на сообщение
        :param text: текст сообщения
        """
        bot.reply_to(self.message, text)

    def my_rating(self) -> None:
        """
        Высылает в чат текущий рейтинг пользователя
        """
        self.send(
            text=self.msg.return_ready_message_text(
                sample=9,
                value_1=self.message_author.username,
                value_2=self.message_author.db_user.ratings.spam_rating,
                value_3=self.message_author.db_user.ratings.toxic_rating,
            )
        )

    def tie_chats(self) -> None:
        """
        Начинает связывание чатов
        :return: int token
        """
        tkn = "".join(random.choices(string.hexdigits, k=16))
        Chats.create(
            main_chat_control_id=self.chat_id, admin_chat_id=0, token_for_tie=tkn
        ).save()
        self.send(
            self.msg.return_ready_message_text(sample=14, value_1=tkn, value_2=tkn)
        )

    def snap_chats(self) -> None:
        """
        Завершает связывание чатов
        :return:
        """
        tokn = self.extract_params(
            error_text="Вы не указали токен для связывания!", args_count=1
        )
        if tokn is None:
            return

        try:
            chat = Chats.get(token_for_tie=tokn)
        except IndexError:
            self.send(
                self.msg.return_ready_message_text(
                    sample=16, value_1="Вы указали несуществующий токен!"
                )
            )
            return
        chat.admin_chat_id = self.chat_id
        Chats.save(chat)
        self.send(self.msg.return_ready_message_text(sample=15))

    def error(self, text):
        self.send(text=self.msg.return_ready_message_text(sample=16, err_text=text))

    def change_autodelete_time(self) -> None:
        """
        Меняет скорость автоудаления сообщений бота
        :return:
        """
        new_time = self.extract_params(
            args_count=1,
            error_text="Ты не указал новое время автоудаления!",
        )
        try:
            new_time = int(new_time)
        except ValueError:
            self.error(
                text="К сожалению, вы указали не тот тип данных! Пример использования команды: "
                     "/change_autodelete_time [новое значение, число, сек]"
            )
        self.msg.change_autodelete_time(new_time=new_time)
        self.send(
            text=self.msg.return_ready_message_text(
                sample=13, value_1=new_time, value_2=self.message_author
            )
        )

    def add(self):
        pass

    def handle_message(self) -> bool:
        """
        Проверяет сообщение на наличие токсичности
        """
        pass
