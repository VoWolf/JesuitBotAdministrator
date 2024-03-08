"""Объявляет класс MessageForm"""

import time
from modules.db.database import BotsMessages, AutoDeleteTime
from modules.domain.forbidden_words import ForbiddenWords


class MessageForm:
    """
    Класс, объединяющий в себе 2 функции:

    1) Проверка сообщений отправленных в чат, работа с сообщениями
    бота (добавлять/удалять их из базы), менеджмент сообщений

    2) Хранение шаблонов различных сообщений (набор методов для
    получения тех или иных текстов)
    """
    def __init__(self, message):
        self.message = message
        self.message_id = message.id
        self.chat_id = message.chat.id
        self.message_text = message.text
        self.forbidden_words = self.get_forbidden_words()

    @staticmethod
    def change_autodelete_time(new_autodelete_time: int) -> None:
        """
        Изменяет время через которое сообщения бота будут удалены
        :param new_autodelete_time:
        """
        AutoDeleteTime.get_by_id(1).autodelete_time = new_autodelete_time

    @staticmethod
    def get_forbidden_words() -> list:
        """
        Подключается к таблице ForbiddenWord и
        получает список запрещенных слов
        """
        fws = ForbiddenWords()
        return fws.return_forbidden_words()

    @staticmethod
    def return_ready_message_text(sample: int, **text_values: str) -> str:
        """
         Возвращает готовое текстовое сообщение (подставляет данные именованные аргументы
         в выбранный номер шаблона)
        :param sample: номер шаблона, в который будут подставляться значения
        :param text_values: значения, которые подставляются в шаблоны
        """
        values = tuple(map(str, list(text_values.values())))
        return {
            0: "{}, вы подозреваетесь в {}!\nВаш рейтинг: {}\nПожалуйста, будьте впредь поаккуратнее, удачи:)",
            1: "ГОЛОСОВАНИЕ!\nДобавить в чат пользователя {}?\nДополнительная информация:\nБудущая подпись "
               "пользователя (кастомное звание): {}\nСообщение ему в лс: {}\nГолосов за: {} | Голосов против: {}",
            2: "Пользователь {} забанен {}\nПричина: {}",
            3: "Пользователь {} кикнут из чата! Причина: {}",
            4: "ЖЕЛТОЕ ПРЕДУПРЕЖДЕНИЕ!\n{} опустил свой рейтинг ниже 0! (рейтинг сейчас: {})",
            5: "КРАСНОЕ ПРЕДУПРЕЖДЕНИЕ!!!\n{} опустил свой рейтинг ниже -25! (рейтинг сейчас: {})",
            6: "БОРДОВАЯ ТРЕВОГА!!!\n{} опустил свой рейтинг ниже -50!! (рейтинг сейчас: {}) Просьба принять срочные"
            " меры!",
            7: "Пользователь {} автоматически забанен навсегда, его рейтинг {} ниже 50.",
            8: "Привет! Я бот-администратор для помощи и контроля за чатом",
            9: "Пользователь {}\nВаш спам-рейтинг: {}\nВаш рейтинг токсичности: {}",
            10: "Слово {} добавлено в список запрещенных слов (Действие совершил администратор {})",
            11: "Слово {} удалено из списка запрещенных слов (Действие совершил администратор {})",
            12: "Рейтинг пользователя {} сменен на {} (Действие совершил администратор {})",
            13: "Время автоудаления сообщений бота изменено на {} секунд (Действие совершил администратор {})",
            14: "Процесс связывания чатов начат! Ваш токен: '{}'. В чате с администрацией введите команду "
                "<code>/snap_chats {}</code>",
            15: "Процесс связывания чатов успешно завершен!",
            16: "К сожалению, произошла ошибка!\nКод ошибки: {}.",
            17: "{} назначен администратором!",
            18: "{} снят с должности администратора!",
            19: "Данная команда должна быть использована ответом на сообщение!",
            20: "...",
            21: "Знакомьтесь, это {}!{}"
        }[sample].format(*values)

    def toxic_check_message(self) -> bool:
        """
        Проверяет текст сообщений на наличие
        запрещенных слов
        """
        for word in self.forbidden_words:
            if word in self.message_text:
                return True
        return False

    def spam_check_message(self) -> bool:
        """
        Проверяет сообщение на наличие спама
        """
        # here is check
        if input():
            return False
        return True

    def insert_message_in_bots_messages_table(self, time_until_exists: int) -> None:
        """
        Вносит текущее сообщение в таблицу BotsMessages
        :param time_until_exists:
        """
        BotsMessages.create(
            message_id=self.message_id,
            time_until=time.time() + time_until_exists
        )
