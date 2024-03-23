"""Объявляет класс бота (CERBERUS)"""
import telebot.types

from modules.instances.bot_instance import BOT


class Cerberus:
    """Класс бота"""

    def __init__(self, message: telebot.types.Message):
        self.message: telebot.types.Message = message
        self.chat_id: int = message.chat.id

    def send(
            self,
            text: str,
            parse: str | None = None,
            buttons: telebot.types.InlineKeyboardMarkup | telebot.types.ReplyKeyboardMarkup | None = None,
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
        BOT.send_message(
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
        BOT.reply_to(self.message, text=text)

    def count_chat_members(self) -> int:
        return BOT.get_chat_member_count(chat_id=self.chat_id)

    def edit(
            self,
            message_id: int,
            new_text: str,
            parse: str | None = None,
            buttons: telebot.types.ReplyKeyboardMarkup | telebot.types.InlineKeyboardMarkup | None = None
    ) -> None:
        """
        Изменяет сообщение с введенным message_id
        :param message_id: ID сообщения
        :param new_text: ID чата
        :param parse: Нужно ли форматировать текст?
        :param buttons: Кнопки под сообщением
        :return:
        """
        BOT.edit_message_text(
            text=new_text,
            chat_id=self.chat_id,
            message_id=message_id,
            parse_mode=parse,
            reply_markup=buttons,
        )

    def chat_member(
        self,
        username_or_userid: str | int
    ) -> telebot.types.User | None:
        """
        Возвращает информацию о пользователе с указанным юзернеймом или ID
        :param username_or_userid: Имя пользователя или ID участника группы
        """
        try:
            chat_member = BOT.get_chat_member(chat_id=self.chat_id, user_id=username_or_userid)
        except Exception:
            self.error()  # add Error
            return
        return chat_member

    def error(self):
        pass

    def change_autodelete_time(self) -> None:
        pass

    def add(self) -> telebot.types.User | None:
        pass
