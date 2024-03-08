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

    def vote_for(self):
        """
        Добавляет 1 голос за
        :return:
        """
        self.votes_for += 1
        return self.check_votes()

    def vote_against(self):
        """
        Добавляет 1 голос против
        :return:
        """
        self.votes_against += 1

    def vote_update(self, bot):
        """
        Обновляет сообщение с голосованием
        :param bot:
        :return:
        """
        pass

    def check_votes(self):
        """
        Проверяет не проголосовало ли за больше половины группы
        :return:
        """
        if self.votes_for >= self.votes_need_to_pass:
            return True
        return False
