import datetime

from modules.constants.users import ADMINS, USERS_PROTECTED_FROM_MUTE
from modules.db.database import TgUser, TgUserRating


class User:
    """
        Класс пользователя.
        Вся информация о данном пользователе
    """

    def __init__(self, username, user_id, chat_id):
        self.username: str = username
        self.user_id: int = user_id
        self.chat_id = chat_id
        self.is_admin = self.username in ADMINS
        self.can_be_muted = self.username not in ADMINS

        try:
            self.db_user = TgUser.get(TgUser.username == username)
        except Exception:
            TgUserRating.create(
                spam_rating=1.00,
                toxic_rating=1.00
            )
            TgUser.create(
                username=username,
                telegram_id=user_id,
                chat_id=chat_id,
                id_inTgUserRating=max(TgUserRating.id)
            )
            self.db_user = TgUser.get(TgUser.username == username)

        self.warnings_count = self.db_user.warnings_count
        self.warnings_valid_until = self.db_user.warnings_valid_until
        self.has_active_warnings = (
                self.db_user.warnings_count > 0
                and self.db_user.warnings_valid_until > datetime.datetime.now()
        )
