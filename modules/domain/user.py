import datetime

from modules.constants.users import ADMINS, USERS_PROTECTED_FROM_MUTE
from modules.db.database import TgUser


class User:
    """User class"""

    def __init__(self, username, user_id, chat_id):
        self.username: str = username
        self.user_id: int = user_id
        self.chat_id = chat_id
        self.is_admin = self.username in ADMINS
        self.can_be_muted = self.username not in USERS_PROTECTED_FROM_MUTE

        try:
            self.db_user = TgUser.get(TgUser.username == username)
        except Exception:
            TgUser.create(
                username=username,
                telegram_id=user_id,
                chat_id=chat_id,
                warnings_count=0,
                warnings_valid_until=datetime.datetime.now(),
            )
            self.db_user = TgUser.get(TgUser.username == username)

        self.warnings_count = self.db_user.warnings_count
        self.warnings_valid_until = self.db_user.warnings_valid_until
        self.has_active_warnings = (
                self.db_user.warnings_count > 0
                and self.db_user.warnings_valid_until > datetime.datetime.now()
        )
