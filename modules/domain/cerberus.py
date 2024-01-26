import time

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
        """Sends new message"""
        bot.send_message(self.chat_id, text)

    def start(self):
        """Sends start message"""
        self.send("Привет! Я бот администратор, помогаю управлять чатом:)")

    def reply(self, text: str):
        """Replies to message"""
        bot.reply_to(self.message, text)

    def is_user_admin(self):
        """Checks if user is admin"""
        if not self.message_author.is_admin:
            self.reply("Ты не можешь этого сделать!)")
            return False
        return True

    def is_reply_to_message_author_exists(self):
        """Checks if author of reply to message exists"""
        if not self.reply_to_message_author:
            self.reply("Эту команду надо использовать ответом на сообщение!")
            return False
        return True

    def mute_user(self):
        """Mutes user"""
        if not self.is_reply_to_message_author_exists:
            return

        if not self.is_user_admin():
            return

        try:
            mute_duration = extract_duration(self.message.text)
        except ValueError as err:
            self.reply(str(err.args))

            return

        if self.reply_to_message_author.can_be_muted:
            bot.restrict_chat_member(
                self.chat_id,
                self.reply_to_message_author.user_id,
                until_date=time.time() + mute_duration * 60,
            )

            self.reply(
                f"Пользователь {self.reply_to_message_author.username} замуьючен на {mute_duration} минут."
            )
        else:
            self.reply("К сожалению, бога забанить невозможно!")

    def unmute_user(self):
        """Unmutes user"""
        if not self.is_reply_to_message_author_exists:
            return

        if not self.is_user_admin():
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
        """Prints forbidden words list"""
        if not self.is_user_admin():
            return

        self.send(str(FORBIDDEN_WORDS))

    def add_forbidden_word(self):
        if not self.is_user_admin():
            return

        try:
            extract_and_add_forbidden_word(self.message)
            self.send("Список запрещенных слов обновлен!")
        except ValueError as err:
            self.reply(str(err.args))


def extract_duration(text):
    """Extracts second word from string as duration(int)"""
    duration = 5

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


def extract_and_add_forbidden_word(text):
    global FORBIDDEN_WORDS
    args_list = text.split()

    if len(args_list) == 1:
        raise ValueError("Не указано запрещенное слово")

    forbidden_word = args_list[1].lower()
    forbidden_word_offset = 0

    if len(args_list) == 2:
        try:
            forbidden_word_offset = int(args_list[2])
        except Exception as exc:
            raise ValueError(
                "Произошла ошибка! Скорее всего, ты указал несуществующий индекс!"
            ) from exc

    if forbidden_word_offset != 0:
        forbidden_word = forbidden_word[0:-forbidden_word_offset]

    FORBIDDEN_WORDS.append(forbidden_word)
