import modules.services.bot_service
from modules.instances.bot_instance import bot as tserberus


@tserberus.message_handler(commands=["append"])
def append(message):
    modules.services.bot_service.append(message)


@tserberus.message_handler(commands=["print_forbidden_words"])
def append(message):
    modules.services.bot_service.print_forbidden_words(message)


@tserberus.message_handler(commands=["start", "restart"])
def start(message):
    modules.services.bot_service.start(message)


@tserberus.message_handler(commands=["mute"])
def mute(message):
    modules.services.bot_service.mute_user(message)


@tserberus.message_handler(commands=["unmute"])
def unmute_user(message):
    modules.services.bot_service.unmute_user(message)


@tserberus.message_handler(commands=["auto_on"])
def auto_pilot(message):
    modules.services.bot_service.auto_pilot_on(message)


@tserberus.message_handler(commands=["auto_off"])
def auto_pilot(message):
    modules.services.bot_service.auto_pilot_off(message)


@tserberus.message_handler(commands=["vote"])
def vote(message):
    modules.


@tserberus.message_handler(func=lambda message: True)
def message_handler(message):
    modules.services.bot_service.message_handle(message)


@tserberus.callback_query_handler(func=lambda call: True)
def callback(call):
    modules.services.bot_service.callback_handler(call)


tserberus.infinity_polling(none_stop=True)
