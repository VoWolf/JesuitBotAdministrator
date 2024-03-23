from modules.constants.users import OWNER
from modules.db.database import TgUser, db


class Statistics:
    def __init__(
            self,
            per_day: int,
            per_week: int,
            per_mouth: int,
            per_all_time: int
    ):
        self.per_day: int = per_day
        self.per_week: int = per_week
        self.per_mouth: int = per_mouth
        self.per_all_time: int = per_all_time


class User:
    def __init__(
            self,
            user_id: int,
            username: str,
            usernik: str,
            db_user: TgUser
    ):
        self.user_id = user_id,
        self.username = username,
        self.usernik = usernik,
        self.is_administrator_in_bot = db_user.is_administrator_in_bot,
        self.is_owner = self.username in OWNER,
        self.stata = Statistics(
            per_day=db_user.statistics.messages_per_day,
            per_week=db_user.statistics.messages_per_week,
            per_mouth=0,
            per_all_time=db_user.statistics.messages_per_all_time
        )
        self.chats_in = db.execute(db_user.chats).fetchall()

    @property
    def statistics(self):
        return {
            "day": self.stata.per_day,
            "week": self.stata.per_week,
            "mouth": self.stata.per_mouth,
            "all_time": self.stata.per_all_time
        }

    @property
    def names(self):
        return {
            "name": self.username,
            "nik": self.usernik
        }

    @property
    def status(self):
        return {
            "admin": self.is_administrator_in_bot,
            "owner": self.is_owner
        }
