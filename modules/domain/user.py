"""Создает объект User с данными о пользователе"""
import time

import modules.instances.bot_instance
from modules.db.database import TgUser, TgUserRating, Chats


def admin_do_not_banned_guard(func):
    """
    Декоратор для проверки является ли
    пользователь администратором
    :param func:
    :return:
    """

    def inner(self, bot, duration, delete_messages_from_this_user, kick):
        if not self.is_admin_or_no(bot):
            return
        func(self, bot, duration, delete_messages_from_this_user, kick)

    return inner


class User:
    """
    Класс пользователя.
    Вся информация о данном пользователе
    """

    def __init__(self, user_id, chat_id):
        try:
            self.db_user = TgUser.get(telegram_id=user_id)
        except Exception:
            self.add(user_id, chat_id)
            print(user_id, chat_id)
            self.db_user = TgUser.get(telegram_id=user_id)

        self.username: str = self.db_user.user_name
        self.usernik: str = self.db_user.user_nik
        self.userrang: str = self.db_user.user_rang
        self.is_admin = self.db_user.is_admin
        self.user_id: int = self.db_user.telegram_id
        self.chat_id = self.db_user.chats.main_chat_id

    def make_user_admin(self, admin: bool = True) -> None:
        """
        Ставит пользователя на должность администратора
        или снимает его с этой должности
        :param admin: назначить пользователя администратором?
        """
        self.db_user.is_admin = admin
        TgUser.save(self.db_user)

    @staticmethod
    def add(user_id: int, chat_id: int) -> None:
        """
        Создает новые записи в таблицах
        TgUser и TgUserRating
        :param user_id: ID пользователя
        :param chat_id: ID чата
        """
        try:
            id_in_chats = Chats.get(main_chat_control_id=chat_id)
        except IndexError:
            modules.domain.cerberus.Cerberus.send(
                text="Для автоматической регистрации данного пользователя "
                     "вам необходимо связать чаты! Инсрукция доступна по команде "
                     "/tie_chats_instruction"
            )
            return
        new_id = TgUserRating.create(
            spam_rating=1.00,
            spam_messages_in_count=0,
            spam_messages_in_count_valid_until=0,
            toxic_rating=1.00,
            toxic_messages_in_count=0,
            toxic_messages_in_count_valid_until=0,
        ).id
        new_record = TgUserRating.get_by_id(new_id)
        new_chat_member = modules.instances.bot_instance.bot.get_chat_member(
            chat_id, user_id
        )
        TgUser.create(
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
            in_TgUserRating_table=new_record,
            in_Chats_table=id_in_chats,
        )

    def is_admin_or_no(self, bot) -> bool:
        """
        Проверяет, является ли пользователь администратором.
        В случае, если пользователь не админ, отправляется сообщение с соответствующим
        оповещением
        :param bot:
        """
        if self.is_admin:
            return True
        bot.send_message(
            chat_id=self.chat_id, text="Забанить администратора может только создатель!"
        )
        return False

    # {'user': {'id': 1044385209, 'is_bot': False, 'first_name': '˚₊· ͟͟͞͞➳❥𝕸𝕰𝕺𝖂~·˚ ༘₊· ͟͟͞͞꒰➳', 'username': 'LastUwUlf',
    # 'last_name': None, 'language_code': 'ru', 'can_join_groups': None, 'can_read_all_group_messages': None,
    # 'supports_inline_queries': None, 'is_premium': None, 'added_to_attachment_menu': None}, 'status': 'creator',
    # 'custom_title': None, 'is_anonymous': False, 'can_be_edited': None, 'can_post_messages': None,
    # 'can_edit_messages': None, 'can_delete_messages': None, 'can_restrict_members': None, 'can_promote_members': None,
    # 'can_change_info': None, 'can_invite_users': None, 'can_pin_messages': None, 'is_member': None,
    # 'can_send_messages': None, 'can_send_polls': None, 'can_send_other_messages': None, 'can_add_web_page_previews':
    # None, 'can_manage_chat': None, 'can_manage_video_chats': None, 'until_date': None, 'can_manage_topics': None,
    # 'can_send_audios': None, 'can_send_documents': None, 'can_send_photos': None, 'can_send_videos': None,
    # 'can_send_video_notes': None, 'can_send_voice_notes': None, 'can_post_stories': None, 'can_edit_stories':
    # None, 'can_delete_stories': None}

    @admin_do_not_banned_guard
    def ban_user(
            self, bot, duration: int = 30, delete_messages_from_this_user: bool = False, kick: bool = False
    ) -> None:
        """
         Выгоняет данного пользователя из чата
         без возможности возврата (вносит в черный список чата) на определенное время
        :param bot: объект класса telebot
        :param duration: длительность бана
        :param delete_messages_from_this_user: удалить все сообщения от этого пользователя?
        :param kick: Удалить поьзователя из черного листа сразу после занесения (дать ему возможность вернуться
        сразу же)
        """
        bot.ban_chat_member(
            chat_id=self.chat_id,
            user_id=self.user_id,
            until_date=duration * 90_000,
            revoke_messages=delete_messages_from_this_user,
        )
        if kick:
            bot.unban_chat_member(
                chat_id=self.chat_id, user_id=self.user_id, only_if_banned=True
            )

    def up_rating(self, up_value: float = 0.01) -> None:
        """
        Повышает рейтинг заданного пользователя на
        введенное число
        :param up_value: число, на которое будет повышен рейтинг
        """
        self.db_user.ratings.toxic_rating += up_value
        self.db_user.ratings.spam_rating += up_value

    def down_rating(self, down_value: float, down_toxic_rating: bool = False, down_spam_rating: bool = False) -> None:
        """
        Понижает выбранный рейтинг данного пользователя
        на введенное число
        :param down_value: значение, на которое будет понижен рейтинг
        :param down_toxic_rating: понизить рейтинг токсичности?
        :param down_spam_rating: понизить спам рейтинг?
        """
        if down_spam_rating:
            self.db_user.ratings.spam_rating -= down_value
            self.db_user.ratings.spam_messages_in_count += 1
            self.db_user.ratings.spam_messages_in_count_valid_until = time.time() + 120
        if down_toxic_rating:
            self.db_user.ratings.toxic_rating -= down_value
            self.db_user.ratings.toxic_messages_in_count += 1
            self.db_user.ratings.toxic_messages_in_count_valid_until = time.time() + 300

    def check_rating(self) -> int:
        pass
