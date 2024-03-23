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

        "inactive" - количество идущих подряд дней когда кол-во сообщений за день было равно 0

        "free_days" - Дни, в которые пользователь может гулять (Отмечаются лс)
    """
    id = AutoField()
    telegram_id = IntegerField()
    user_nik = CharField(max_length=128)
    user_name = CharField(max_length=32)
    is_administrator_in_bot = BooleanField()


class UserStatistics(BaseModel):
    """
    Активность пользователя

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
    messages_per_day = IntegerField()
    messages_per_week = IntegerField()
    messages_per_all_time = IntegerField()
    user = ForeignKeyField(TgUser, backref="statistics")


class InactiveDays(BaseModel):
    """
    New**
    """
    warned_to_go: BooleanField()
    inactive_days_counter = IntegerField()
    user = ForeignKeyField(TgUser, backref="inactive")


class FreeWeekDays(BaseModel):
    """
    New**
    """
    monday = BooleanField()
    tuesday = BooleanField()
    wednesday = BooleanField()
    Thursday = BooleanField()
    Friday = BooleanField()
    Saturday = BooleanField()
    Sunday = BooleanField()
    user = ForeignKeyField(TgUser, backref="free_days")


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

        "rules" - Правила чата
    """
    id = AutoField()
    chat_id = IntegerField()
    chat_type = CharField()


class UserChat(BaseModel):
    """
    Обеспечение связи 'многие ко многим' между таблицами TgUser и Chat

    user (ForeignKey)
        Ссылка на таблицу с пользователем
    chat (ForeignKey)
        Ссылка на таблицу с чатом, в котором состоит пользователь
    """
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
    autodelete_time = IntegerField()
    chat = ForeignKeyField(Chat, backref="autodelete_time")


class BotsMessages(BaseModel):
    """
    Сохраняет все сообщения, отправленные ботом

    message_id (int)
        ID сообщения
    time_until (timestamp)
        Время до которого сообщение должно существовать в чате
    chat (ForeignKey)
        Ссылка на чат, в котором это сообщение было отправлено
    """
    message_id = IntegerField()
    valid_until = DateTimeField()
    chat = ForeignKeyField(Chat, backref="bot_messages")


class StopWords(BaseModel):
    """
    Запрещенные слова в чате (бот будет автоматически их чистить)

    word (str)
        Само слово
    chat (ForeignKey)
        Ссылка на чат, в котором действует данное стоп-слово
    """
    word = CharField(max_length=64)
    chat = ForeignKeyField(Chat, backref="stop_words")


class Rules(BaseModel):
    rule = CharField(max_length=4096)
    chat = ForeignKeyField(Chat, backref="rules")


class Place(BaseModel):
    city = CharField(max_length=16)
    metro_thread = CharField(max_length=16)
    metro_station = CharField(max_length=16)
    location = CharField(max_length=32)


class Walks(BaseModel):
    name = CharField(max_length=32)
    place = ForeignKeyField(Place, backref="walk")
    time_start = DateTimeField()
    time_end = DateTimeField()
    how_many_people = IntegerField()
    chat = ForeignKeyField(Chat, backref="walks")


class UserWalks(BaseModel):
    walk = ForeignKeyField(Walks, backref="users")
    user = ForeignKeyField(TgUser, backref="walks")


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
