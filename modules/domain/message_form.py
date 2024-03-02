"""Объявляет класс MessageForm"""

import time
from modules.db.database import BotsMessages
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
    def get_forbidden_words():
        """
        Подключается к таблице ForbiddenWord и
        получает список запрещенных слов
        :return:
        """
        fws = ForbiddenWords()
        return fws.return_forbidden_words()

    @staticmethod
    def return_ready_message_text(sample, **text_values):
        """
         Возвращает готовое текстовое сообщение (подставляет данные именованные аргументы
         в выбранный номер шаблона)
        :param sample:
        :param text_values:
        :return:
        """
        values = list(text_values.values())
        return {
            0: "{}, вы подозреваетесь в {}!\nВаш рейтинг: {}\nПожалуйста, будьте впредь поаккуратнее, удачи:)",
            1: "ГОЛОСОВАНИЕ!\nДобавить в чат пользователя {}?\nДополнительная информация:\nБудущая подпись "
               "пользователя (кастомное звание): {}\nСообщение ему в лс: {}",
            2: "Пользователь {} забанен {}\nПричина: {}",
            3: "Пользователь {} кикнут из чата! Причина: {}",
            4: "ЖЕЛТОЕ ПРЕДУПРЕЖДЕНИЕ!\n{} опустил свой рейтинг {} ниже 0! (рейтинг сейчас: {})",
            5: "КРАСНОЕ ПРЕДУПРЕЖДЕНИЕ!!!\n{} опустил свой рейтинг {} ниже -25! (рейтинг сейчас: {})",
            6: "БОРДОВАЯ ТРЕВОГА!!!\n{} опустил свой рейтинг {} ниже -50!! (рейтинг сейчас: {}) Просьба принять срочные"
            " меры!",
            7: "Пользователь {} автоматически забанен навсегда, его рейтинг {} ниже 50.",
            8: "Привет! Я бот-администратор для помощи и контроля за чатом",
            9: "Пользователь {}\nВаш спам-рейтинг: {}\nВаш рейтинг токсичности: {}\n{}",
            10: "Слово {} добавлено в список запрещенных слов (Действие совершил администратор {})",
            11: "Слово {} удалено из списка запрещенных слов (Действие совершил администратор {})",
            12: "Рейтинг пользователя {} сменен на {} (Действие совершил администратор {})",
            13: "Время автоудаления сообщений бота изменено на {} секунд (Действие совершил администратор {})",
            14: "Процесс связывания чатов начат! Ваш токен: '{}'. В чате с администрацией введите команду "
                "<code>/snap_chats {}</code>",
            15: "Процесс связывания чатов успешно завершен!",
            16: "К сожалению, произошла ошибка!\nКод ошибки: {}.",
            17: "Теперь пользователь {} будет отмечаться во время получения тревог!",
            18: "Теперь пользователь {} не будет отмечаться во время получения тревог!",
            19: "Я запомнил 5 человек! (Статус администратора получили пользователи: {})",
            20: "Пользователь {} получил статус администратора!"
        }[sample].format(values)

    def check_message(self):
        """
        Проверяет текст сообщений на наличие
        запрещенных слов
        :return: True - если запрещенное слово обнаружено; False - если запрещенное слово не
        обнаружено
        """
        for word in self.forbidden_words:
            if word in self.message_text:
                return True
        return False

    def insert_message_in_bots_messages_table(self, time_until_exists):
        """
        Вносит текущее сообщение в таблицу BotsMessages
        :param time_until_exists:
        :return:
        """
        BotsMessages.create(
            message_id=self.message_id,
            time_until=time.time() + time_until_exists
        )
