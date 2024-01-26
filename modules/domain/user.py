from modules.constants.users import ADMINS, USERS_PROTECTED_FROM_MUTE


class User:
    """User class"""

    def __init__(self, username, user_id):
        self.username: str = username
        self.user_id: int = user_id
        self.is_admin = self.username in ADMINS
        self.can_be_muted = self.username not in USERS_PROTECTED_FROM_MUTE
