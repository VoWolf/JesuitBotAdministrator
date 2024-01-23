from modules.instances.bot_instance import bot as tserberus
from modules.work_with_user_stuff.user_klass import UserData
from telebot import types


class VoteData:
    """Helps with vote process"""
    def __init__(self, user_id, username, message_id):
        self.votes_za: int = 0
        self.votes_protiv: int = 0
        self.voted_users: list = []
        self.message_to_edit_id: int = message_id
        self.userdata = UserData(user_id=user_id, username=username)
        self.voted_users.append(self.userdata.username)

    def vote_process_accept(self, message):
        """Creates a new vote za
        checks if votes za > half of group"""
        self.votes_za += 1
        self.update_vote_information_message(message)
        if self.check_za_votes(message):
            self.userdata.do_user_free(message=message)
            tserberus.edit_message_text(
                f"Пользователь {self.userdata.username} реабелитирован и снова может отправлять сообщения!"
            )

    def vote_process_cancel(self, message):
        """Creates a new vote protiv"""
        self.votes_protiv += 1
        self.update_vote_information_message(message)

    def update_vote_information_message(self, message):
        """Updates message or sends new if Error"""
        buttons = types.InlineKeyboardMarkup()
        buttons.row(
            types.InlineKeyboardButton("Да", callback_data="za"),
            types.InlineKeyboardButton("Нет", callback_data="protiv")
        )
        try:
            tserberus.edit_message_text(
                f"ГОЛОСОВАНИЕ\nРазмутить {self.userdata.username}?\nДа: "
                f"{self.votes_za} голосов | Нет: {self.votes_protiv} голосов\nПроголосовали: "
                f"{', '.join(self.voted_users[1:])}", message.chat.id, self.message_to_edit_id + 1, reply_markup=buttons
            )
        except:
            tserberus.send_message(
                message.chat.id, f"ГОЛОСОВАНИЕ\nРазмутить {self.userdata.username}?\nДа: "
                f"{self.votes_za} голосов | Нет: {self.votes_protiv} голосов\nПроголосовали: "
                f"{', '.join(self.voted_users[1:])}", reply_markup=buttons
            )

    @staticmethod
    def check_za_votes(message):
        """Returns True if voted > 1/2 of group
        False if not"""
        if tserberus.get_chat_member_count(message.chat.id) // 2 - 2:
            return True
        return False


vote_data = VoteData(
    user_id=0,
    username="None",
    message_id=0
    )


def vote(message):
    """Starts vote"""
    global vote_data
    if message.reply_to_message:
        vote_data = VoteData(
            user_id=message.reply_to_message.from_user.id,
            username=message.reply_to_message.from_user.username,
            message_id=message.id
        )
        buttons = types.InlineKeyboardMarkup()
        buttons.row(
            types.InlineKeyboardButton("Да", callback_data="za"),
            types.InlineKeyboardButton("Нет", callback_data="protiv")
        )
        tserberus.reply_to(message, f"ГОЛОСОВАНИЕ\nРазмутить {message.reply_to_message.from_user.username}?\nДа: "
                                    "0 голосов | Нет: 0 голосов", reply_markup=buttons)
    else:
        tserberus.send_message(message.chat.id, "Данную команду надо использовать ответом на сообщение")


def vote_process_accept(call):
    """Add a new vote za, unmute if votes za > 1/2 of chat members"""
    global vote_data
    vote_data.vote_process_accept(message=call.message)


def vote_process_cancel(call):
    """Add a new vote protiv"""
    global vote_data
    vote_data.vote_process_cancel(message=call.message)


def callback_handler(call):
    """To execute buttons call.data"""
    global vote_data
    command = call.data
    if call.from_user.username not in vote_data.voted_users:
        vote_data.voted_users.append(call.from_user.username)
        match command:
            case "za":
                vote_process_accept(call)
            case "protiv":
                vote_process_cancel(call)
