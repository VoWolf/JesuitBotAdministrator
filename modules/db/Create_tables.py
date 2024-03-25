from modules.db.Tables.BaseModel import db
from modules.db.Tables.ChatTables import UserChat, AutoDeleteTime, BotsMessages, StopWords, Rules, Chat
from modules.db.Tables.TgUserTables import UserStatistics, InactiveDays, TgUser
from modules.db.Tables.WalksTables import Place, Walks, UserWalks


def create_tables():
    """
        Создает таблицы
    :return:
    """
    db.connect()
    with db:
        db.create_tables(
            [
                TgUser,
                UserStatistics,
                InactiveDays,

                Chat,
                UserChat,
                AutoDeleteTime,
                BotsMessages,
                StopWords,
                Rules,

                Place,
                Walks,
                UserWalks
            ]
        )


create_tables()
