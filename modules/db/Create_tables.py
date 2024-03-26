from modules.db.Tables.BaseModel import db
from modules.db.Tables.ChatTables import UserChat, StopWords, Rules, Chat
from modules.db.Tables.TgUserTables import UserStatistics, InactiveData, TgUser
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
                TgUser,  # Таблица с пользователем
                UserStatistics,  # Логирование сообщений пользователей
                InactiveData,  # Информация о периодах неактивности пользователя

                Chat,  # Таблица я чатом
                UserChat,  # Таблица для обеспечения связи многие ко многим между пользователями и чатом
                StopWords,  # Запрещенные в данном чате слова
                Rules,  # Правила текущего чата

                Place,  # Вся информация о месте проведения события
                Walks,  # Вся информация о запланированных прогулках
                UserWalks  # Таблица для обеспечения связи многие между прогулками и пользователями
            ]
        )
