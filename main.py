"""Главный файл"""
import telebot

from modules.instances.bot_instance import BOT


@BOT.message_handler(commands=["start"])
def start(message):
    pass


@BOT.message_handler(commands=["me", "my_stata"], regexp="Церберус, кто я")
def user_statistics(message):
    pass


@BOT.message_handler(commands=["my_free_days"], regexp="Церберус, мои свободные дни")
def free_days(message):
    pass


@BOT.message_handler(commands=["add_member"], regexp="Церберус, добавить @")
def add_member(message):
    pass


@BOT.message_handler(commands=["BAN"], regexp=["Церберус, забань @", "Церберус, прогони @"])
def ban_member(message):
    pass


@BOT.message_handler(commands=["add_stop_word"], regexp="Церберус, добавить стоп-слово")
def add_stop_word(message):
    pass


@BOT.message_handler(commands=["del_stop_word"], regexp="Церберус, удалить стоп-слово")
def del_stop_word(message):
    pass


@BOT.message_handler(commands=["planned_walks"], regexp="Церберус, прогулки")
def planned_walks(message):
    pass


@BOT.message_handler(commands=["add_walk"], regexp="Церберус, добавь прогулку")
def add_walk(message):
    pass


BOT.infinity_polling(none_stop=True)
