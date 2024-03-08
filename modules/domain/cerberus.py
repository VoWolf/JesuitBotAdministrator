"""Объявляет класс бота (Cerberus)"""

import random
import string

from modules.constants.users import OWNER
from modules.db.database import Chats
from modules.domain.forbidden_words import ForbiddenWords
from modules.domain.message_form import MessageForm
from modules.domain.user import User
from modules.instances.bot_instance import bot


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
    Декоратор для проверки использована ли команда пользователем LastUwUlf
    :param func: Функция-callback
    :returns: callable
    """

    def inner(self):
        if not self.message.from_user.username == OWNER:
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
                    chat_id=message.chat.id,
                )

            self.message_author = User(
                user_id=message.from_user.id, chat_id=message.chat.id
            )
        else:
            self.reply_to_message_author = None
            self.message_author = None

        if message_form:
            self.msg = MessageForm(message=self.message)
        else:
            self.msg = None

        if forbidden_words:
            self.forbidden_word = ForbiddenWords()
        else:
            self.forbidden_word = None

    def send(self, text: str, buttons: list = None, parse: bool = False) -> None:
        """
        Отправляет новое сообщение
        :param text: Текст сообщения
        :param buttons: Список с кнопками, которые нужно добавить под сообщение
        :param parse: Нужен ли parse_mode?
        """
        if buttons:
            bot.send_message(
                self.chat_id, text, reply_markup=buttons, parse_mode="HTML"
            )
        elif parse:
            bot.send_message(self.chat_id, text, parse_mode="HTML")
        else:
            bot.send_message(self.chat_id, text)

    def send_in_admin_chat(self, text: str) -> None:
        """
        Отправляет новое сообщение в чат с администрацией
        :param text: текст сообщения
        """
        bot.send_message(
            chat_id=Chats.get(main_chat_control_id=self.chat_id).admin_chat_id,
            text=text,
        )

    def is_user_admin(self) -> bool:
        """
        Проверяет, является ли пользователь администратором
        """
        if not self.message_author.is_admin:
            self.reply("Ты не можешь этого сделать!)")
            return False
        return True

    def is_reply_to_message_author_exists(self) -> bool:
        """
        Проверяет, использована ли команда ответом на сообщение
        """
        if not self.reply_to_message_author:
            self.reply("Эту команду надо использовать ответом на сообщение!")
            return False
        return True

    def refresh_forbidden_words(self) -> None:
        """Reloads forbidden words from database"""
        self.forbidden_word.refresh_forbidden_words()

    def reply(self, text: str) -> None:
        """
        Отвечает на сообщение
        :param text: текст сообщения
        """
        bot.reply_to(self.message, text)

    def start(self) -> None:
        """
        Отправляет сообщение по команде
        /start
        """
        self.send(self.msg.return_ready_message_text(sample=8))

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

    def extract_params(
            self, error_text: str, args_count: int | None = None
    ) -> list | None:
        """
        Извлекает из текста сообщения нужные параметры для команд;
        В случае ошибки отправляет соответствующее сообщение
        :param error_text: Текст сообщения, которое будет отправлено при ошибке
        :param args_count: Количество аргументов, которые мы хотим взять из строки.
        Если не передаем, то вернутся все
        """
        args_list = self.msg.message_text.split()[1:]

        if args_count is None:
            return args_list

        if len(args_list) < args_count:
            self.send(
                text=self.msg.return_ready_message_text(sample=16, value_1=error_text)
            )

            return None

        return args_list[: args_count + 1]

    @admin_guard
    def extract_and_add_forbidden_word(self) -> None:
        """
        Извлекает из команды новое слово и
        добавляет его к списку запрещенных слов
        """
        word = self.extract_params(
            error_text="Не указано запрещенное слово! (формат ввода данной команды: /add_forbidden_word "
                       "[слово, которое вы хотите добавить])",
            args_count=1,
        )

        if word:
            self.forbidden_word.add_forbidden_word(word=word[0])

    @admin_guard
    def extract_and_remove_forbidden_word(self) -> None:
        """
        Извлекает из команды новое слово и
        удаляет его из списка запрещенных слов
        """
        word = self.extract_params(
            error_text="К сожалению, не указано запрещенное слово! (формат ввода данной команды: "
                       "/delete_forbidden_word [слово, которое вы хотите удалить])",
            args_count=1,
        )

        if word is None:
            return

        try:
            self.forbidden_word.delete_forbidden_word(word=word)
        except KeyboardInterrupt:
            self.send(
                text=self.msg.return_ready_message_text(
                    sample=16,
                    value_1="К сожалению, введенного вами слово нет в базе данных! (формат ввода данной команды: "
                            "/delete_forbidden_word [слово, которое вы хотите удалить])",
                )
            )

    @creator_guard
    @reply_user_guard
    def extract_and_change_rating(self) -> None:
        """
         Меняет указанный рейтинг выбранного пользователя
         на указанное число
        :return:
        """
        rating_type, new_rating = self.extract_params(
            error_text="К сожалению, не указаны все необходимые параметры! (Формат ввода данной команды:"
                       "/rating_change [юзернейм] [тип рейтинга] [новый рейтинг])",
            args_count=2,
        )

        if rating_type is None or new_rating is None:
            return
        # Поменять, а то значения не сохраняются
        if rating_type.lower() == "спам":
            self.reply_to_message_author.db_user.ratings.spam_rating = new_rating
        elif rating_type.lower() == "токсик":
            self.reply_to_message_author.db_user.ratings.toxic_rating = new_rating
        else:
            self.send(
                self.msg.return_ready_message_text(
                    sample=16,
                    value_1="Указан несуществующий тип рейтинга!\nСпам - поменять спам рейтинг\nТоксик - поменять"
                            " рейтинг токсичности",
                )
            )
            return
        self.send(
            self.msg.return_ready_message_text(
                sample=12,
                value_1=self.reply_to_message_author.user_name,
                value_2=new_rating,
                value_3=self.message_author.user_name,
            )
        )

    @creator_guard
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

    @creator_guard
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

    @admin_guard
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

    @creator_guard
    @redirect_regular_chat_member_to_vote
    @reply_user_guard
    def admin_stat(self) -> None:
        """ "
        Назначает выбранного пользователя администратором
        """
        self.reply_to_message_author.make_user_admin(admin=True)
        self.send(
            text=self.msg.return_ready_message_text(
                sample=17, value_1=self.reply_to_message_author.username
            )
        )

    @creator_guard
    @redirect_regular_chat_member_to_vote
    @reply_user_guard
    def delete_admin_stat(self) -> None:
        """
        Снимает выбранного пользователя с должности администратора
        :return:
        """
        self.reply_to_message_author.make_user_admin(admin=False)
        self.send(
            text=self.msg.return_ready_message_text(
                sample=18, value_1=self.reply_to_message_author.username
            )
        )

    @admin_guard
    @redirect_regular_chat_member_to_vote
    def kick_user(self, kick=False):
        pass

    def reply_kick_user(self):
        pass

    @redirect_regular_chat_member_to_vote
    def add(self):
        pass

    def handle_message(self) -> bool:
        """
        Проверяет сообщение на наличие токсичности
        """
        pass
