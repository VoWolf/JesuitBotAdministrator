from modules.db.Tables.BaseModel import db
from modules.db.Tables.ChatTables import Chat


class DbChat:
    def __init__(self, db_chat: Chat) -> None:
        self.db_chat = db_chat
        self.users = [usr.user for usr in self.db_chat.users]
        self.stop_words = [word.word for word in db_chat.stop_words]
        print(db.execute(db_chat.walks).fetchall())
        self.walks = [walk for walk in db_chat.walks]
        self.rules = [rule for rule in db_chat.rules]
        print(db_chat.chat_id)
        print(self.users, self.stop_words, self.walks, self.rules)


class ChatInfo(DbChat):
    def __init__(self, db_chat: Chat) -> None:
        super().__init__(db_chat)
        self.chat_id = db_chat.chat_id
        self.type = db_chat.chat_type
