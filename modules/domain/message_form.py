"""Объявляет класс MessageForm"""

import time

import telebot.types

from modules.db.database import BotsMessages


class MessageForm:
    """
    Класс, объединяющий в себе 2 функции:

    1) Проверка сообщений отправленных в чат, работа с сообщениями
    бота (добавлять/удалять их из базы), менеджмент сообщений

    2) Хранение шаблонов различных сообщений (набор методов для
    получения тех или иных текстов)
    """
    def __init__(self, message: telebot.types.Message) -> None:
        self.message: telebot.types.Message = message
        self.message_id: int = message.id
        self.chat_id: int = message.chat.id
        self.message_text: str = message.text

    @staticmethod
    def return_ready_message_text(sample: str, **text_values: str) -> str:
        """
         Возвращает готовое текстовое сообщение (подставляет данные именованные аргументы
         в выбранный номер шаблона)
        :param sample: номер шаблона, в который будут подставляться значения
        :param text_values: значения, которые подставляются в шаблоны
        """
        values = tuple(map(str, list(text_values.values())))
        return {
            "start_form": "Привет! Я бот администратор, и по системе рейтингов я буду отслеживать плохишей в группах и "
            "уведомлять вас о них",
            "ratings_form": "Пользователь {}!\n<b>Ваш рейтинг: {}.</b>\nИзменения за последние 5 дней:\n<code>{}</code>",
            "ess_rating_form": "Ваша эссенция неактива:\n<code>{}</code>\n1 уровень хранилища = +1 день афк (при "
                               "неактиве уровни отнимаются, по достижении 0 вас кикает из чата)",
            "change_rating": "Рейтинг пользователя {} теперь {}!",
            "changed_auto_mode": "Скорость автоудаления изменена! Теперь она составляет {} секунд."
        }[sample].format(*values)

    def toxic_check_message(self) -> bool:
        """
        Проверяет текст сообщений на наличие
        запрещенных слов
        """
        pass

    def insert_message_in_bots_messages_table(
            self,
            time_until_exists: int
    ) -> None:
        """
        Вносит текущее сообщение в таблицу BotsMessages
        :param time_until_exists:
        """
        BotsMessages.create(
            message_id=self.message_id,
            time_until=time.time() + time_until_exists
        )

    def extract_params(
            self,
            args_count: int | None = None
    ) -> list | bool:
        """
        Извлекает из текста сообщения нужные параметры для команд; В случае ошибки возвращает False
        :param args_count: Количество аргументов, которые мы хотим взять из строки.
        Если не передаем, то вернутся все
        """
        args_list = self.message_text.split()[1:]

        if args_count is None:
            return args_list

        if len(args_list) < args_count:
            return False

        return args_list[: args_count + 1]
