from modules.db.Tables.BaseModel import db
from modules.db.Tables.ChatTables import Chat


class DbChat:
    def __init__(self, db_chat: Chat) -> None:
        self.db_chat = db_chat
        self.users = db.execute(db_chat.users).fetchall(),
        self.autodelete_time = db.execute(db_chat.autodelete_time).fetchone()[0],
        self.stop_words = [word for word in db_chat.stop_words]
        self.walks = [walk[:-1] for walk in db_chat.walks]


class ChatInfo(DbChat):
    def __init__(self, db_chat: Chat) -> None:
        super().__init__(db_chat)
        self.chat_id = db_chat.chat_id,
        self.type = db_chat.chat_type,
