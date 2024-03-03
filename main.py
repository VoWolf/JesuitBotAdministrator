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
    cerberus = Cerberus(
        message=message,
        user=False,
        message_form=True,
        forbidden_words=False
    )
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
def my_rating(message):
    """
    Отправляет в чат рейтинг пользователя
    :return:
    """
    cerberus = Cerberus(
        message=message,
        user=True,
        message_form=True,
        forbidden_words=False
    )
    cerberus.my_rating()


@bot.message_handler(commands=["add_forbidden_word"])
def add_forbidden_word(message):
    """
    Добавляет стоп-слово введенное после команды
    :return:
    """
    cerberus = Cerberus(
        message=message,
        user=False,
        message_form=True,
        forbidden_words=True
    )
    cerberus.extract_and_add_forbidden_word()


@bot.message_handler(commands=["delete_forbidden_word"])
def delete_forbidden_word(message):
    """
    Удалеят стоп-слово введенное после команды
    :return:
    """
    cerberus = Cerberus(
        message=message,
        user=False,
        message_form=True,
        forbidden_words=True
    )
    cerberus.extract_and_remove_forbidden_word()


@bot.message_handler(commands=["rating_change"])
def rating_change(message):
    """
    Изменяет спам рейтинг выбранного пользователя
    :return:
    """
    cerberus = Cerberus(
        message=message,
        user=True,
        message_form=True,
        forbidden_words=False
    )
    cerberus.extract_and_change_rating()


@bot.message_handler(commands=["tie_chats"])
def tie_chats(message):
    """
    Начинает связывание чатов, отправляет токен для привязки
    :return:
    """
    cerberus = Cerberus(
        message=message,
        user=False,
        message_form=True,
        forbidden_words=False
    )
    cerberus.tie_chats()


@bot.message_handler(commands=["snap_chats"])
def snap_chats(message):
    """
    Заканчивает связывание чатов
    :return:
    """
    cerberus = Cerberus(
        message=message,
        user=False,
        message_form=True,
        forbidden_words=False
    )
    cerberus.snap_chats()


@bot.message_handler(commands=["autodelete_speed"])
def autodelete_speed(message):
    """
    Регулирует авто удаление технических сообщений от бота
    :return:
    """
    cerberus = Cerberus(
        message=message,
        user=True,
        message_form=True,
        forbidden_words=False
    )
    cerberus.change_autodelete_time()


@bot.message_handler(commands=["remember_admins"])
def admin_stat(message):
    """
    Вносит в базу данных всех участников чата как
    администраторов
    :return:
    """
    cerberus = Cerberus(
        message=message,
        user=True,
        message_form=True,
        forbidden_words=False
    )
    cerberus.admin_stat()


@bot.message_handler(commands=["remember_admins"])
def delete_admin_stat(message):
    """
    Вносит в базу данных всех участников чата как
    администраторов
    :return:
    """
    cerberus = Cerberus(
        message=message,
        user=True,
        message_form=True,
        forbidden_words=False
    )
    cerberus.delete_admin_stat()


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
