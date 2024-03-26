from telebot.formatting import hlink

from modules.db.Create_tables import create_tables
from modules.domain.CommandExecutor import Commands
from modules.domain.cerberus import Cerberus
from modules.instances.bot_instance import BOT


create_tables()


@BOT.message_handler(commands=["start"])
def start(message):
    cmd = Commands(message)
    cmd.start()


@BOT.message_handler(commands=["me"])
def user_statistics(message):
    pass
    # link = hlink("Привет", "")
    # BOT.send_message(message.chat.id, f"{link}! Как дела?", parse_mode="HTML")


@BOT.message_handler(commands=["my_free_days"])
def free_days(message):
    cmd = Commands(message)
    cmd.send_free_user_days()


@BOT.message_handler(commands=["BAN"])
def ban_member(message):
    cmd = Commands(message)
    cmd.ban_user()


@BOT.message_handler(commands=["add_bad_word"])
def add_stop_word(message):
    cmd = Commands(message)
    cmd.add_stop_word()


@BOT.message_handler(commands=["delete_bad_word"])
def del_stop_word(message):
    cmd = Commands(message)
    cmd.delete_stop_word()


@BOT.message_handler(commands=["walks"])
def planned_walks(message):
    cmd = Commands(message)
    cmd.send_planned_walks()


@BOT.message_handler(commands=["add_walk"])
def add_walk(message):
    cmd = Commands(message)
    cmd.add_walk()


@BOT.message_handler(commands=["leave"])
def leave_walk(message):
    pass


@BOT.message_handler(commands=["delete_walk"])
def delete_walk(message):
    pass


@BOT.message_handler(commands=["change_walk"])
def change_walk(message):
    pass


@BOT.message_handler(commands=["walks_info"])
def walks_info(message):
    cmd = Commands(message)
    cmd.send_help_info_walks()


@BOT.message_handler(commands=["cerb"])
def add_walk(message):
    cerberus = Cerberus(message)
    cerberus.send("На месте!")


@BOT.message_handler(content_types=["text"])
def test(message):
    cmd = Commands(message)
    match message.text:
        case _ if "walk" in message.text.lower():
            cmd.get_walk_by_command()
        case _ if "@" in message.text:
            cmd.check_calls(message.text[1:])


BOT.infinity_polling(none_stop=True)
