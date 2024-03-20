"""Таблицы в базе данных бота"""
from peewee import *

db = SqliteDatabase("bot_database.db")


class BaseModel(Model):
    """Базовая модель"""

    class Meta:
        """Параметры базы данных"""

        database = db


class TgUser(BaseModel):
    """
    Информация о пользователе

    id (int)
        ID записи
    telegram_id (int)
        ID пользователя в Telegram
    user_nik (str)
        Имя пользователя внутри бота
    user_name (str)
        Имя пользователя в Telegram образца @ExampleUser
    is_administrator_in_bot (bool)
        Является ли пользователь администратором внутри бота (НЕ ЧАТА!!!)

    Ссылки на другие таблицы:
        "statistics" - статистика данного пользователя

        "chats" - чаты, в которых состоит пользователь
    """
    id = AutoField()
    telegram_id = IntegerField()
    user_nik = CharField(max_length=128)
    user_name = CharField(max_length=32)
    is_administrator_in_bot = BooleanField()


class UserStatistics(BaseModel):
    """
    Активность пользователя

    id (int)
        Номер записи (автоматическое поле, int)
    messages_per_day (int)
        Количество сообщений, отправленных пользователем за промежуток времени от 00:00 до 23:59
    messages_per_week (int)
        Количество сообщений, отправленных пользователем за промежуток времени от 00:00 (понедельник) до 23:59
        (воскресенье)
    messages_per_all_time (int)
        Количество сообщений, отправленных пользователем за все время
    user (ForeignKey)
        Ссылка на запись о пользователе, к которому относится статистика
    """
    id = AutoField()
    messages_per_day = IntegerField()
    messages_per_week = IntegerField()
    messages_per_all_time = IntegerField()
    user = ForeignKeyField(TgUser, backref="statistics")


class Chat(BaseModel):
    """
    Информация о чатах

    id (int)
        ID записи
    chat_id (int)
        ID чата
    chat_type (str)
        Тип чата (Бывают: private - приватный или supergroup - супергруппа. Также бывают и другие,
        но здесь они не обрабатываются)

    Ссылки на другие таблицы:
        "users" - пользователи, которые состоят в чате

        "autodelete_time" - время автоматического удаления сообщений в данном чате

        "bot_messages" - сообщения бота в этом чате

        "stop_words" - стоп-слова (запрещенные слова) в данном чате
    """
    id = AutoField()
    chat_id = IntegerField()
    chat_type = CharField()


class UserChat(BaseModel):
    """
    Обеспечение связи 'многие ко многим' между таблицами TgUser и Chat

    id (int)
        ID записи
    user (ForeignKey)
        Ссылка на таблицу с пользователем
    chat (ForeignKey)
        Ссылка на таблицу с чатом, в котором состоит пользователь
    """
    id = AutoField()
    user = ForeignKeyField(TgUser, backref="chats")
    chat = ForeignKeyField(Chat, backref="users")


class AutoDeleteTime(BaseModel):
    """
    Хранит время, через которое бот автоматически будет удалять свои сообщения

    autodelete_time (int)
        Время автоудаления (секунды)
    chat (ForeignKey)
        Ссылка на чат, в нем действует заданное время
    """
    id = AutoField()
    autodelete_time = IntegerField()
    chat = ForeignKeyField(Chat, backref="autodelete_time")


class BotsMessages(BaseModel):
    """
    Сохраняет все сообщения, отправленные ботом

    id (int)
        ID записи
    message_id (int)
        ID сообщения
    time_until (timestamp)
        Время до которого сообщение должно существовать в чате
    chat (ForeignKey)
        Ссылка на чат, в котором это сообщение было отправлено
    """
    id = AutoField()
    message_id = IntegerField()
    valid_until = DateTimeField()
    chat = ForeignKeyField(Chat, backref="bot_messages")


class StopWords(BaseModel):
    """
    Запрещенные слова в чате (бот будет автоматически их чистить)

    id (int)
        ID записи
    word (str)
        Само слово
    chat (ForeignKey)
        Ссылка на чат, в котором действует данное стоп-слово
    """
    id = IntegerField()
    word = CharField(max_length=64)
    chat = ForeignKeyField(Chat, backref="stop_words")


def create_tables():
    """
        Создает таблицы
    :return:
    """
    db.connect()
    with db:
        db.create_tables(
            [
                TgUser,
                UserStatistics,
                Chat,
                UserChat,
                AutoDeleteTime,
                BotsMessages,
                StopWords
            ]
        )
