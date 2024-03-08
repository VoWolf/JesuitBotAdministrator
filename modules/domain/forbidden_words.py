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

    def extract_and_add_forbidden_word(self) -> None:
        """
        Извлекает из команды новое слово и
        добавляет его к списку запрещенных слов
        """
        word = self.extract_params(
            error_text="Не указано запрещенное слово! (формат ввода данной команды: /add_forbidden_word "
                       "[слово, которое вы хотите добавить])",
            args_count=1,
        )

        if word:
            self.forbidden_word.add_forbidden_word(word=word[0])

    def extract_and_remove_forbidden_word(self) -> None:
        """
        Извлекает из команды новое слово и
        удаляет его из списка запрещенных слов
        """
        word = self.extract_params(
            error_text="К сожалению, не указано запрещенное слово! (формат ввода данной команды: "
                       "/delete_forbidden_word [слово, которое вы хотите удалить])",
            args_count=1,
        )

        if word is None:
            return

        try:
            self.forbidden_word.delete_forbidden_word(word=word)
        except KeyboardInterrupt:
            self.send(
                text=self.msg.return_ready_message_text(
                    sample=16,
                    value_1="К сожалению, введенного вами слово нет в базе данных! (формат ввода данной команды: "
                            "/delete_forbidden_word [слово, которое вы хотите удалить])",
                )
            )
