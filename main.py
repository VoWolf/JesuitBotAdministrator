"""Главный файл"""
from modules.domain.cerberus import Cerberus
from modules.instances.bot_instance import BOT
from modules.db.database import create_tables
# from modules.domain.decorators import


create_tables()


@BOT.message_handler(commands=["start"])
def start(message):
    cerberus = Cerberus(message)
    cerberus.send(text="Привет! Я - бот администратор, помогу разобраться с чатом")


@BOT.message_handler(regexp="Церберус, кто я")
def user_statistics(message):
    pass


@BOT.message_handler(regexp="Церберус, мои свободные дни")
def free_days(message):
    pass


def add_member(message, data):
    pass


@BOT.message_handler(regexp=["Церберус, прогони @"])
def ban_member(message, data):
    pass


@BOT.message_handler(regexp="Церберус, добавь стоп-слово")
def add_stop_word(message, data):
    pass


@BOT.message_handler(regexp="Церберус, удали стоп-слово")
def del_stop_word(message, data):
    pass


@BOT.message_handler(regexp="Церберус, прогулки")
def planned_walks(message):
    pass


@BOT.message_handler(regexp="Церберус, добавь прогулку")
def add_walk(message):
    pass


@BOT.message_handler(startwith="Церберус")
def add_walk(message):
    pass


BOT.infinity_polling(none_stop=True)
