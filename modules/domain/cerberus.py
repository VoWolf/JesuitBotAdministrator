"""Объявляет класс бота (Cerberus)"""

import time, string, random

from modules.db.database import Chats
from modules.instances.bot_instance import bot

from modules.domain.user import User
from modules.domain.forbidden_words import ForbiddenWords
from modules.domain.message_form import MessageForm
from modules.domain.add_vote import Vote


def admin_guard(func):
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


def reply_user_guard(func):
    """
    Декоратор для проверки используется ли команда ответом
    на сообщение
    :param func:
    :return:
    """

    def inner(self):
        if not self.message.reply_to_message:
            return
        func(self)

    return inner


def redirect_regular_chat_member_to_vote(func):
    """
    Декоратор для перезаправки пользователей, не имеющих статуса администратора:
    те попадут на другой метод, начинающий голосование
    :param func:
    :return:
    """

    def inner(self):
        if self.message_author.is_admin:
            func(self)
        else:
            pass

    return inner


def creator_guard(func):
    """
    Декоратор для проверки использована ли
    команда пользователем LastUwUlf
    :param func:
    :return:
    """

    def inner(self):
        if not self.message.from_user.username == "LastUwUlf":
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

            self.message_author = User(
                user_id=message.from_user.id,
                chat_id=message.chat.id
            )
        else:
            self.reply_to_message_author = None
            self.message_author = None

        if message_form:
            self.msg = MessageForm(
                message=self.message
            )
        else:
            self.msg = None

        if forbidden_words:
            self.forbidden_word = ForbiddenWords()
        else:
            self.forbidden_word = None

    def send(self, text, buttons=None, parse=False):
        """
        Отправляет новое сообщение
        :param text:
        :param buttons:
        :param parse:
        :return:
        """
        if buttons:
            bot.send_message(self.chat_id, text, reply_markup=buttons, parse_mode="HTML")
        elif parse:
            bot.send_message(self.chat_id, text, parse_mode="HTML")
        else:
            bot.send_message(self.chat_id, text)

    def send_in_admin_chat(self, text):
        """
        Отправляет новое сообщение в чат с администрацией
        :param text:
        :return:
        """
        bot.send_message(chat_id=Chats.get(main_chat_control_id=self.chat_id).admin_chat_id, text=text)

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
        self.forbidden_word.refresh_forbidden_words()

    def reply(self, text: str):
        """
        Отвечает на сообщение
        :param text:
        :return:
        """
        bot.reply_to(self.message, text)

    def start(self):
        """
        Отправляет сообщение по команде
        /start
        :return:
        """
        self.send(self.msg.return_ready_message_text(
            sample=8
        ))

    def my_rating(self):
        """
        Высылает в чат текущий рейтинг пользователя
        :return:
        """
        self.send(
            text=self.msg.return_ready_message_text(
                sample=9,
                value_1=self.message_author.username,
                value_2=self.message_author.db_user.in_TgUserRating_table.spam_rating,
                value_3=self.message_author.db_user.in_TgUserRating_table.toxic_rating
            )
        )

    def extract_params(self, error_code: str, values_count):
        """
        Извлекает из текста сообщения нужные параметры для команд;
        В случае ошибки отправляет соответствующее сообщение
        :param error_code:
        :param values_count:
        :return str:
        """
        text = self.msg.message_text.split()

        if values_count == "end":
            return text[1:]

        if len(text) + 1 != values_count:
            self.send(text=self.msg.return_ready_message_text(
                sample=16,
                value_1=error_code
            ))
            return None

        text = text[1:values_count + 1]
        return text

    @admin_guard
    def extract_and_add_forbidden_word(self):
        """
        Извлекает из команды новое слово и
        добавляет его к списку запрещенных слов
        :return:
        """
        word = self.extract_params(
            error_code="Не указано запрещенное слово! (формат ввода данной команды: /add_forbidden_word "
                       "[слово, которое вы хотите добавить])",
            values_count=1
        )

        if word:
            self.forbidden_word.add_forbidden_word(
                word=word[0]
            )

    @admin_guard
    def extract_and_remove_forbidden_word(self):
        """
        Извлекает из команды новое слово и
        удаляет его из списка запрещенных слов
        :return:
        """
        word = self.extract_params(
            error_code="К сожалению, не указано запрещенное слово! (формат ввода данной команды: "
                       "/delete_forbidden_word [слово, которое вы хотите удалить])",
            values_count=1
        )

        if word is None:
            return

        try:
            self.forbidden_word.delete_forbidden_word(
                word=word
            )
        except KeyboardInterrupt:
            self.send(text=self.msg.return_ready_message_text(
                sample=16,
                value_1="К сожалению, введенного вами слово нет в базе данных! (формат ввода данной команды: "
                        "/delete_forbidden_word [слово, которое вы хотите удалить])"
            ))

    @creator_guard
    @reply_user_guard
    def extract_and_change_rating(self):
        """
         Меняет указанный рейтинг выбранного пользователя
         на указанное число
        :return:
        """
        rating_type, new_rating = self.extract_params(
            error_code="К сожалению, не указаны все необходимые параметры! (Формат ввода данной команды:"
                       "/rating_change [юзернейм] [тип рейтинга] [новый рейтинг])",
            values_count=2
        )

        if rating_type is None or new_rating is None:
            return
