"""Создает класс ForbiddenWords"""

from modules.db.database import ForbiddenWord


class ForbiddenWords:
    """
    Отвечает за работу с таблицей ForbiddenWords
    """

    def __init__(self):
        self.forbidden_words = [value.word for value in ForbiddenWord.select()]

    @staticmethod
    def add_forbidden_word(word: str) -> None:
        """
        Добавляет слово из позиционного аргумента word
        в таблицу ForbiddenWords
        :param word: Текст слова, которое мы хотим добавить в запрещенные
        """
        ForbiddenWord.create(word=word)

    @staticmethod
    def delete_forbidden_word(word: str) -> None:
        """
        Удаляет слово из позиционного аргумента word
        из таблицы ForbiddenWords
        :param word: Текст слова, которое мы хотим удалить
        """
        try:
            ForbiddenWord.delete_by_id(ForbiddenWord.get(word=word).id)
        except IndexError:
            raise KeyboardInterrupt("Введено слово, которое отсутствует в базе данных")

    def refresh_forbidden_words(self) -> None:
        """
        Обновляет значение forbidden_words
        """
        self.forbidden_words = [value.word for value in ForbiddenWord.select()]

    def return_forbidden_words(self) -> list:
        """
        Возвращает список запрещенных слов
        """
        return self.forbidden_words
