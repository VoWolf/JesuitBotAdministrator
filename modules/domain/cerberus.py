import datetime
from typing import Callable

from modules.db.database import ForbiddenWord, Pilot, Poll, PollOption
from modules.domain.user import User
from modules.instances.bot_instance import bot


class Cerberus:
    """Bot class"""

    def __init__(self, message):
        self.message = message

        self.chat_id = message.chat.id
        self.chat_members_count = bot.get_chat_member_count(message.chat.id)

        if message.reply_to_message:
            self.reply_to_message_author = User(
                username=message.reply_to_message.from_user.username,
                user_id=message.reply_to_message.from_user.id,
                chat_id=message.chat.id,
            )
        else:
            self.reply_to_message_author = None

        self.message_author = User(
            username=message.from_user.username,
            user_id=message.from_user.id,
            chat_id=message.chat.id,
        )

        fws = ForbiddenWord.select()
        self.forbidden_words = [fw.word for fw in fws]

        self.pilot = Pilot.get(Pilot.name == "autopilot")

    def send(self, text):
        """Sends new message"""
        bot.send_message(self.chat_id, text)

    def start(self):
        """Sends start message"""
        self.send("Привет! Я бот администратор, помогаю управлять чатом:)")

    def reply(self, text: str):
        """Replies to message"""
        bot.reply_to(self.message, text)

    def is_user_admin(self):
        """Checks if user is admin"""
        if not self.message_author.is_admin:
            self.reply("Ты не можешь этого сделать!)")
            return False
        return True

    def is_reply_to_message_author_exists(self):
        """Checks if author of reply to message exists"""
        if not self.reply_to_message_author:
            self.reply("Эту команду надо использовать ответом на сообщение!")
            return False
        return True

    def admin_guard(func: Callable):
        def inner(self):
            if not self.is_user_admin():
                return
            func(self)

        return inner

    def reply_user_guard(func: Callable):
        def inner(self):
            if not self.is_reply_to_message_author_exists():
                return
            func(self)

        return inner

    def refresh_forbidden_words(self):
        """Reloads forbidden words from database"""
        fws = ForbiddenWord.select()
        self.forbidden_words = [fw.word for fw in fws]

    @reply_user_guard
    @admin_guard
    def mute_user(self):
        """Mutes user"""
        try:
            mute_duration = extract_duration(self.message.text)
        except ValueError as err:
            self.reply(str(err.args))

            return

        if self.reply_to_message_author.can_be_muted:
            muted_until = datetime.datetime.now() + datetime.timedelta(
                minutes=mute_duration
            )

            bot.restrict_chat_member(
                self.chat_id,
                self.reply_to_message_author.user_id,
                until_date=muted_until,
            )

            self.reply_to_message_author.db_user.is_muted_until = muted_until
            self.reply_to_message_author.db_user.save()

            self.reply(
                f"Пользователь {self.reply_to_message_author.username} замуьючен на {mute_duration} минут."
            )
        else:
            self.reply("К сожалению, бога забанить невозможно!")

    @reply_user_guard
    @admin_guard
    def unmute_user(self):
        """Unmutes user"""
        bot.restrict_chat_member(
            self.chat_id,
            self.reply_to_message_author.user_id,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
        )

        self.reply(f"{self.reply_to_message_author.username} освобожден!")

    @admin_guard
    def print_forbidden_words(self):
        """Prints forbidden words list"""
        self.send(str(self.forbidden_words))

    @admin_guard
    def add_forbidden_word(self):
        """Adds forbidden word"""
        try:
            extract_and_add_forbidden_word(self.message.text)
            self.send("Список запрещенных слов обновлен!")
            self.refresh_forbidden_words()
        except ValueError as err:
            self.reply(str(err.args))

    @admin_guard
    def remove_forbidden_word(self):
        """Removes forbidden word"""
        try:
            extract_and_remove_forbidden_word(self.message.text)
            self.send("Список запрещенных слов обновлен!")
            self.refresh_forbidden_words()
        except ValueError as err:
            self.reply(str(err.args))

    @admin_guard
    def turn_pilot_on(self):
        """Turns autopilot on"""
        try:
            mute_time, mute_break_time = extract_pilot_params(self.message.text)
        except ValueError as err:
            self.reply(str(err.args))
            return

        self.pilot.is_on = True
        self.pilot.mute_time = mute_time
        self.pilot.mute_break_time = mute_break_time
        self.pilot.save()

        self.reply(
            f"Автомьют включен!\nСведения:\nВремя между предупреждениями: {mute_break_time} "
            f"минут\nВремя автомьюта: {mute_time} минут"
        )

    @admin_guard
    def turn_pilot_off(self):
        """Turns autopilot off"""
        self.pilot.is_on = False
        self.pilot.save()
        self.reply("Автомьют отключен!")

    def automute_user(self):
        muted_until = datetime.datetime.now() + datetime.timedelta(
            minutes=self.pilot.mute_time
        )

        bot.restrict_chat_member(
            self.chat_id,
            self.message_author.user_id,
            until_date=muted_until,
        )

        self.message_author.db_user.is_muted_until = muted_until
        self.message_author.db_user.save()

        self.send(
            f"Попуск {self.message_author.username} лишен права отправлять сообщения на "
            f"{self.pilot.mute_time}  минут за повторное наружение правил (Отдыхай)"
        )

    def handle_message(self):
        """Controls message for forbidden words"""
        if self.is_forbidden_word_in_message(self.message.text):
            bot.delete_message(self.chat_id, self.message.id)

            if self.pilot.is_on:
                if self.message_author.has_active_warnings:
                    self.automute_user()
                else:
                    self.message_author.db_user.warnings_count = 1
                    self.message_author.db_user.warnings_valid_until = (
                            datetime.datetime.now()
                            + datetime.timedelta(minutes=self.pilot.mute_break_time)
                    )
                    self.message_author.db_user.save()

                    self.send(
                        f"{self.message_author.username}, вы нарушили правила! За повторное нарушение в "
                        f"ближайшие {self.pilot.mute_break_time} минут то вы будете замьючены!"
                    )
            else:
                self.send(f"Сообщение от {self.message_author.username} скрыто")

    def is_forbidden_word_in_message(self, text: str):
        """Checks if message contains one of forbidden words"""
        for el in self.forbidden_words:
            if el in text.lower():
                return True

        return False

    @reply_user_guard
    def start_unmute_poll(self):
        if not self.reply_to_message_author.is_muted:
            return

        question = f"Размьютить пользователя {self.reply_to_message_author.username}?"

        result = bot.send_poll(
            chat_id=self.chat_id,
            question=question,
            options=["Да", "Нет"],
        )
        bot.delete_message(self.message.id)

        poll = Poll.create(
            question=question,
            is_closed=False,
            tg_message_id=result.message_id,
            tg_poll_id=result.poll.id,
        )

        PollOption.create(text="Да", voter_count=0, poll=poll)
        PollOption.create(text="Нет", voter_count=0, poll=poll)

    def handle_poll(self, call):
        print(call)


