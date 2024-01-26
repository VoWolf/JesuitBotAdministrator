from peewee import *

db = SqliteDatabase("database.db")


class BaseModel(Model):
    class Meta:
        database = db


class ForbiddenWord(BaseModel):
    id = AutoField()
    word = CharField()


class Pilot(BaseModel):
    id = AutoField()
    name = CharField()
    is_on = BooleanField()
    mute_time = IntegerField()
    mute_break_time = IntegerField()


class TgUser(BaseModel):
    id = AutoField()
    telegram_id = IntegerField()
    chat_id = CharField()
    username = CharField()
    warnings_count = IntegerField()
    warnings_valid_until = DateTimeField()


def create_tables():
    db.connect()
    with db:
        db.create_tables([ForbiddenWord, Pilot, TgUser])
