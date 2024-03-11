"""Создает объект User с данными о пользователе"""
from time import time

import telebot.types

from modules.instances.bot_instance import bot
from modules.db.database import *


class User:
    """
    Класс пользователя.
    Вся информация о данном пользователе
    """

    def __init__(self, message: telebot.types.Message) -> None:
        try:
            self.db_user: TgUser = TgUser.get(telegram_id=message.from_user.id)
        except Exception:
            self.db_user: TgUser = TgUser.get_by_id(self.add())

        self.message: telebot.types.Message = message

        self.username: str = self.db_user.user_name
        self.usernik: str = self.db_user.user_nik
        self.userrang: str = self.db_user.user_rang
        self.is_admin: bool = self.db_user.is_admin
        self.user_id: int = self.db_user.telegram_id
        self.chat_id: int = self.db_user.chats.main_chat_id

    def add_user(self) -> TgUser | None:
        user = TgUser.create(
            user_name=self.message.from_user.username,
            user_nik=self.message.from_user.full_name
            user_rang="das",
            is_admin="self.message.from_user."
        )

    @staticmethod
    def add_stata_and_ratings() -> tuple | None:
        tables = (
            ActiveRating.create(
                active_in_chat_rating=0,
                active_in_chat_rating_lvl=1,
                coefficient=1,
                active_days_in_group=1
            ).id,
            UserStatistics.create(
                messages_per_day=1,
                messages_per_week=1,
                messages_per_all_time=1
            ).id,
            TgUserRating.create(
                main_rating=1.00,
                yesterday_rating=0.00
            ).id,
        )
        return tables

    def add_chat(self) -> Chat:
        """
        Добавляет запись в таблицу Chat или
        :return:
        """
        try:
            chat = Chat.get(chat_id=self.chat_id)
        except Exception:
            auto = AutoDeleteTime.create(
                autodelete_time=15
            ).id
            chat = Chat.create(
                chat_id=self.chat_id,
                chat_type=self.message.chat.type,
                autodelete_speed=AutoDeleteTime.get(auto)
            )

        return chat

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
