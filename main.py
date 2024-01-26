import modules.command_executors.auto_pilot_executor
import modules.command_executors.message_check_executor
import modules.command_executors.vote_executor
from modules.domain.cerberus import Cerberus
from modules.instances.bot_instance import bot


@bot.message_handler(commands=["append"])
def append(message):
    cerberus = Cerberus(message)
    cerberus.add_forbidden_word()


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
    modules.command_executors.auto_pilot_executor.auto_pilot_on(message)


@bot.message_handler(commands=["auto_off"])
def auto_pilot(message):
    modules.command_executors.auto_pilot_executor.auto_pilot_off(message)


@bot.message_handler(commands=["vote"])
def vote(message):
    modules.command_executors.vote_executor.vote(message)


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    modules.command_executors.message_check_executor.message_handle(message)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    modules.command_executors.vote_executor.callback_handler(call)


bot.infinity_polling(none_stop=True)
