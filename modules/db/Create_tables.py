from modules.db.Tables.BaseModel import db
from modules.db.Tables.Chat import UserChat, AutoDeleteTime, BotsMessages, StopWords, Rules, Chat
from modules.db.Tables.TgUser import UserStatistics, InactiveDays, FreeWeekDays, TgUser
from modules.db.Tables.Walks import Place, Walks, UserWalks


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
                FreeWeekDays,

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
