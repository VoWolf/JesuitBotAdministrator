"""Главный файл"""
from modules.db.database import create_tables
# from modules.domain.cerberus import Cerberus
from modules.domain.decorators import Decorator
from modules.domain.user import User
from modules.instances.bot_instance import bot

create_tables()

dec = Decorator


@bot.message_handler(commands=["start", "restart"])
def start(message):
    """
    Отправляет сообщение
    :param message:
    :return:
    """
    pass


@dec.creator_guard
@bot.message_handler(commands=["print_forbidden_words"])  # Функция разработчика
def print_forbidden_words(message):
    """
    Печатает список стоп-слов, тестовая функция
    :param message:
    :return:
    """
    pass


@bot.message_handler(commands=["my_rating"])
def my_rating(message):
    """
    Отправляет в чат рейтинг пользователя
    :return:
    """
    pass


@dec.redirect_non_creators_to_vote(vote_text="Добавить слово {} к списку запрещенных слов?", admins_available=True)
@bot.message_handler(commands=["add_forbidden_word"])
def add_forbidden_word(message):
    """
    Добавляет стоп-слово введенное после команды
    :return:
    """
    pass


@bot.message_handler(commands=["delete_forbidden_word"])
def delete_forbidden_word(message):
    """
    Удалеят стоп-слово введенное после команды
    :return:
    """
    pass


@bot.message_handler(commands=["rating_change"])
def rating_change(message):
    """
    Изменяет спам рейтинг выбранного пользователя
    :return:
    """
    pass


@bot.message_handler(commands=["tie_chats"])
def tie_chats(message):
    """
    Начинает связывание чатов, отправляет токен для привязки
    :return:
    """
    pass


@bot.message_handler(commands=["snap_chats"])
def snap_chats(message):
    """
    Заканчивает связывание чатов
    :return:
    """
    pass


@bot.message_handler(commands=["autodelete_speed"])
def autodelete_speed(message):
    """
    Регулирует авто удаление технических сообщений от бота
    :return:
    """
    pass


@bot.message_handler(commands=["admin_stat"])
def admin_stat(message):
    """
    Вносит в базу данных всех участников чата как
    администраторов
    :return:
    """
    pass


@bot.message_handler(commands=["delete_admin_stat"])
def delete_admin_stat(message):
    """
    Вносит в базу данных всех участников чата как
    администраторов
    :return:
    """
    pass


@bot.message_handler(commands=["kick"])
def kick_user(message):
    pass


@bot.message_handler(commands=["ban"])
def ban_user(message):
    pass


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    """
    Откликается на каждое текстовое сообщение; проверяет их
    :param message:
    :return:
    """
    global dec
    dec = Decorator(
        message=message,
        user=User(message.from_user.id)
    )
    # print(message.from_user.id)
    # print("1")


@bot.callback_query_handler(func=lambda call: True)
def callback():
    """
    Реагирует на нажатие инлайн кнопок
    :return:
    """
    print("huj")


bot.infinity_polling(none_stop=True)
