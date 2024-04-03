from peewee import AutoField, IntegerField, BooleanField, CharField, ForeignKeyField, DateTimeField
from modules.db.Tables.BaseModel import BaseModel


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
        "statistics (dev)" - статистика данного пользователя

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
    time_message_sent_at = DateTimeField()
    user = ForeignKeyField(TgUser, backref="statistics")


class InactiveData(BaseModel):
    """
    New**
    """
    warned_to_go = BooleanField()
    warned_to_go_valid_until = DateTimeField()
    inactive_days_counter = IntegerField()
    free_days = CharField(max_length=7)
    user = ForeignKeyField(TgUser, backref="inactive")
