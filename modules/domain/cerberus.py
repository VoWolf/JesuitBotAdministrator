"""Объявляет класс бота (Cerberus)"""

import time
from typing import Callable

from modules.db.database import ForbiddenWord
from modules.domain.user import User
from modules.instances.bot_instance import bot


def admin_guard(func: Callable):
    """
    Декоратор для проверки является ли пользователь
    администратором
    :param func:
    :return:
    """
    def inner(self):
        if not self.is_user_admin():
            return
        func(self)

    return inner


def reply_user_guard(func: Callable):
    """
    Декоратор для проверки используется ли команда ответом
    на сообщение
    :param func:
    :return:
    """
    def inner(self):
        if not self.is_reply_to_message_author_exists():
            return
        func(self)

    return inner


class Cerberus:
    """Bot class"""

    def __init__(self, message, user=False, message_form=False, forbidden_words=False):
        self.message = message
        self.chat_id = message.chat.id

        if user:
            if message.reply_to_message:
                self.reply_to_message_author = User(
                    user_id=message.reply_to_message.from_user.id,
                    chat_id=message.chat.id
                )
            else:
                self.reply_to_message_author = None

            self.message_author = User(
                user_id=message.from_user.id,
                chat_id=message.chat.id
            )

        if message_form:
            pass

        if forbidden_words:
            pass

    def send(self, text):
        """
        Отправляет новое сообщение
        :param text:
        :return:
        """
        bot.send_message(self.chat_id, text)

    def start(self):
        """
        Отправляет сообщение по команде
        /start
        :return:
        """
        self.send("Привет! Я бот администратор, помогаю управлять чатом:)")

    def reply(self, text: str):
        """
        Отвечает на сообщение
        :param text:
        :return:
        """
        bot.reply_to(self.message, text)

    def is_user_admin(self):
        """
        Проверяет, является ли пользователь администратором
        :return: True если пользователь администратор, False если пользователь не администратор
        """
        if not self.message_author.is_admin:
            self.reply("Ты не можешь этого сделать!)")
            return False
        return True

    def is_reply_to_message_author_exists(self):
        """
        Проверяет, использована ли
        команда ответом на сообщение
        :return:
        """
        if not self.reply_to_message_author:
            self.reply("Эту команду надо использовать ответом на сообщение!")
            return False
        return True

    def refresh_forbidden_words(self):
        """Reloads forbidden words from database"""
        pass

    @admin_guard
    def print_forbidden_words(self):
        """Prints forbidden words list"""
        query = ForbiddenWord.select()

        self.send(str([fw.word for fw in query]))

    @admin_guard
    def add_forbidden_word(self):
        """Adds forbidden word"""
        try:
            extract_and_add_forbidden_word(self.message.text)
            self.send("Список запрещенных слов обновлен!")
            self.refresh_forbidden_words()
        except ValueError as err:
            self.reply(str(err.args))

    @admin_guard
    def remove_forbidden_word(self):
        """Removes forbidden word"""
        try:
            extract_and_remove_forbidden_word(self.message.text)
            self.send("Список запрещенных слов обновлен!")
            self.refresh_forbidden_words()
        except ValueError as err:
            self.reply(str(err.args))

    def handle_message(self):
        """Controls message for forbidden words"""
        pass


def extract_pilot_params(text: str):
    args_list = text.split()

    if len(args_list) < 3:
        raise ValueError(
            f"Тебе нужно указать время автомьюта и время автоудаления после предупреждения ",
            f"через пробел от команды. \n*Для дураков: ЭТО ЧИСЛА!",
        )

    try:
        mute_time = int(args_list[1])
    except Exception as exc:
        raise ValueError(
            "Время автомьюта должно быть числом (первый параметр)"
        ) from exc

    try:
        mute_break_time = int(args_list[2])
    except Exception as exc:
        raise ValueError(
            "Время автоудаления после предупреждения должно быть числом (второй параметр)"
        ) from exc

    return mute_time, mute_break_time


def extract_duration(text: str):
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


def extract_and_add_forbidden_word(text: str):
    args_list = list(map(str.strip, text.strip().split()))

    if len(args_list) == 1:
        raise ValueError("Не указано запрещенное слово")

    forbidden_word = args_list[1].lower()
    forbidden_word_offset = 0

    if len(args_list) == 3:
        try:
            forbidden_word_offset = int(args_list[2])
        except Exception as exc:
            raise ValueError(
                "Произошла ошибка! Скорее всего, ты указал несуществующий индекс!"
            ) from exc

    if forbidden_word_offset != 0:
        forbidden_word = forbidden_word[0:-forbidden_word_offset]

    ForbiddenWord.create(word=forbidden_word)


def extract_and_remove_forbidden_word(text: str):
    args_list = text.strip().split()

    if len(args_list) == 1:
        raise ValueError("Не указано запрещенное слово")

    if len(args_list) == 3:
        print("1")
        try:
            ForbiddenWord.delete_by_id(int(args_list[2]))
        except Exception as exc:
            raise ValueError(
                "Произошла ошибка! Скорее всего, ты указал несуществующий индекс!"
            ) from exc
    else:
        forbidden_word = args_list[1].lower()


        try:
            fw = ForbiddenWord.get(ForbiddenWord.word == forbidden_word)
        except Exception:
            raise ValueError(
                "Данного слова нет в базе!"
            )
        fw.delete_instance()