def extract_pilot_params(text: str):
    args_list = text.split()

    if len(args_list) < 3:
        raise ValueError(
            f"Тебе нужно указать время автомьюта и время автоудаления после предупреждения ",
            f"через пробел от команды. \n*Для дураков: ЭТО ЧИСЛА!",
        )

    try:
        mute_time = int(args_list[1])
    except Exception as exc:
        raise ValueError(
            "Время автомьюта должно быть числом (первый параметр)"
        ) from exc

    try:
        mute_break_time = int(args_list[2])
    except Exception as exc:
        raise ValueError(
            "Время автоудаления после предупреждения должно быть числом (второй параметр)"
        ) from exc

    return mute_time, mute_break_time


def extract_duration(text: str):
    """Extracts second word from string as duration(int)"""
    duration = 5

    args_list = text.split()

    if len(args_list) == 1:
        return duration

    try:
        duration = int(args_list[1])
    except Exception as exc:
        raise ValueError("Неправильный формат времени!") from exc

    if duration < 1:
        raise ValueError("Минимальное время 1 минута!")

    if duration > 1440:
        raise ValueError("Максимальное время 24 часа (1440 минут)!")

    return duration


def extract_and_add_forbidden_word(text: str):
    args_list = text.strip().split()

    if len(args_list) == 1:
        raise ValueError("Не указано запрещенное слово")

    forbidden_word = args_list[1].lower()
    forbidden_word_offset = 0

    if len(args_list) == 3:
        try:
            forbidden_word_offset = int(args_list[2])
        except Exception as exc:
            raise ValueError(
                "Произошла ошибка! Скорее всего, ты указал несуществующий индекс!"
            ) from exc

    if forbidden_word_offset != 0:
        forbidden_word = forbidden_word[0:-forbidden_word_offset]

    ForbiddenWord.create(word=forbidden_word)


def extract_and_remove_forbidden_word(text: str):
    args_list = text.strip().split()

    if len(args_list) == 1:
        raise ValueError("Не указано запрещенное слово")

    forbidden_word = args_list[1].lower()

    fw = ForbiddenWord.get(ForbiddenWord.word == forbidden_word)
    fw.delete_instance()
