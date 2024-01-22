from modules.instances.bot_instance import bot as tserberus
import time
from telebot import types

warned_users = {}
auto = False
mute_time = 300
mute_pause_time = 300
vote_data = [0, 0, [], -1, ["", 0]]  # za, protiv, voted, message_id, voted_username, voted_id


def vote(message):
    """Starts vote"""
    global vote_data
    if message.reply_to_message:
        vote_data = [0, 0, [], -1, ["", 0]]
        vote_data[2].append(message.reply_to_message.from_user.username)
        vote_data[4][0] = message.reply_to_message.from_user.username
        vote_data[4][1] = message.reply_to_message.from_user.id
        buttons = types.InlineKeyboardMarkup()
        buttons.row(
            types.InlineKeyboardButton("Да", callback_data="za"),
            types.InlineKeyboardButton("Нет", callback_data="protiv")
        )
        tserberus.reply_to(message, f"ГОЛОСОВАНИЕ\nРазмутить {message.reply_to_message.from_user.username}?\nДа: "
                                    f"{vote_data[0]} голосов | Нет: {vote_data[1]} голосов", reply_markup=buttons)
        vote_data[3] = message.id
    else:
        tserberus.send_message(message.chat.id, "Данную команду надо использовать ответом на сообщение")


def vote_process_accept(call):
    """Add a new vote za, unmute if votes za > 1/2"""
    global vote_data
    vote_data[0] += 1
    buttons = types.InlineKeyboardMarkup()
    buttons.row(
        types.InlineKeyboardButton("Да", callback_data="za"),
        types.InlineKeyboardButton("Нет", callback_data="protiv")
    )
    try:
        tserberus.edit_message_text(f"ГОЛОСОВАНИЕ\nРазмутить {vote_data[4][0]}?\nДа: "
                                    f"{vote_data[0]} голосов | Нет: {vote_data[1]} голосов\nПроголосовали: "
                                    f"{', '.join(vote_data[2][1:])}", call.message.chat.id, vote_data[3] + 1,
                                    reply_markup=buttons)
    except:
        tserberus.send_message(call.message.chat.id, f"ГОЛОСОВАНИЕ\nРазмутить {vote_data[4][0]}?\nДа: {vote_data[0]} "
                                                     f"голосов | Нет: {vote_data[1]} голосов\nПроголосовали: "
                                                     f"{', '.join(vote_data[2][1:])}",
                                                     reply_markup=buttons)
    if vote_data[0] > tserberus.get_chat_member_count(call.message.chat.id) // 2 - 2:
        chat_id = call.message.chat.id
        user_id = vote_data[4][1]
        tserberus.restrict_chat_member(
            chat_id, user_id, can_send_messages=True, can_send_media_messages=True,
            can_send_other_messages=True, can_add_web_page_previews=True
        )
        tserberus.edit_message_text(f"Пользователь {vote_data[4][0]} реабилитирован", call.message.chat.id,
                                    vote_data[3] + 1)
        vote_data = [0, 0, [], -1, ["", 0]]


def vote_process_cancel(call):
    """Vote +1 protiv"""
    global vote_data
    vote_data[1] += 1
    buttons = types.InlineKeyboardMarkup()
    buttons.row(
        types.InlineKeyboardButton("Да", callback_data="za"),
        types.InlineKeyboardButton("Нет", callback_data="protiv")
    )
    try:
        tserberus.edit_message_text(f"ГОЛОСОВАНИЕ\nРазмутить {vote_data[4][0]}?\nДа: "
                                    f"{vote_data[0]} голосов | Нет: {vote_data[1]} голосов\nПроголосовали: "
                                    f"{', '.join(vote_data[2][1:])}", call.message.chat.id, vote_data[3] + 1,
                                    reply_markup=buttons)
    except:
        tserberus.send_message(call.message.chat.id, f"ГОЛОСОВАНИЕ\nРазмутить {vote_data[4][0]}?\nДа: "
                                    f"{vote_data[0]} голосов | Нет: {vote_data[1]} голосов\nПроголосовали: "
                                    f"{', '.join(vote_data[2][1:])}", reply_markup=buttons)


def auto_pilot_on(message):
    """Turns on auto mute"""
    global mute_time, auto, mute_pause_time
    if check_admin(message):
        try:
            mute_time = int(message.text.split()[1])
            mute_pause_time = int(message.text.split()[2])
        except IndexError:
            tserberus.reply_to(message, "Тебе нужно указать время автомута и время автоудаления после предупреждения"
                                        " через пробел от команды!")
            return
        except ValueError:
            tserberus.reply_to(message, "Тебе нужно указать время автомута и время автоудаления после предупреждения "
                                        "через пробел от команды. \n*Для дураков: ЭТО ЧИСЛА!")
            return
        auto = True
        tserberus.reply_to(message, f"Автомут включен!\nСведения:\nВремя между предупреждениями: {mute_pause_time} "
                                    f"минут\nВремя автомута: {mute_time} минут")
    else:
        tserberus.reply_to(message, "Ты не можешь этого сделать!)")


