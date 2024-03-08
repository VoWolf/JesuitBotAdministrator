"""Занимается процессом голосования за добавление новых участников"""


class Vote:
    """
    Контролирует процесс голосования
    """
    def __init__(self, text, message_id, votes_to_pass):
        self.votes_for = 0
        self.votes_against = 0
        self.text = text
        self.message_id = message_id
        self.votes_need_to_pass = votes_to_pass

    def vote_for(self) -> bool:
        """
        Добавляет 1 голос за
        """
        self.votes_for += 1
        return self.check_votes()

    def vote_against(self) -> None:
        """
        Добавляет 1 голос против
        """
        self.votes_against += 1

    def vote_update(self, bot: object) -> None:
        """
        Обновляет сообщение с голосованием
        :param bot: объект класса telebot
        """
        pass

    def check_votes(self) -> bool:
        """
        Проверяет не проголосовало ли за больше половины группы
        """
        if self.votes_for >= self.votes_need_to_pass:
            return True
        return False
