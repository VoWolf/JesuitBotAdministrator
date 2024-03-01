"""В данном файле создаются таблицы в базе данных бота"""

from peewee import *

db = SqliteDatabase("database.db")


class BaseModel(Model):
    class Meta:
        database = db


class ForbiddenWord(BaseModel):
    """
        Отвечает за таблицу с запрещенными словами

        Колонки:

        >> id - номер слова в таблице (автоматическое поле, int)

        >> word - само слово (текст, str)
    """
    id = AutoField()
    word = CharField()


class TgUser(BaseModel):
    """
        Отвечает за таблицу для пользователя Telegram

        Колонки:

        >> id - номер пользователя (автоматическое поле, int)

        >> telegram_id - id пользователя в Telegram (число, int)

        >> chat_id - id чата с пользователем (число, int)

        >> user_name - имя пользователя (текст, str)

        >> user_nik - ник пользователя (текст, str)

        >> user_rang - звание пользователя (текст, str)

        >> id_inTgUserRating - id записей о рейтинге данного пользователя в таблице
        TgUserRating (число, int)

        >> in_Chats_table_id - id записей о связке чатов данного пользователя в таблице
        Chats (число, int)
    """
    id = AutoField()
    telegram_id = IntegerField()
    chat_id = CharField()
    user_name = CharField()
    user_nik = CharField()
    user_rang = CharField()
    in_TgUserRating_table_id = IntegerField()
    in_Chats_table_id = IntegerField()


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
    id = AutoField()
    spam_rating = FloatField()
    toxic_rating = FloatField()


class Chats(BaseModel):
    """
        Отвечает за таблицу со связками id чатов

        Колонки:

        >> id - номер записи (автоматическое поле, int)

        >> admin_chat_id - id чата с администрацией (число, int)

        >> main_chat_control_id - id основного чата с участниками (число, int)
    """
    id = AutoField()
    admin_chat_id = IntegerField()
    main_chat_control_id = IntegerField()


class AdminTags(BaseModel):
    """
        id - номер записи (автоматическое поле, int)
        user_names_list - Строка с именами пользователей
        для отметки (Разделитель: '::')
    """
    id = AutoField()
    user_names_list = CharField()


class BorsMessages(BaseModel):
    """
        id - номер записи (автоматическое поле, int)
        message_id - id сообщения бота (число, int)
        time_until - время до которого сообщение должно существовать в чате
        (время, datetime)
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
        db.create_tables([ForbiddenWord, TgUser, TgUserRating, Chats])
