from peewee import CharField, ForeignKeyField, DateTimeField, IntegerField

from modules.db.Tables.TgUser import TgUser
from modules.db.Tables.Chat import Chat
from modules.db.Tables.BaseModel import BaseModel


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
