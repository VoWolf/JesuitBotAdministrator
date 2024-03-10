"""Создает объект User с данными о пользователе"""
from time import time

from modules.instances.bot_instance import bot
from modules.db.database import TgUser, TgUserRating, Chats, ActiveRating, UserStatistics


class User:
    """
    Класс пользователя.
    Вся информация о данном пользователе
    """
    def __init__(self, user_id: int) -> None:
        try:
            self.db_user = TgUser.get(telegram_id=user_id)
        except Exception:
            self.db_user = TgUser.get_by_id(self.add())

        self.username: str = self.db_user.user_name
        self.usernik: str = self.db_user.user_nik
        self.userrang: str = self.db_user.user_rang
        self.is_admin = self.db_user.is_admin
        self.user_id: int = self.db_user.telegram_id
        self.chat_id = self.db_user.chats.main_chat_id

    def add(self) -> None | TgUser:
        """
        Создает новые записи в таблицах
        TgUser и TgUserRating
        """
        try:
            in_chats = Chats.get(main_chat_control_id=self.chat_id)
        except IndexError:
            return

        in_ratings_table = TgUserRating.create(
            spam_rating=1.00,
            spam_messages_in_count=0,
            spam_messages_in_count_valid_until=0,
            toxic_rating=1.00,
            toxic_messages_in_count=0,
            toxic_messages_in_count_valid_until=0,
        ).id

        in_active_rating_table = ActiveRating.create(
            active_in_chat_rating=0,
            active_in_chat_rating_lvl=1,
            coefficient=1,
            active_days_in_group=1
        ).id

        in_statistics_table = UserStatistics.create(
            messages_per_day=1,
            messages_per_week=1,
            messages_per_all_time=1
        ).id

        new_chat_member = bot.get_chat_member(
            self.chat_id, self.user_id
        )
        return TgUser.create(
            user_name=new_chat_member.user.username,
            user_nik=new_chat_member.user.first_name,
            user_rang=""
            if new_chat_member.custom_title is None
            else new_chat_member.custom_title,
            is_admin=True
            if new_chat_member.custom_title is not None
               and "адм" in new_chat_member.custom_title
            else False,
            telegram_id=new_chat_member.user.id,
            in_TgUserRating_table=TgUserRating.get_by_id(in_ratings_table),
            in_Chats_table=in_chats,
            statistics=UserStatistics.get_by_id(in_statistics_table),
            active_rating=ActiveRating.get_by_id(in_active_rating_table)
        ).id

    def change_user_admin_stat(self, admin: bool = True) -> None:
        """
        Ставит пользователя на должность администратора
        или снимает его с этой должности
        :param admin: назначить пользователя администратором?
        """
        self.db_user.is_admin = admin
        TgUser.save(self.db_user)

    def ban_user(
            self, duration: int = 30,
            delete_messages_from_this_user: bool = False,
            kick: bool = False
    ) -> None:
        """
         Выгоняет данного пользователя из чата без возможности возврата (вносит в черный список чата) на определенное время
        :param duration: длительность бана
        :param delete_messages_from_this_user: удалить все сообщения от этого пользователя?
        :param kick: Удалить поьзователя из черного листа сразу после занесения (дать ему возможность вернуться сразу же)
        """
        bot.ban_chat_member(
            chat_id=self.chat_id,
            user_id=self.user_id,
            until_date=time() + duration * 90_000,
            revoke_messages=delete_messages_from_this_user,
        )
        if kick:
            bot.unban_chat_member(
                chat_id=self.chat_id, user_id=self.user_id, only_if_banned=True
            )
