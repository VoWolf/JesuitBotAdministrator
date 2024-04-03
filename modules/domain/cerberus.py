"""Объявляет класс бота (CERBERUS)"""
import datetime

import telebot.types

from modules.constants.PyMorphy3_analyzer import MORPH
from modules.db.Tables.TgUserTables import TgUser
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
            disable_notification=silence,
            disable_web_page_preview=True
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

    def poll(
            self,
            question: str,
            answers: list[str],
            anonymous: bool,
            quiz: bool,
            correct: int | None= None,
            expl: str | None = None,
            many_answers: bool = False,
            until: datetime | None = None
    ):
        BOT.send_poll(
            chat_id=self.chat_id,
            question=question,
            options=answers,
            is_anonymous=anonymous,
            type="quiz" if quiz else "regular",
            correct_option_id=correct,
            explanation=expl,
            allows_multiple_answers=many_answers,
            close_date=until
        )

    def pin(
        self,
        message_id_delta: int
    ):
        BOT.pin_chat_message(
            chat_id=self.chat_id,
            message_id=self.message.id + message_id_delta,
            disable_notification=False
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

    def ban(self, reason, user_id, username):
        print(user_id)
        BOT.ban_chat_member(
            chat_id=self.chat_id,
            user_id=user_id
        )
        self.send(text=f"@{username} забанен НАВСЕГДА. Причина: {reason}")

    def error(self):
        pass

    def mute(self, user: TgUser, is_reply: bool):
        try:
            text = self.message.text.split()[1] if is_reply else self.message.text.split()[2]
            duration = int(text)

            if duration < 1 or duration > 1440:
                raise TypeError("Необходимо указать значение от 1 до 1440!")
        except (IndexError, ValueError, TypeError) as e:
            print(e)
            self.reply("Необходимо указать имя пользователя (или использовать команду ответом на сообщение) и число от "
                       "1 до 1440 (Длительность мьюта в минутах)!")
            return

        BOT.restrict_chat_member(
            chat_id=self.chat_id,
            user_id=user.telegram_id,
            until_date=datetime.datetime.now() + datetime.timedelta(minutes=duration)
        )

        self.send(f"{user.user_nik}, ты замьючен на {duration} "
                  f"{MORPH.parse('минута')[0].make_agree_with_number(duration).word}, отдыхай!")

    def unmute(self, user: TgUser):
        BOT.restrict_chat_member(
            chat_id=self.chat_id,
            user_id=user.telegram_id,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )

        self.send(f"{user.user_nik}, теперь ты свободен! Будь аккуратнее и не зли админов:)")
