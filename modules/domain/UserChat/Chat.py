from modules.db.database import Chat, db


class DbChat:
    def __init__(self, db_chat: Chat) -> None:
        self.users = db.execute(db_chat.users).fetchall(),
        self.autodelete_time = db.execute(db_chat.autodelete_time).fetchall(),
        self.bot_messages = db.execute(db_chat.bot_messages).fetchall(),
        self.stop_words = db.execute(db_chat.stop_words).fetchall()


class ChatInfo:
    def __init__(
            self,
            db_chat: Chat
    ) -> None:
        self.chat_id = db_chat.chat_id,
        self.type = db_chat.chat_type,
        self.db_chat = DbChat(db_chat)

    @property
    def full_info(self):
        return {
            "id": self.chat_id,
            "type": self.type,
            "users": self.db_chat.users,
            "auto_time": self.db_chat.autodelete_time,
            "fws": self.db_chat.stop_words,
            "bot_msgs": self.db_chat.bot_messages
        }
