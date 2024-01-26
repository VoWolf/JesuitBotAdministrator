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

        user = TgUser.get(User.username == username)

        if user:
            self.db_user = user
            self.warnings_count = user.warnings_count
            self.warnings_valid_until = user.warnings_valid_until
            self.has_active_warnings = (
                    user.warnings_count > 0
                    and user.warnings_valid_until > datetime.datetime.now()
            )
        else:
            self.warnings_count = 0
            self.warnings_valid_until = None
            self.has_active_warnings = False
