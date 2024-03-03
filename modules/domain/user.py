"""Создает объект User с данными о пользователе"""
import modules.instances.bot_instance
import time
from modules.db.database import TgUser, TgUserRating, Chats


def admin_do_not_banned_guard(func):
    """
    Декоратор для проверки является ли
    пользователь администратором
    :param func:
    :return:
    """
    def inner(self):
        if self.is_admin():
            return
        func(self)

    return inner


class User:
    """
        Класс пользователя.
        Вся информация о данном пользователе
    """

    def __init__(self, user_id, chat_id):
        try:
            self.db_user = TgUser.get(telegram_id=user_id)
        except IndexError:
            self.add(user_id, chat_id)
            self.db_user = TgUser.get(telegram_id=user_id)

        self.username: str = self.db_user.user_name
        self.usernik: str = self.db_user.user_nik
        self.userrang: str = self.db_user.user_rang
        self.is_admin = self.db_user.is_admin
        self.user_id: int = self.db_user.telegram_id
        self.chat_id = self.db_user.in_Chats_table.main_chat_control_id

    @staticmethod
    def add(user_id, chat_id):
        """
        Создает новые записи в таблицах
        TgUser и TgUserRating
        :param user_id:
        :param chat_id:
        :return:
        """
        try:
            id_in_chats = Chats.get(main_chat_control_id=chat_id).id
        except IndexError:
            return
        new_id = TgUserRating.create(
            spam_rating=1.00,
            toxic_rating=1.00
        ).id
        new_chat_member = modules.instances.bot_instance.bot.get_chat_member(
            Chats.get(id=id_in_chats).main_chat_control_id, user_id
        )
        TgUser.create(
            user_name=new_chat_member.username,
            user_nik=new_chat_member.first_name,
            user_rang=new_chat_member.status,
            is_admin=False,
            telegram_id=user_id,
            in_TgUserRating_table=TgUserRating.get(id=new_id),
            in_Chats_table=Chats.get(id=id_in_chats)
        )

    @admin_do_not_banned_guard
    def kick_user(self, bot):
        """
        Выгоняет данного пользователя из чата с возможностью возврата
        :param bot:
        :return:
        """
        bot.ban_chat_member(
            chat_id=self.chat_id,
            user_id=self.user_id,
            until_date=time.time() + 30,
            revoke_messages=False
        )
        bot.unban_chat_member(
            chat_id=self.chat_id,
            user_id=self.user_id,
            only_if_banned=False
        )

    @admin_do_not_banned_guard
    def ban_user(self, bot, duration, delete_messages_from_this_user):
        """
         Выгоняет данного пользователя из чата
         без возможности возврата (вносит в черный список чата) на определенное время
        :param bot:
        :param duration:
        :param delete_messages_from_this_user:
        :return:
        """
        bot.ban_chat_member(
            chat_id=self.chat_id,
            user_id=self.user_id,
            until_date=duration,
            revoke_messages=delete_messages_from_this_user
        )

    def up_rating(self, up_value=0.01):
        """
        Повышает рейтинг заданного пользователя на
        введенное число
        :param up_value:
        :return:
        """
        self.db_user.in_TgUserRating_table.toxic_rating += up_value
        self.db_user.in_TgUserRating_table.spam_rating += up_value

    def down_rating(self, down_value, down_toxic_rating=False, down_spam_rating=False):
        """
        Понижает выбранный рейтинг данного пользователя
        на введенное число
        :param down_value:
        :param down_toxic_rating:
        :param down_spam_rating:
        :return:
        """
        if down_spam_rating:
            self.db_user.in_TgUserRating_table.spam_rating -= down_value
            self.db_user.in_TgUserRating_table.spam_messages_in_count += 1
            self.db_user.in_TgUserRating_table.spam_messages_in_count_valid_until = time.time() + 120
        if down_toxic_rating:
            self.db_user.in_TgUserRating_table.toxic_rating -= down_value
            self.db_user.in_TgUserRating_table.toxic_messages_in_count += 1
            self.db_user.in_TgUserRating_table.toxic_messages_in_count_valid_until = time.time() + 300

    def check_rating(self, rating_type):
        """
        Проверяет рейтинг данного пользователя

        1 - рейтинг выше 1.00

        2 - рейтинг выше 0 и ниже 1.00

        3 - рейтинг выше -25 и ниже 0

        4 - рейтинг ниже -25 и выше -50

        5 - рейтинг ниже -50
        :param rating_type:
        :return int:
        """
        if rating_type is None:
            return
        if self.db_user.in_TgUserRating_table.rating_type >= 1.00:
            return 1
        if 0.00 <= self.db_user.in_TgUserRating_table.rating_type < 1.00:
            return 2
        if -25 <= self.db_user.in_TgUserRating_table.rating_type < 0.00:
            return 3
        if -50 <= self.db_user.in_TgUserRating_table.rating_type < -25.00:
            return 4
        return 5
