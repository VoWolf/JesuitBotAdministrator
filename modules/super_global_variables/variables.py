from modules.instances.bot_instance import bot as tserberus


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

    def do_user_stricted(self, message):
        """Mute current user"""
        pass


# Here the values for vote_process

forbidden_words = ["сука", "пидор", "долбоеб", "еблан", "шлюх", "хуесос", "пидар", "немощь", "тупой", "тупая",
                   "далбаеб", "клоун", "даун", "аутист", "птеух", "дебил", "дибил", "шавка", "шафка", "гнида",
                   "лох", "лохушка", "мразь", "мудак", "нахал", "паскуда", "поскуда", "проститутка", "сволочь",
                   "тварь", "ублюдок", "выродок", "уебан", "писька", "пэска", "гандон", "бомж", "глупый", "урод",
                   "пиздюк", "хуила", "хуйло", "гей в панам", "пидрила", "хуило", "уебище", "шалав", "обезьян"]
# Here is all bad words that don't need to be mentioned:)

warned_users = {}
# Here is stored all users that should be muted if they break the rules again within the prescribed period

auto = False
# Indicates whether auto mode is enabled

auto_data = [0, 0]
# mute_time, mute_pause_time
# here is some values about auto mode
