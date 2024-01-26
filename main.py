from modules.db.database import create_tables
from modules.domain.cerberus import Cerberus
from modules.instances.bot_instance import bot

create_tables()


@bot.message_handler(commands=["append"])
def append(message):
    cerberus = Cerberus(message)
    cerberus.add_forbidden_word()


@bot.message_handler(commands=["remove"])
def remove(message):
    cerberus = Cerberus(message)
    cerberus.remove_forbidden_word()


@bot.message_handler(commands=["print_forbidden_words"])
def print_forbidden_words(message):
    cerberus = Cerberus(message)
    cerberus.print_forbidden_words()


@bot.message_handler(commands=["start", "restart"])
def start(message):
    cerberus = Cerberus(message)
    cerberus.start()


@bot.message_handler(commands=["mute"])
def mute(message):
    cerberus = Cerberus(message)
    cerberus.mute_user()


@bot.message_handler(commands=["unmute"])
def unmute(message):
    cerberus = Cerberus(message)
    cerberus.unmute_user()


@bot.message_handler(commands=["auto_on"])
def auto_pilot(message):
    cerberus = Cerberus(message)
    cerberus.turn_pilot_on()


@bot.message_handler(commands=["auto_off"])
def auto_pilot(message):
    cerberus = Cerberus(message)
    cerberus.turn_pilot_off()


@bot.message_handler(commands=["vote"])
def vote(message):
    cerberus = Cerberus(message)
    cerberus.start_unmute_poll()


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    cerberus = Cerberus(message)
    cerberus.handle_message()


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    print("huj")
    # modules.command_executors.vote_executor.callback_handler(call)


@bot.poll_handler(func=lambda call: True)
def callback(call):
    print(call)
    print(call.options[0])
    print(call.options[1])


bot.infinity_polling(none_stop=True)
