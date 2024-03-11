from modules.db.database import ActiveRating, TgUserRating


class Ratings:
    def __init__(self, main_rating: TgUserRating, active_rating: ActiveRating):
        self.ratings: TgUserRating = main_rating
        self.active_rating: ActiveRating = active_rating

    def change_main_rating(
            self,
            change_value: float = 0.01,
            set_rating: bool = False
    ) -> tuple:
        """
        Повышает рейтинг заданного пользователя на введенное число
        :param change_value: значение, на которое будет повышен рейтинг
        :param set_rating: прировнять рейтинг к значению change_value
        """
        if set_rating:
            self.ratings.main_rating = change_value
        else:
            self.ratings.main_rating += change_value
        TgUserRating.save(self.ratings)
        return self.check_ratings()

    def count_active_rating(self) -> int:
        """
        Высчитывает значение, которое будет прибавлено к рейтингу активности
        """
        a = (self.ratings.spam_rating + self.ratings.toxic_rating) / 2 * self.active_rating.coefficient
        return int(round(a))

    def change_active_rating(
            self,
            value: int,
            set_rating: bool = False
    ) -> None:
        """
        Изменяет рейтинг активности на value
        :param value: на сколько будет изменен рейтинг активности
        :param set_rating: прировнять рейтинг к значению change_value
        """
        if set_rating:
            self.active_rating.active_in_chat_rating = value
        else:
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
            True if self.ratings.main_rating < 0.00 else False,
            True if self.ratings.main_rating < -5.00 else False,
            True if self.ratings.main_rating < -10.00 else False,
            True if self.ratings.main_rating < -20.00 else False,
        )

        return result_of_check
