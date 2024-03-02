"""Главный файл; рабочий цикл здесь"""


from modules.db.database import create_tables
from modules.domain.cerberus import Cerberus
from modules.instances.bot_instance import bot

create_tables()


@bot.message_handler(commands=["start", "restart"])
def start(message):
    """
    Отправляет сообщение
    :param message:
    :return:
    """
    cerberus = Cerberus(message)
    cerberus.start()


@bot.message_handler(commands=["print_forbidden_words"])  # Функция разработчика
def print_forbidden_words(message):
    """
    Печатает список стоп-слов, тестовая функция
    :param message:
    :return:
    """
    cerberus = Cerberus(message)
    cerberus.print_forbidden_words()


@bot.message_handler(commands=["my_rating"])
def my_rating():
    """
    Отправляет в чат рейтинг пользователя
    :return:
    """
    print("huj")


@bot.message_handler(commands=["add_forbidden_word"])
def add_forbidden_word():
    """
    Добавляет стоп-слово введенное после команды
    :return:
    """
    print("huj")


@bot.message_handler(commands=["delete_forbidden_word"])
def delete_forbidden_word():
    """
    Удалеят стоп-слово введенное после команды
    :return:
    """
    print("huj")


@bot.message_handler(commands=["rating_change"])
def rating_change():
    """
    Изменяет рейтинг выбранного пользователя
    :return:
    """
    print("huj")


@bot.message_handler(commands=["tie_chats"])
def tie_chats():
    """
    Начинает связывание чатов, отправляет токен для привязки
    :return:
    """
    print("huj")


@bot.message_handler(commands=["snap_chats"])
def snap_chats():
    """
    Заканчивает связывание чатов
    :return:
    """
    print("huj")


@bot.message_handler(commands=["autodelete_speed"])
def autodelete_speed():
    """
    Регулирует авто удаление технических сообщений от бота
    :return:
    """
    print("huj")


@bot.message_handler(commands=["tag"])
def tag():
    """
    Добавляет отмеченного участка в список тех, кого бот будет
    отмечать при подозрениях к участникам
    :return:
    """
    print("huj")


@bot.message_handler(commands=["do_not_tag"])
def do_not_tag():
    """
    Удаляет отмеченного участка в список тех, кого бот будет
    отмечать при подозрениях к участникам
    :return:
    """
    print("huj")


@bot.message_handler(commands=["remember_admins"])
def remember_admins():
    """
    Вносит в базу данных всех участников чата как
    администраторов
    :return:
    """
    print("huj")


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    """
    Откликается на каждое текстовое сообщение; проверяет их
    :param message:
    :return:
    """
    cerberus = Cerberus(message)
    cerberus.handle_message()


@bot.callback_query_handler(func=lambda call: True)
def callback():
    """
    Реагирует на нажатие инлайн кнопок
    :return:
    """
    print("huj")


bot.infinity_polling(none_stop=True)
