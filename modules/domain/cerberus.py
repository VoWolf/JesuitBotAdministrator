import time

from modules.constants.words import forbidden_words
from modules.domain.user import User
from modules.instances.bot_instance import bot


class Cerberus:
    """Bot class"""

    def __init__(self, message):
        self.message = message
        self.chat_id = message.chat.id

        if message.reply_to_message:
            self.reply_to_message_author = User(
                username=message.reply_to_message.from_user.username,
                user_id=message.reply_to_message.from_user.id,
            )
        else:
            self.reply_to_message_author = None

        self.message_author = User(
            username=message.from_user.username,
            user_id=message.from_user.id,
        )

    def start(self):
        """Sends start message"""
        bot.send_message(
            self.chat_id, "Привет! Я бот администратор, помогаю управлять чатом:)"
        )

    def mute_user(self):
        """Mute user"""
        if not self.reply_to_message_author:
            bot.reply_to(
                self.message, "Эту команду надо использовать ответом на сообщение!"
            )

            return

        if not self.message_author.is_admin:
            bot.reply_to(self.message, "Ты не можешь этого сделать!)")

            return

        try:
            duration = extract_duration(self.message.text)
        except ValueError as err:
            bot.reply_to(self.message, str(err.args))
            return

        if self.reply_to_message_author.can_be_muted:
            bot.restrict_chat_member(
                self.chat_id,
                self.reply_to_message_author.user_id,
                until_date=time.time() + duration * 60,
            )

            bot.reply_to(
                self.message,
                f"Пользователь {self.reply_to_message_author.username} замучен на {duration} минут.",
            )
        else:
            bot.reply_to(self.message, "К сожалению, бога забанить невозможно!")

    def unmute_user(self):
        """Unmute user"""
        if not self.reply_to_message_author:
            bot.reply_to(
                self.message, "Эту команду надо использовать ответом на сообщение!"
            )
            return

        bot.restrict_chat_member(
            self.chat_id,
            self.reply_to_message_author.user_id,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
        )

        bot.reply_to(
            self.message, f"{self.reply_to_message_author.username} освобожден!"
        )

    def print_forbidden_words(self):
        if self.reply_to_message_author.is_admin:
            bot.send_message(self.chat_id, str(forbidden_words))
        else:
            bot.send_message(self.chat_id, "Ты не можешь этого сделать!)")


def extract_duration(text):
    duration = 5

    if not text:
        return duration

    args_list = text.split()

    if len(args_list) == 1:
        return duration

    try:
        duration = int(args_list[1])
    except Exception as exc:
        raise ValueError("Неправильный формат времени!") from exc

    if duration < 1:
        raise ValueError("Минимальное время 1 минута!")

    if duration > 1440:
        raise ValueError("Максимальное время 24 часа (1440 минут)!")

    return duration
