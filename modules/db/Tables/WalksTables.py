from peewee import CharField, ForeignKeyField, DateTimeField, IntegerField

from modules.db.Tables.TgUserTables import TgUser
from modules.db.Tables.ChatTables import Chat
from modules.db.Tables.BaseModel import BaseModel


class Walks(BaseModel):
    name = CharField(max_length=32)
    time_start = DateTimeField()
    time_end = DateTimeField()
    people_count = IntegerField()
    chat = ForeignKeyField(Chat, backref="walks")


class Place(BaseModel):
    city = CharField(max_length=16)
    metro_thread = CharField(max_length=16)
    metro_station = CharField(max_length=16)
    location = CharField(max_length=32)
    walk = ForeignKeyField(Walks, backref="place")


class UserWalks(BaseModel):
    walk = ForeignKeyField(Walks, backref="users")
    user = ForeignKeyField(TgUser, backref="walks")
