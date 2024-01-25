import time

from modules.constants.users import admins, users_protected_from_mute
from modules.instances.bot_instance import bot as cerberus


class User:
    """User class"""

    def __init__(self, username, user_id):
        self.username: str = username
        self.user_id: int = user_id
        self.is_admin = self.username in admins
        self.can_be_muted = self.username not in users_protected_from_mute

    def mute(self, message, duration):
        """Mute user"""
        if self.can_be_muted:
            cerberus.restrict_chat_member(
                message.chat.id, self.user_id, until_date=time.time() + duration * 60
            )

    def unmute(self, message):
        """Unmute user"""
        cerberus.restrict_chat_member(
            message.chat.id,
            self.user_id,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
        )