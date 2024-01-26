from peewee import *

db = SqliteDatabase("database.db")


class BaseModel(Model):
    class Meta:
        database = db


class ForbiddenWord(BaseModel):
    id = AutoField()
    word = CharField()


def create_tables():
    db.connect()
    with db:
        db.create_tables([ForbiddenWord])
