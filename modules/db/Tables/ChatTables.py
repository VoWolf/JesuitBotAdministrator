from peewee import AutoField, IntegerField, CharField, ForeignKeyField, DateTimeField

from modules.db.Tables.TgUserTables import TgUser
from modules.db.Tables.BaseModel import BaseModel


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
