from datetime import datetime, timedelta

from modules.constants.users import OWNER
from modules.db.Tables.BaseModel import db
from modules.db.Tables.TgUserTables import TgUser, UserStatistics


class Statistics:
    def __init__(self, db_user):
        self.db_user: TgUser = db_user
        now: datetime = datetime.now()
        self.messages_per_previous_24_hours: int = self.count_last_days(now - timedelta(days=1))
        self.messages_per_previous_16_days: int = self.count_last_days(now - timedelta(days=16))
        self.messages_per_previous_16_weeks: int = self.count_last_days(now - timedelta(days=112))

    def count_last_days(self, start: datetime):
        days = UserStatistics.select().\
            where(
            (UserStatistics.user == self.db_user) &
            (UserStatistics.time_message_sent_at.between(start, datetime.now()))
        )
        return len(days)


class User(Statistics):
    def __init__(self, db_user: TgUser):
        super().__init__(db_user)

        self.user_id: int = db_user.telegram_id
        self.username: str = db_user.user_name
        self.usernik: str = db_user.user_nik

        self.is_administrator_in_bot: bool = db_user.is_administrator_in_bot
        self.is_owner: bool = self.username in OWNER

        inactive_data: tuple = db.execute(db_user.inactive).fetchone()

        self.inactive_days_counter: int = inactive_data[2]
        self.warned_to_leave: bool = inactive_data[0]
        self.warned_to_leave_valid_until = inactive_data[1]
        self.free_week_days: list = list(map(int, list(str(inactive_data[3]))))

        self.walks_registered_in: list = [walk.walk for walk in db.execute(db_user.walks).fetchall()]

    @property
    def statistics(self):
        return Statistics(self.db_user)

    @property
    def free_days(self):
        return False if self.free_week_days == "null" else list(map(
            lambda d: [
                "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"
            ][d], self.free_week_days
        ))
