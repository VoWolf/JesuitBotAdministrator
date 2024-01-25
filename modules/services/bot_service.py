from modules.instances.bot_instance import bot as cerberus


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
            forbidden_words.append(
                message.reply_to_message.text.split()[word][0:-word_letters_cut].lower()
            )
            cerberus.reply_to(message, "Список запрещенных слов обновлен!")
        except IndexError:
            cerberus.reply_to(
                message,
                "Произошла ошибка! Скорее всего, ты указал несуществующий индекс!",
            )
    else:
        cerberus.send_message(message.chat.id, "Ты не можешь этого сделать!)")