def auto_pilot_off(message):
    """Turns off auto mute"""
    global auto
    if check_admin(message):
        auto = False
        tserberus.reply_to(message, "Автомут отключен!")
    else:
        tserberus.reply_to(message, "Ты не можешь этого сделать!)")


def message_handle(message):
    global warned_users
    if check_message(message):

        nik = message.from_user.username
        tserberus.delete_message(message.chat.id, message.id)
        if auto:
            for el in list(warned_users.keys()):
                if warned_users[el] < time.time():
                    del warned_users[el]
            if nik in list(warned_users.keys()):
                if message.from_user.username not in ["innorif2099", "IezyitskyGuardBot"]:
                    tserberus.restrict_chat_member(message.chat.id, message.from_user.id, until_date=time.time() + mute_time*60)
                    tserberus.send_message(message.chat.id, f"Попуск {nik} лишен права отправлять сообщения на {mute_time} "
                                                        f"минут за повторное наружение правил (Отдыхай)")
            else:
                tserberus.send_message(message.chat.id, f"{nik}, вы нарушили правила! За повторное нарушение в"
                                                        f" ближайшие {mute_pause_time} минут то вы будете замучены!")
                warned_users[nik] = time.time() + mute_pause_time*60
        else:
            if message.from_user.username not in ["innorif2099", "IezyitskyGuardBot"]:
                tserberus.send_message(message.chat.id, f"Сообщение скрыто")


def check_message(message):
    forbidden_words = ["сука", "пидор", "долбоеб", "еблан", "шлюх", "хуесос", "пидар", "немощь", "тупой", "тупая",
                       "далбаеб", "клоун", "даун", "аутист", "птеух", "дебил", "дибил", "шавка", "шафка", "гнида",
                       "лох", "лохушка", "мразь", "мудак", "нахал", "паскуда", "поскуда", "проститутка", "сволочь",
                       "тварь", "ублюдок", "выродок", "уебан", "писька", "пэска", "гандон", "бомж", "глупый", "урод",
                       "пиздюк", "хуила", "хуйло", "гей в панам", "пидрила", "хуило", "уебище", "шалав", "обезьян"]
    for el in forbidden_words:
        if el in message.text.lower():
            return True
    return False


def start(message):
    tserberus.send_message(message.chat.id, "Привет! Я бот администратор, помогаю управлять чатом:)")


def mute_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        if check_admin(message):
            duration = 5
            try:
                args = message.text.split()[1]
            except IndexError:
                args = None
            if args:
                try:
                    duration = int(args)
                except ValueError:
                    tserberus.reply_to(message, "Неправильный формат времени!")
                    return
                if duration < 1:
                    tserberus.reply_to(message, "Минимальное время 1 минута!")
                    return
                if duration > 1440:
                    tserberus.reply_to(message, "Максимальное время 24 часа (1440 минут)!")
                    return
            print(message.reply_to_message.from_user.username)
            if message.reply_to_message.from_user.username in ["innorif2099", "IezyitskyGuardBot"]:
                tserberus.reply_to(message, "К сожалению, бога забанить невозможно!")
                print()
                return
            tserberus.restrict_chat_member(chat_id, user_id, until_date=time.time()+duration*60)
            tserberus.reply_to(
                message, f"Пользователь {message.reply_to_message.from_user.username} замучен на {duration} минут."
            )
        else:
            tserberus.reply_to(message, "Ты не можешь этого сделать!)")
    else:
        tserberus.reply_to(message, "Эту команду надо использовать ответом на сообщение!")


def check_admin(message):
    if message.from_user.username in ["LastUwUlf2001", "innorif2099"]:
        return True
    return False


def unmute_user(message):
    if check_admin(message):
        if message.reply_to_message:
            chat_id = message.chat.id
            user_id = message.reply_to_message.from_user.id
            tserberus.restrict_chat_member(
                chat_id, user_id, can_send_messages=True, can_send_media_messages=True,
                can_send_other_messages=True, can_add_web_page_previews=True
            )
            tserberus.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} размучен.")
        else:
            tserberus.reply_to(
                message,
                "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите размутить."
            )
    else:
        tserberus.reply_to(message, "Ты не можешь этого сделать!)")


def callback_handler(call):
    global vote_data
    command = call.data
    if call.from_user.username not in vote_data[2]:
        vote_data[2].append(call.from_user.username)
        match command:
            case "za":
                vote_process_accept(call)
            case "protiv":
                vote_process_cancel(call)
