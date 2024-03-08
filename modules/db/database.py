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

    Свойства:

    id (int)
        ID запрещенного слова

    word (str)
        Слово
    """

    id = AutoField()
    word = CharField()


class TgUserRating(BaseModel):
    """
    Отвечает за таблицу с рейтингами пользователя

    Свойства:

    id (int)
        Номер записи (автоматическое поле, int)

    spam_rating (float)
        Рейтинг пользователя относительно спама,
        по умолчанию ставить 1.00 (число, float)

    toxic_rating (float)
        Рейтинг пользователя относительно токсичности,
        по умолчанию ставить 1.00 (число, float)
    """

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

    Свойства:

    id (int)
        ID чата

    admin_chat_id (int)
        ID чата с администрацией

    main_chat_id (int)
        ID основного чата с участниками
    """

    id = AutoField()
    admin_chat_id = IntegerField()
    main_chat_id = IntegerField()
    token_for_tie = CharField(max_length=16)


class TgUser(BaseModel):
    """
    Отвечает за таблицу для пользователя Telegram

    Свойства:

    id (int)
        ID пользователя

    telegram_id (int)
        ID пользователя в Telegram

    user_name (str)
        Имя пользователя

    user_nik (str)
        Ник пользователя

    user_rang (str)
        Звание пользователя

    ratings (TgUserRating)
        Список рейтингов пользователя

    chats (Chats)
        Список чатов пользователя
    """

    id = AutoField()
    user_name = CharField(max_length=32)
    user_nik = CharField(max_length=128)
    user_rang = CharField(max_length=16)
    is_admin = BooleanField()
    telegram_id = IntegerField()
    ratings = ForeignKeyField(TgUserRating, backref="user")


class UserChats(BaseModel):
    user = ForeignKeyField(TgUser)
    chat = ForeignKeyField(Chats)


class AutoDeleteTime(BaseModel):
    id = AutoField()
    autodelete_time = IntegerField()


class BotsMessages(BaseModel):
    """
    id (int)
        ID записи

    message_id (int)
        ID сообщения

    time_until (timestamp)
        Время до которого сообщение должно существовать в чате
    """

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
        db.create_tables(
            [
                ForbiddenWord,
                TgUserRating,
                Chats,
                TgUser,
                UserChats,
                BotsMessages,
                AutoDeleteTime,
            ]
        )
