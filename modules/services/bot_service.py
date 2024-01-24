from modules.instances.bot_instance import bot as tserberus


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
