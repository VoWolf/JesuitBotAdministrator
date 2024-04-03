from peewee import *

# db = SqliteDatabase("bot_database.db")
db = SqliteDatabase("test_bot_database.db")


class BaseModel(Model):
    """Базовая модель"""

    class Meta:
        """Параметры базы данных"""

        database = db
