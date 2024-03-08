from datetime import datetime

from peewee import *

db = SqliteDatabase("database.db")


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)

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
    is_muted_until = DateTimeField()
    unmute_poll_id = IntegerField()


class Poll(BaseModel):
    id = AutoField()
    tg_poll_id = CharField()
    tg_message_id = CharField()
    question = CharField()
    is_closed = BooleanField()


class PollOption(BaseModel):
    id = AutoField()
    text = CharField()
    voter_count = IntegerField()
    poll = ForeignKeyField(Poll, backref="options")


def create_tables():
    db.connect()
    with db:
        db.create_tables([ForbiddenWord, Pilot, TgUser, Poll, PollOption])
