"""Создает объект User с данными о пользователе"""
import modules.instances.bot_instance
import time
from modules.db.database import TgUser, TgUserRating, Chats


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

    def mute(self, bot, mute_duration):
        """
        Мьютит пользователя
        :param bot:
        :param mute_duration:
        :return:
        """
        self.down_chat_member_rang(bot)
        bot.restrict_chat_member(
            self.chat_id,
            self.user_id,
            until_date=time.time() + mute_duration * 60,
        )

    def unmute(self, bot):
        """
        Размьючивает пользователя
        :param bot:
        :return:
        """
        bot.restrict_chat_member(
            self.chat_id,
            self.user_id,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
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
        if down_toxic_rating:
            self.db_user.in_TgUserRating_table.toxic_rating -= down_value

    def down_chat_member_rang(self, bot):
        """
        Понижает указанного пользователя
        :param bot:
        :return:
        """
        bot.promote_chat_member(
            chat_id=self.chat_id,
            user_id=self.user_id
        )

    def up_chat_member_rang(self, bot):
        """
        Повышает указанного пользователя
        :param bot:
        :return:
        """
        # Здесь бот повышает участника, ДОБАВИТЬ
        bot.set_chat_administrator_custom_title(
            chat_id=self.chat_id,
            user_id=self.user_id,
            custom_title=self.userrang
        )

# promote_chat_member
# ПАРАМЕТРЫ:
# chat_id (int or str) – Уникальный id чата или username канала (в формате @channelusername)
#
# user_id (int) – Уникальный id сделавшего запрос пользователя
#
# can_change_info (bool) – Передайте True, если администратор может менять название чата, аватарку и другие настройки
#
# can_post_messages (bool) – Передайте True, если администратор может создавать посты в канале, только для каналов
#
# can_edit_messages (bool) – Передайте True, если администратор может изменять сообщения других пользователей, только для каналов
#
# can_delete_messages (bool) – Передайте True, если администратор может удалять сообщения других пользователей
#
# can_invite_users (bool) – Передайте True, если администратор может приглашать новых пользователей в чат
#
# can_restrict_members (bool) – Передайте True, если администратор может ограничивать, банить или разбанивать участников чата
#
# can_pin_messages (bool) – Передайте True, если администратор может закреплять сообщения, только для супергрупп
#
# can_promote_members (bool) – Передайте True, если администратор может добавлять новых администраторов с подмножеством его собственных прав администратора или понижать администраторов, которых он повысил, напрямую или косвенно (администраторами, которых он назначил)
#
# is_anonymous (bool) – Передайте True, если присутствие администратора в чате скрыто
#
# can_manage_chat (bool) – Передайте True, если администратор имеет доступ к логу событий чата, статистике чата, статистике сообщений в каналах, видеть участников канала, видеть анонимных администраторов в супергруппах и игнорировать медленный режим. Подразумевается любым другим правом администратора
#
# can_manage_video_chats (bool) – Передайте True, если администратор может управлять голосовыми чатами. На текущий момент, боты могут использовать это право администратора только для передачи другим администраторам.
#
# can_manage_voice_chats (bool) – Устарело, используйте can_manage_video_chats.
#
# can_manage_topics (bool) – Передайте True, если пользователю разрешено создавать, переименовывать, закрывать, и возобновлять топики, только для супергрупп
#
# can_post_stories (bool) – Pass True if the administrator can create the channel’s stories
#
# can_edit_stories (bool) – Pass True if the administrator can edit the channel’s stories
#
# can_delete_stories (bool) – Pass True if the administrator can delete the channel’s stories
#
# РЕЗУЛЬТАТ:
# True в случае успеха.
#
# ТИП РЕЗУЛЬТАТА:
# bool

# set_chat_administrator_custom_title
# chat_id (int or str) – Уникальный id чата или username супергруппы (в формате @supergroupusername)
#
# user_id (int) – Уникальный id сделавшего запрос пользователя
#
# custom_title (str) – Новое кастомное звание администратора; 0-16 символов, эмодзи не разрешены
