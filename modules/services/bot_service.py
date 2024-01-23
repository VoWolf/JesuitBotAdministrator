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



def print_forbidden_words(message):
    if message.from_user.username == "LastUwUlf2001":
        tserberus.send_message(message.chat.id, str(forbidden_words))
    else:
        tserberus.send_message(message.chat.id, "Ты не можешь этого сделать!)")



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
                return
            tserberus.restrict_chat_member(chat_id, user_id, until_date=time.time()+duration*60)
            tserberus.reply_to(
                message, f"Пользователь {message.reply_to_message.from_user.username} замучен на {duration} минут."
            )
        else:
            tserberus.reply_to(message, "Ты не можешь этого сделать!)")
    else:
        tserberus.reply_to(message, "Эту команду надо использовать ответом на сообщение!")
