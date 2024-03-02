"""Создает класс ForbiddenWords"""

from modules.db.database import ForbiddenWord


class ForbiddenWords:
    """
    Отвечает за работу с таблицей ForbiddenWords
    """
    def __init__(self):
        self.forbidden_words = [value.word for value in ForbiddenWord.select()]

    @staticmethod
    def add_forbidden_words(word):
        """
        Добавляет слово из позиционного аргумента word
        в таблицу ForbiddenWords
        :param word:
        :return:
        """
        ForbiddenWord.create(
            word=word
        )

    @staticmethod
    def delete_forbidden_word(word):
        """
        Удаляет слово из позиционного аргумента word
        из таблицы ForbiddenWords
        :param word:
        :return:
        """
        try:
            ForbiddenWord.delete_by_id(ForbiddenWord.get(word=word).id)
        except IndexError:
            raise IndexError("Введено слово, которое отсутствует в базе данных")

    def refresh_forbidden_words(self):
        """
        Обновляет значение forbidden_words
        :return:
        """
        self.forbidden_words = [value.word for value in ForbiddenWord.select()]

    def return_forbidden_words(self):
        """
        Возвращает список с запрещенными словами
        :return list:
        """
        return self.forbidden_words