# Поменять, а то значения не сохраняются
        if rating_type.lower() == "спам":
            self.reply_to_message_author.db_user.in_TgUserRating_table.spam_rating = new_rating
        elif rating_type.lower() == "токсик":
            self.reply_to_message_author.db_user.in_TgUserRating_table.toxic_rating = new_rating
        else:
            self.send(
                self.msg.return_ready_message_text(
                    sample=16,
                    value_1="Указан несуществующий тип рейтинга!\nСпам - поменять спам рейтинг\nТоксик - поменять"
                            " рейтинг токсичности"
                )
            )
            return
        self.send(
            self.msg.return_ready_message_text(
                sample=12,
                value_1=self.reply_to_message_author.user_name,
                value_2=new_rating,
                value_3=self.message_author.user_name
            )
        )

    @creator_guard
    def tie_chats(self):
        """
        Начинает связывание чатов
        :return: int token
        """
        tkn = "".join(random.choices(string.hexdigits, k=16))
        Chats.create(
            main_chat_control_id=self.chat_id,
            admin_chat_id=0,
            token_for_tie=tkn
        ).save()
        self.send(
            self.msg.return_ready_message_text(
                sample=14,
                value_1=tkn,
                value_2=tkn
            )
        )

    @creator_guard
    def snap_chats(self):
        """
        Завершает связывание чатов
        :return:
        """
        tokn = self.extract_params(
            error_code="Вы не указали токен для связывания!",
            values_count=1
        )
        if tokn is None:
            return

        try:
            chat = Chats.get(token_for_tie=tokn)
        except IndexError:
            self.send(
                self.msg.return_ready_message_text(
                    sample=16,
                    value_1="Вы указали несуществующий токен!"
                )
            )
            return
        chat.admin_chat_id = self.chat_id
        Chats.save(chat)
        self.send(
            self.msg.return_ready_message_text(
                sample=15
            )
        )

    def error(self, text):
        self.send(
            text=self.msg.return_ready_message_text(
                sample=16,
                err_text=text
            )
        )

    @admin_guard
    def change_autodelete_time(self):
        """
        Меняет скорость автоудаления сообщений бота
        :return:
        """
        new_time = self.extract_params(
            values_count=1,
            error_code="Ты не указал новое время автоудаления!",
        )
        try:
            new_time = int(new_time)
        except ValueError:
            self.error(text="К сожалению, вы указали не тот тип данных! Пример использования команды: "
                            "/change_autodelete_time [новое значение, число, сек]")
        self.msg.change_autodelete_time(
            new_time=new_time
        )
        self.send(
            text=self.msg.return_ready_message_text(
                sample=13,
                value_1=new_time,
                value_2=self.message_author
            )
        )

    @creator_guard
    @redirect_regular_chat_member_to_vote
    @reply_user_guard
    def admin_stat(self):
        """"
        Назначает выбранного пользователя администратором
        """
        self.reply_to_message_author.make_user_admin(admin=True)
        self.send(
            text=self.msg.return_ready_message_text(
                sample=17,
                value_1=self.reply_to_message_author.username
            )
        )

    @creator_guard
    @redirect_regular_chat_member_to_vote
    @reply_user_guard
    def delete_admin_stat(self):
        """
        Снимает выбранного пользователя с должности администратора
        :return:
        """
        self.reply_to_message_author.make_user_admin(admin=False)
        self.send(
            text=self.msg.return_ready_message_text(
                sample=18,
                value_1=self.reply_to_message_author.username
            )
        )

    @admin_guard
    @redirect_regular_chat_member_to_vote
    def kick_user(self, kick=False):
        """
        Банит пользователя на определенный срок
        :return:
        """
        params = self.extract_params(
            error_code="Вы указали недостаточное количество параметров! Пример использования команды: /kick "
                       "[@username (если не ответом на сообщение)] [Срок (минимум - 30, сек)] [причина]",
            values_count="end"
        )
        if params is None:
            return

        username = params[0] if "@" in params[0] else None
        duration = params[1] if "@" in params[0] and not kick else params[0]
        reason = params[2:] if duration == params[1] else params[1:]

        if not kick:
            try:
                duration = int(duration)
            except ValueError:
                self.error(text="Длительность должна быть целым числом! Пример использования команды: /kick "
                           "[@username (если не ответом на сообщение)] [Срок (минимум - 30, сек)] [причина]")
                return

        if not reason:
            self.error(text="Вы не указали причину для бана участника! /kick [@username (если не ответом на "
                            "сообщение)] [Срок (минимум - 30, сек)] [причина]")
            return

        user_to_kick = User(
            user_id=bot.get_chat_member(chat_id=self.chat_id, user_id=username[1:]).user.id,
            chat_id=self.chat_id
        )
        user_to_kick.ban_user(
            bot=bot,
            duration=duration,
            kick=kick
        )

    def reply_kick_user(self):
        pass

    @redirect_regular_chat_member_to_vote
    def add(self):
        pass

    def handle_message(self):
        """
        Проверяет сообщение на наличие токсичности
        :return:
        """
        pass
