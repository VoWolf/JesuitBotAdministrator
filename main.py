"""Главный файл"""
from modules.instances.bot_instance import bot
from modules.domain.cerberus import Cerberus
from modules.domain.message_form import MessageForm
from modules.domain.ratings_stuff import Ratings
from modules.db.database import *
from modules.domain.decorators import *

create_tables()


@bot.message_handler(commands=["start", "restart"])
def start(message) -> None:
    """
    Отправляет стартовое сообщение
    :param message:
    """
    cerberus = Cerberus(message=message)
    msg = MessageForm(message=message)
    cerberus.send(text=msg.return_ready_message_text(
        sample="start_form"
    ))


@bot.message_handler(commands=["my_rating"])
def my_rating(message):
    """
    Отправляет в чат рейтинг пользователя
    :return:
    """
    cerberus = Cerberus(message=message)
    msg = MessageForm(message=message)
    user = User(message=message)
    cerberus.send(msg.return_ready_message_text(
        sample="ratings_form",
        user=user.username,
        rating_now=user.db_user.active_rating,
        diagram="pass"
    ))
    cerberus.reply(text=msg.return_ready_message_text(
        sample="ess_rating_form",
        diagram="pass"
    ))


@redirect_non_creators_to_vote(vote_text="Изменить рейтинг пользователя {} на {}", admins_available=True)
@bot.message_handler(commands=["rating_change"])
def rating_change(message):
    """
    Изменяет спам рейтинг выбранного пользователя
    :return:
    """
    cerberus = Cerberus(message=message)
    msg = MessageForm(message=message)
    user = User(message=message)
    rating = Ratings(main_rating=user.db_user.ratings, active_rating=user.db_user.active_rating)
    rating_type, new_value = msg.extract_params(args_count=2)

    try:
        new_value = float(new_value)
    except ValueError or rating_type not in ["a", "m"]:
        cerberus.error(text="Указан неправильный тип данных! Пример ввода команды: /rating_change [тип рейтинга ("
                            "a - рейтинг активности, m - основной рейтинг)] [новое значение (дробное число в формате "
                            "xx:xx)]")
        return

    match rating_type:
        case "a":
            rating.change_main_rating(change_value=new_value, set_rating=True)
        case "b":
            rating.change_active_rating(value=round(new_value), set_rating=True)

    cerberus.reply(text=msg.return_ready_message_text(
        sample="change_rating",
        username=user.userrang if user.userrang is not None else user.username,
        new_rating=str(new_value)
    ))


@redirect_non_creators_to_vote(
    vote_text="Изменить время автоматического удаления сообщений на {}?", admins_available=True
)
@bot.message_handler(commands=["autodelete_speed"])
def autodelete_speed(message):
    """
    Регулирует авто удаление технических сообщений от бота
    :return:
    """
    cerberus = Cerberus(message=message)
    msg = MessageForm(message=message)

    new_autodelete_time = msg.extract_params(args_count=1)
    try:
        new_autodelete_time = int(new_autodelete_time)
    except ValueError:
        cerberus.error(text="Вы указали неправильный тип данных! Пример ввода команды: /autodelete_speed ["
                            "новое значение времени, через которые мои сообщения будут автоматически удалены, в "
                            "секундах]")
        return

    auto_mode = Chat.get(chat_id=message.chat.id).autodelete_speed
    auto_mode.autodelete_time = new_autodelete_time
    AutoDeleteTime.save(auto_mode)

    cerberus.reply(text=msg.return_ready_message_text(sample="changed_auto_mode"))


@redirect_non_creators_to_vote("Назначить пользователя {} на должность администратора?")
@bot.message_handler(commands=["admin_stat"])
def admin_stat(message):
    """
    Вносит в базу данных всех участников чата как
    администраторов
    :return:
    """
    cerberus = Cerberus(message=message)
    msg = MessageForm(message=message)
    user = User(message=message)



@redirect_non_creators_to_vote("Снять пользователя {} с должности администратора?")
@bot.message_handler(commands=["delete_admin_stat"])
def delete_admin_stat(message):
    """
    Вносит в базу данных всех участников чата как
    администраторов
    :return:
    """
    pass


@redirect_non_creators_to_vote("Кикнуть пользователя {} из чата?\nПричина: {}")
@bot.message_handler(commands=["kick"])
def kick_user(message):
    pass


@redirect_non_creators_to_vote("Забанить пользователя {}?\nПричина: {}")
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
    pass


@bot.callback_query_handler(func=lambda call: True)
def callback():
    """
    Реагирует на нажатие инлайн кнопок
    :return:
    """
    print("huj")


bot.infinity_polling(none_stop=True)
