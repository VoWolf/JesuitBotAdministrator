from datetime import datetime, timedelta

from modules.constants.users import OWNER
from modules.db.Tables.BaseModel import db
from modules.db.Tables.TgUserTables import TgUser, UserStatistics


class Statistics:
    def __init__(self, db_user):
        self.db_user = db_user
        self.messages_per_previous_24_hours = self.count_last_days(d=1)
        self.messages_per_previous_16_days = self.count_last_days(d=16)
        self.messages_per_previous_16_weeks = self.count_last_days(d=112)

    def count_last_days(self, d):
        days = []
        for i in range(d):
            time_start = (datetime.now() - timedelta(days=i))
            time_end = (datetime.now() - timedelta(days=i-1))
            days.append(UserStatistics.select().where(
                time_start <= UserStatistics.time_message_sent_at <= time_end and UserStatistics.user == self.db_user
            ).fetchall())
        return list(map(lambda day: len(day), days))


class User(Statistics):
    def __init__(self, db_user: TgUser):
        super().__init__(db_user)
        self.db_user = db_user

        self.user_id = db_user.telegram_id
        self.username = db_user.user_name
        self.usernik = db_user.user_nik

        self.is_administrator_in_bot = db_user.is_administrator_in_bot
        self.is_owner = self.username in OWNER

        inactive_data = db.execute(db_user.inactive).fetchone()[:-1]

        self.inactive_days_counter: int = inactive_data[2]
        self.warned_to_leave: bool = inactive_data[0]
        self.warned_to_leave_valid_until = inactive_data[1]
        self.free_week_days: list = list(map(int, list(inactive_data[3])))

        self.walks_registered_in: list = [walk.walk for walk in db.execute(db_user.walks).fetchall()]

    @property
    def statistics(self):
        return Statistics(self.db_user)

    @property
    def free_days(self):
        return list(map(
            lambda d: [
                "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"
            ][d], self.free_week_days
        ))
