from modules.db.database import ActiveRating, TgUserRating


class Ratings:
    def __init__(self, ratings, active_rating):
        self.ratings = ratings
        self.active_rating = active_rating

    def change_rating(
            self,
            change_value: float = 0.01,
            change_spam_rating: bool = True,
            change_toxic_rating: bool = True,
    ) -> tuple:
        """
        Повышает рейтинг заданного пользователя на
        введенное число
        :param change_value: значение, на которое будет повышен рейтинг
        :param change_spam_rating: изменить значение спам рейтинга или нет
        :param change_toxic_rating: изменить значения рейтинга токсичности или нет
        """
        if change_toxic_rating:
            self.ratings.toxic_rating += change_value
        if change_spam_rating:
            self.ratings.spam_rating += change_value
        TgUserRating.save(self.ratings)
        return self.check_ratings()

    def count_change_active_rating(self) -> int:
        """
        Высчитывает значение, которое будет прибавлено к рейтингу активности
        """
        a = (self.ratings.spam_rating + self.ratings.toxic_rating) / 2 * self.active_rating.coefficient
        return int(round(a))

    def change_active_rating(self, value: int) -> None:
        """
        Изменяет рейтинг активности на value
        :param value: на сколько будет изменен рейтинг активности
        """
        self.active_rating.active_in_chat_rating += value
        ActiveRating.save(self.active_rating)

    def check_ratings(self) -> tuple:
        """
        Проверяет все три рейтинга. Расшифровка кортежа, который он вернет:
        False - рейтинг в норме
        True - рейтинг опустился ниже порогового значения
        ([спам рейтинг], [рейтинг токсичности])
        """
        result_of_check = (
            True if self.ratings.spam_rating < 0.00 else False,
            True if self.ratings.toxic_rating < 0.00 else False,
        )

        return result_of_check
