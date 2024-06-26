import telebot.util

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
    cmd = Commands(message)
    cmd.delete_current_user_from_walk()


@BOT.message_handler(commands=["go"])
def go_to_walk(message):
    cmd = Commands(message)
    cmd.add_current_user_to_walk()


@BOT.message_handler(commands=["delete_walk"])
def delete_walk(message):
    cmd = Commands(message)
    cmd.delete_walk()


@BOT.message_handler(commands=["change_walk"])
def change_walk(message):
    cmd = Commands(message)
    cmd.change_walk()


@BOT.message_handler(commands=["cerb"])
def add_walk(message):
    cerberus = Cerberus(message)
    cerberus.send("На месте!")


@BOT.message_handler(commands=["add_free_day"])
def add_free_day(message):
    cmd = Commands(message)
    cmd.add_free_day()


@BOT.message_handler(commands=["del_free_day"])
def del_free_day(message):
    cmd = Commands(message)
    cmd.del_free_day()


@BOT.message_handler(commands=["mute"])
def mute_user(message):
    cmd = Commands(message)
    cmd.mute_user()


@BOT.message_handler(commands=["unmute"])
def unmute_user(message):
    cmd = Commands(message)
    cmd.unmute_user()


@BOT.message_handler(commands=["admin_stat"])
def give_admin_status(message):
    cmd = Commands(message)
    cmd.admin_status(admin=True)


@BOT.message_handler(commands=["del_admin_stat"])
def del_admin_status(message):
    cmd = Commands(message)
    cmd.admin_status(admin=False)


@BOT.poll_answer_handler(func=lambda poll_answer: True)
def register_poll_answer(answer: telebot.types.PollAnswer):
    if answer.option_ids[0] != 1:
        return


@BOT.message_handler(content_types=["text"])
def test(message):
    cmd = Commands(message)
    match message.text:
        case _ if "/walk_" in message.text.lower():
            cmd.get_walk_by_command_id(walk_id=telebot.util.extract_command(message.text).strip("/walk_"))
        case _ if "@" in message.text:
            cmd.check_calls(message.text[1:])


BOT.infinity_polling(none_stop=True)
