"""Объявляет класс бота (Cerberus)"""

import time

from modules.db.database import ForbiddenWord, Chats
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

    def send(self, text):
        """
        Отправляет новое сообщение
        :param text:
        :return:
        """
        bot.send_message(self.chat_id, text)

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
                value_1=self.message_author.db_user.in_TgUserRating_table.spam_rating,
                value_2=self.message_author.db_user.in_TgUserRating_table.toxic_rating
            )
        )

    def extract_params(self, error_code: str, values_count: int, index_start: int, error_name):
        """
        Извлекает из текста сообщения нужные параметры для команд;
        В случае ошибки отправляет соответствующее сообщение
        :param index_start:
        :param error_code:
        :param values_count:
        :param error_name:
        :return str:
        """
        try:
            word = self.msg.message_text.split()[index_start:index_start + values_count].lower()
            t = self.msg.message_text.split()[index_start + values_count]
        except error_name:
            self.send(text=self.msg.return_ready_message_text(
                sample=16,
                value_1=error_code
            ))
            return
        return word

    def extract_and_add_forbidden_word(self):
        """
        Извлекает из команды новое слово и
        добавляет его к списку запрещенных слов
        :return:
        """
        word = self.extract_params(
            error_code="Не указано запрещенное слово! (формат ввода данной команды: /add_forbidden_word "
                        "[слово, которое вы хотите добавить])",
            values_count=1,
            index_start=1,
            error_name=IndexError
        )

        if word:
            self.forbidden_word.add_forbidden_word(
                word=word
            )

    def extract_and_remove_forbidden_word(self):
        """
        Извлекает из команды новое слово и
        удаляет его из списка запрещенных слов
        :return:
        """
        word = self.extract_params(
            error_code="К сожалению, не указано запрещенное слово! (формат ввода данной команды: "
                       "/delete_forbidden_word [слово, которое вы хотите удалить])",
            values_count=1,
            index_start=1,
            error_name=IndexError
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
            values_count=2,
            index_start=1,
            error_name=IndexError
        )

        if rating_type is None or new_rating is None:
            return

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

    def tie_chats(self):
        """
        Начинает связывание чатов
        :return: int token
        """
        Chats.create(
            main_chat_control_id=self.chat_id,
            admin_chat_id=0
        )
        self.send(
            self.msg.return_ready_message_text(
                sample=14,
                value_1=self.chat_id,
                value_2=self.chat_id
            )
        )

    def snap_chats(self):
        """
        Завершает связывание чатов
        :return:
        """
        tokn = self.extract_params(
            error_code="Вы не указали токен для связывания!",
            values_count=1,
            index_start=1,
            error_name=IndexError
        )

        if tokn is None:
            return

        try:
            chat = Chats.get(main_chat_control_id=0)
        except IndexError:
            self.send(
                self.msg.return_ready_message_text(
                    sample=16,
                    value_1="Вы указали несуществующий токен!"
                )
            )
            return
        chat.admin_chat_id = self.chat_id
        self.send(
            self.msg.return_ready_message_text(
                sample=15
            )
        )

    def change_autodelete_time(self):
        """
        Меняет скорость автоудаления сообщений бота
        :return:
        """
        new_time = self.extract_params(
            values_count=1,
            index_start=1,
            error_code="Ты не указал новое время автоудаления!",
            error_name=IndexError
        )
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

    @reply_user_guard
    def admin_stat(self):
        """"
        Назначает выбранного пользователя администратором
        """
        self.reply_to_message_author.db_user.is_admin = True
        self.send(
            text=self.msg.return_ready_message_text(
                sample=17,
                value_1=self.reply_to_message_author
            )
        )

    def delete_admin_stat(self):
        """
        Снимает выбранного пользователя с должности администратора
        :return:
        """
        self.reply_to_message_author.db_user.is_admin = False
        self.send(
            text=self.msg.return_ready_message_text(
                sample=18,
                value_1=self.reply_to_message_author
            )
        )

    def handle_message(self):
        """
        Проверяет сообщение на наличие токсичности
        :return:
        """
        if self.msg.toxic_check_message():
            self.message_author.down_rating(
                down_spam_rating=False,
                down_toxic_rating=True,
                down_value=0.05 * self.message_author.db_user.in_TgUserRating_table.toxic_messages_in_count
            )
            self.warning_in_chats(
                warning_level=self.message_author.check_rating(rating_type="toxic_rating"),
                rating_name="токсичности",
                rating_type="toxic_rating"
            )
        if self.msg.spam_check_message():
            self.message_author.down_rating(
                down_spam_rating=True,
                down_toxic_rating=False,
                down_value=0.01 * self.message_author.db_user.in_TgUserRating_table.spam_messages_in_count
            )
            self.warning_in_chats(
                warning_level=self.message_author.check_rating(rating_type="spam_rating"),
                rating_name="спамерстве",
                rating_type="toxic_rating"
            )

    def warning_in_chats(self, warning_level, rating_type, rating_name):
        """
        При низком рейтинге высылает предупреждения в чаты
        :param warning_level:
        :param rating_type:
        :param rating_name:
        :return:
        """
        # 3 - рейтинг выше -25 и ниже 0
        #
        # 4 - рейтинг ниже -25 и выше -50
        #
        # 5 - рейтинг ниже -50
        if warning_level in [1, 2]:
            return
        self.send(
            text=self.msg.return_ready_message_text(
                sample=0,
                value_1=rating_name,
                value_2=self.message_author.db_user.in_TgUserRating_table.rating_type
            )
        )
        sample = 0
        match warning_level:
            case 3:
                sample = 5
            case 4:
                sample = 6
            case 5:
                self.message_author.ban_user(
                    bot=bot,
                    duration=time.time() + 30_672_000,
                    delete_messages_from_this_user=False
                )
                self.send(
                    text=self.msg.return_ready_message_text(
                        sample=2,
                        value_1=self.message_author.user_name,
                        value_2="на год",
                        value_3="слишком низкий рейтинг (ниже -50)"
                    )
                )
        self.send_in_admin_chat(
            text=self.msg.return_ready_message_text(
                sample=sample,
                value_1=self.message_author.user_name,
                value_2=self.message_author.db_user.in_TgUserRating_table.rating_type
            )
        )

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
