import time

from modules.constants.words import FORBIDDEN_WORDS
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

    def send(self, text):
        bot.send_message(self.chat_id, text)

    def start(self):
        """Sends start message"""
        self.send("Привет! Я бот администратор, помогаю управлять чатом:)")

    def is_user_admin(self):
        if not self.message_author.is_admin:
            self.reply("Ты не можешь этого сделать!)")
            return False
        return True

    def reply(self, text: str):
        bot.reply_to(self.message, text)

    def mute_user(self):
        """Mute user"""
        if not self.reply_to_message_author:
            self.reply("Эту команду надо использовать ответом на сообщение!")

            return

        if not self.is_user_admin():
            return

        try:
            duration = extract_duration(self.message.text)
        except ValueError as err:
            self.reply(str(err.args))

            return

        if self.reply_to_message_author.can_be_muted:
            bot.restrict_chat_member(
                self.chat_id,
                self.reply_to_message_author.user_id,
                until_date=time.time() + duration * 60,
            )

            self.reply(
                f"Пользователь {self.reply_to_message_author.username} замучен на {duration} минут."
            )
        else:
            self.reply("К сожалению, бога забанить невозможно!")

    def unmute_user(self):
        """Unmute user"""
        if not self.reply_to_message_author:
            self.reply("Эту команду надо использовать ответом на сообщение!")

            return

        bot.restrict_chat_member(
            self.chat_id,
            self.reply_to_message_author.user_id,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
        )

        self.reply(f"{self.reply_to_message_author.username} освобожден!")

    def print_forbidden_words(self):
        if not self.is_user_admin():
            return

        self.send(str(FORBIDDEN_WORDS))


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
