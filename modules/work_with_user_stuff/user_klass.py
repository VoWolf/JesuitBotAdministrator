from modules.instances.bot_instance import bot as tserberus
import time


class UserData:
    """Helps with user storage"""
    def __init__(self, username, user_id):
        self.username: str = username
        self.userid: int = user_id

    def do_user_free(self, message):
        """Unmute current user"""
        tserberus.restrict_chat_member(
            message.chat.id, self.userid, can_send_messages=True, can_send_media_messages=True,
            can_send_other_messages=True, can_add_web_page_previews=True
        )

    def do_user_strict(self, message, duration):
        """Mute current user"""
        if message.from_user.username not in ["innorif2099", "IezyitskyGuardBot", "LastUwUlf2001"]:
            tserberus.restrict_chat_member(message.chat.id, self.userid, until_date=time.time() + duration * 60)


