"""Главный файл"""
from modules.db.Create_tables import create_tables
from modules.domain._CommandExecutor import Commands
from modules.instances.bot_instance import BOT
# from modules.domain.decorators import


create_tables()


@BOT.message_handler(commands=["start"])
def start(message):
    cmd = Commands(message)
    cmd.start()


@BOT.message_handler(regexp="Церберус, кто я")
def user_statistics(message):
    pass


@BOT.message_handler(regexp="Церберус, мои свободные дни")
def free_days(message):
    cmd = Commands(message)
    cmd.send_free_user_days()


@BOT.message_handler(regexp="Церберус, пригласи @")
def add_member(message):
    pass


@BOT.message_handler(regexp=["Церберус, прогони @"])
def ban_member(message):
    cmd = Commands(message)
    cmd.ban_user()


@BOT.message_handler(regexp="Церберус, добавь стоп-слово")
def add_stop_word(message):
    cmd = Commands(message)
    cmd.add_stop_word()


@BOT.message_handler(regexp="Церберус, удали стоп-слово")
def del_stop_word(message):
    cmd = Commands(message)
    cmd.delete_stop_word()


@BOT.message_handler(regexp="Церберус, прогулки")
def planned_walks(message):
    cmd = Commands(message)
    cmd.send_planned_walks()


@BOT.message_handler(regexp="Церберус, добавь прогулку")
def add_walk(message):
    pass


@BOT.message_handler(startwith="Церберус")
def add_walk(message):
    pass


BOT.infinity_polling(none_stop=True)
