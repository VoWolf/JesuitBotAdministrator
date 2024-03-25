from modules.db.Tables.BaseModel import db
from modules.db.Tables.ChatTables import Chat


class DbChat:
    def __init__(self, db_chat: Chat) -> None:
        self.db_chat = db_chat
        self.users = db.execute(db_chat.users).fetchall(),
        self.autodelete_time = db.execute(db_chat.autodelete_time).fetchone()[0],
        self.bot_messages = [msg[:-1] for msg in db.execute(db_chat.bot_messages).fetchall()],
        self.stop_words = [word[0] for word in db.execute(db_chat.stop_words).fetchall()]
        self.walks = [walk[:-1] for walk in db.execute(db_chat.walks).fetchall()]


class ChatInfo(DbChat):
    def __init__(self, db_chat: Chat) -> None:
        super().__init__(db_chat)
        self.chat_id = db_chat.chat_id,
        self.type = db_chat.chat_type,
