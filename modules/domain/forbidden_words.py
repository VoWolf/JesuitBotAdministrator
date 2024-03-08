"""Создает класс ForbiddenWords"""

from modules.db.database import ForbiddenWord


class ForbiddenWords:
    """
    Отвечает за работу с таблицей ForbiddenWords
    """

    def __init__(self):
        self.forbidden_words = [value.word for value in ForbiddenWord.select()]

    @staticmethod
    def add_forbidden_word(word: str):
        """
        Добавляет слово из позиционного аргумента word
        в таблицу ForbiddenWords
        :param word: Текст слова, которое мы хотим добавить в запрещенные

        :returns: None
        """
        ForbiddenWord.create(word=word)

    @staticmethod
    def delete_forbidden_word(word: str):
        """
        Удаляет слово из позиционного аргумента word
        из таблицы ForbiddenWords
        :param word: Текст слова, которое мы хотим удалить
        :returns: None
        """
        try:
            ForbiddenWord.delete_by_id(ForbiddenWord.get(word=word).id)
        except IndexError:
            raise KeyboardInterrupt("Введено слово, которое отсутствует в базе данных")

    def refresh_forbidden_words(self):
        """
        Обновляет значение forbidden_words
        :returns: None
        """
        self.forbidden_words = [value.word for value in ForbiddenWord.select()]

    def return_forbidden_words(self):
        """
        Возвращает список запрещенных слов
        :returns list:
        """
        return self.forbidden_words
