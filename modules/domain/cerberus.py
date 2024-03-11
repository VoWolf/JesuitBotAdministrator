"""Объявляет класс бота (Cerberus)"""
import telebot.types

from modules.instances.bot_instance import bot
from modules.domain.message_form import MessageForm


class Cerberus:
    """Класс бота"""

    def __init__(self, message):
        self.message: telebot.types.Message = message
        self.chat_id: int = message.chat.id
        self.msg: MessageForm = MessageForm(message=message)

    def send(
            self,
            text: str,
            parse: str | None = None,
            buttons: list | None = None,
            protect: bool = False,
            silence: bool = False
    ) -> None:
        """
        Отправляет новое сообщение в указанный чат
        :param text: Текст сообщения
        :param parse: Нужен ли парс
        :param buttons: Кнопки под сообщением
        :param protect: Защитить сообщение от копирования и пересылки
        :param silence: Отправить сообщение без звука
        """
        bot.send_message(
            chat_id=self.chat_id,
            text=text,
            parse_mode=parse,
            reply_markup=buttons,
            protect_content=protect,
            disable_notification=silence
        )

    def reply(
        self,
        text: str
    ) -> None:
        """
        Отвечает на сообщение
        :param text: текст сообщения
        """
        bot.reply_to(self.message, text=text)

    def chat_member(
        self,
        username_or_userid: str | int
    ) -> telebot.types.User | None:
        """
        Возвращает информацию о пользователе с указанным юзернеймом или ID
        :param username_or_userid: Имя пользователя или ID участника группы
        """
        try:
            chat_member = bot.get_chat_member(chat_id=self.chat_id, user_id=username_or_userid)
        except Exception as e:
            self.error(text=f"Указан несуществующий юзернейм или ID пользователя! Ошибка: {e}")
            return
        return chat_member

    def error(
            self,
            text: str
    ) -> None:
        """
        Отправляет в чат сообщение об ошибке
        :param text: текст ошибки
        """
        self.send(text=self.msg.return_ready_message_text(sample="error", err_text=text))

    def change_autodelete_time(self) -> None:
        pass

    def add(self) -> telebot.types.User | None:
        pass
