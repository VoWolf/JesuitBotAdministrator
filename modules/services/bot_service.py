from modules.instances.bot_instance import bot as tserberus
import time
from telebot import types

mute_time = 300
mute_pause_time = 300


# movwed to vote_executor

def append(message):
    global forbidden_words
    if message.from_user.username == "LastUwUlf2001":
        try:
            word = int(message.text.split()[1])
        except (IndexError, ValueError):
            word = 0
        try:
            word_letters_cut = int(message.text.split()[2])
        except (IndexError, ValueError):
            word_letters_cut = 0
        try:
            print(message.reply_to_message.text.split()[word][0:-word_letters_cut])
            forbidden_words.append(message.reply_to_message.text.split()[word][0:-word_letters_cut].lower())
            tserberus.reply_to(message, "Список запрещенных слов обновлен!")
        except IndexError:
            tserberus.reply_to(message, "Произошла ошибка! Скорее всего, ты указал несуществующий индекс!")
    else:
        tserberus.send_message(message.chat.id, "Ты не можешь этого сделать!)")




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


def print_forbidden_words(message):
    if message.from_user.username == "LastUwUlf2001":
        tserberus.send_message(message.chat.id, str(forbidden_words))
    else:
        tserberus.send_message(message.chat.id, "Ты не можешь этого сделать!)")


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