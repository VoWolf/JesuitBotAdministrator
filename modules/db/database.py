"""В данном файле создаются таблицы в базе данных бота"""

from peewee import *

db = SqliteDatabase("bot_database.db")


class BaseModel(Model):
    """Базовая модель"""
    class Meta:
        """Параметры базы данных"""
        database = db


class ForbiddenWord(BaseModel):
    """
        Отвечает за таблицу с запрещенными словами

        Колонки:

        >> id - номер слова в таблице (автоматическое поле, int)

        >> word - само слово (текст, str)
    """
    class Meta:
        db_table = "ForbiddenWord"
    id = AutoField()
    word = CharField()


class TgUserRating(BaseModel):
    """
        Отвечает за таблицу с рейтингами пользователя

        Колонки:

        >> id - номер записи (автоматическое поле, int)

        >> spam_rating - Рейтинг пользователя относительно спама,
        по умолчанию ставить 1.00 (число, float)

        >> toxic_rating - Рейтинг пользователя относительно токсичности,
        по умолчанию ставить 1.00 (число, float)
    """
    class Meta:
        db_table = "TgUserRating"
    id = AutoField()
    spam_rating = FloatField()
    spam_messages_in_count = IntegerField()
    spam_messages_in_count_valid_until = DateTimeField()
    toxic_rating = FloatField()
    toxic_messages_in_count = IntegerField()
    toxic_messages_in_count_valid_until = DateTimeField()


class Chats(BaseModel):
    """
        Отвечает за таблицу со связками id чатов

        Колонки:

        >> id - номер записи (автоматическое поле, int)

        >> admin_chat_id - id чата с администрацией (число, int)

        >> main_chat_control_id - id основного чата с участниками (число, int)
    """
    class Meta:
        db_table = "Chats"
    id = AutoField()
    admin_chat_id = IntegerField()
    main_chat_control_id = IntegerField()
    token_for_tie = CharField(max_length=16)


class TgUser(BaseModel):
    """
        Отвечает за таблицу для пользователя Telegram

        Колонки:

        >> id - номер пользователя (автоматическое поле, int)

        >> telegram_id - id пользователя в Telegram (число, int)

        >> user_name - имя пользователя (текст, str)

        >> user_nik - ник пользователя (текст, str)

        >> user_rang - звание пользователя (текст, str)

        >> id_inTgUserRating - id записей о рейтинге данного пользователя в таблице
        TgUserRating (число, int)

        >> in_Chats_table_id - id записей о связке чатов данного пользователя в таблице
        Chats (число, int)
    """
    class Meta:
        db_table = "TgUser"
    id = AutoField()
    user_name = CharField(max_length=32)
    user_nik = CharField(max_length=128)
    user_rang = CharField(max_length=16)
    is_admin = BooleanField()
    telegram_id = IntegerField()
    in_TgUserRating_table = ForeignKeyField(TgUserRating)
    in_Chats_table = ForeignKeyField(Chats)


class AutoDeleteTime(BaseModel):
    class Meta:
        db_table = "AutoDeleteTime"
    id = AutoField()
    autodelete_time = IntegerField()


class BotsMessages(BaseModel):
    """
        id - номер записи (автоматическое поле, int)

        message_id - id сообщения бота (число, int)

        time_until - время до которого сообщение должно существовать в чате
        (время, datetime)
    """
    class Meta:
        db_table = "BotsMessages"
    id = AutoField()
    message_id = IntegerField()
    time_until = DateTimeField()


def create_tables():
    """
        Создает таблицы
    :return:
    """
    db.connect()
    with db:
        db.create_tables([ForbiddenWord, TgUserRating, Chats, TgUser, BotsMessages, AutoDeleteTime])
