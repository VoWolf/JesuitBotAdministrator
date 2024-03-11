"""В данном файле создаются таблицы в базе данных бота"""
from peewee import *

db = SqliteDatabase("bot_database.db")


class BaseModel(Model):
    """Базовая модель"""

    class Meta:
        """Параметры базы данных"""

        database = db


class TgUserRating(BaseModel):
    """
    Отвечает за таблицу с рейтингами пользователя

    Свойства:

    id (int)
        Номер записи (автоматическое поле, int)

    main_rating (float)
        Сегодняшний рейтинг пользователя, изменяется с каждым отправленным сообщением,
        по умолчанию ставить 1.00 (число, float)

    yesterday_rating (float)
        Вчерашний рейтинг пользователя, используется для подсчета изменений рейтинга
        по умолчанию ставить 0.00 (число, float)
    """
    id = AutoField()
    main_rating = IntegerField()
    yesterday_rating = IntegerField()


class ActiveRating(BaseModel):
    """
    Отвечает за таблицу с рейтингом активности

    Свойства:

    id (int)
        Номер записи (автоматическое поле, int)

    active_in_chat_rating (int)
        Рейтинг активности в чате, количество очков, накопленных пользователем

    active_in_chat_rating_lvl (int)
        Уровень пользователя. 1 уровень = +1 дню ко времени, через которое пользователя автоматически
        кикнет из чата

    coefficient (int)
        Коэффициент, на который умножается изменение двух средних арифметических 2-х остальных рейтингов.
        Формула: a = ([разница между вчерашним и сегодняшним средним арифметическим спам рейтинга и рейтинга
        токсичности]*[этот коэффициент]), где a - значение, которое прибавится к active_in_chat_rating

    active_days_in_group (int)
        Сколько дней участник провел в группе (считаются только те дни, когда участник отправил хотя бы 1 сообщение)
    """
    id = AutoField()
    active_in_chat_rating = IntegerField()
    active_in_chat_rating_lvl = IntegerField()
    coefficient = IntegerField()
    active_days_in_group = IntegerField()


class UserStatistics(BaseModel):
    """
    Отвечает за таблицу с активностью пользователя

    Свойства:

    id (int)
        Номер записи (автоматическое поле, int)

    messages_per_day (int)
        Количество сообщений, отправленных пользователем за промежуток времени от 00:00 до 23:59

    messages_per_week (int)
        Количество сообщений, отправленных пользователем за промежуток времени от 00:00 (понедельник) до 23:59
        (воскресенье)

    messages_per_all_time (int)
        Количество сообщений, отправленных пользователем за все время
    """
    id = AutoField()
    messages_per_day = IntegerField()
    messages_per_week = IntegerField()
    messages_per_all_time = IntegerField()


class AutoDeleteTime(BaseModel):
    id = AutoField()
    autodelete_time = IntegerField()


class Chat(BaseModel):
    """
    pass
    """
    id = AutoField()
    chat_id = IntegerField()
    chat_type = CharField()
    autodelete_speed = ForeignKeyField(AutoDeleteTime, backref="chat")


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
    statistics = ForeignKeyField(UserStatistics, backref="user")
    active_rating = ForeignKeyField(ActiveRating, backref="user")


class UserChat(BaseModel):
    """
    pass
    """
    id = AutoField()
    user = ForeignKeyField(TgUser, backref="chats")
    chat = ForeignKeyField(Chat, backref="users")


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
                TgUserRating,
                ActiveRating,
                UserStatistics,
                Chat,
                TgUser,
                UserChat,
                AutoDeleteTime,
                BotsMessages
            ]
        )
