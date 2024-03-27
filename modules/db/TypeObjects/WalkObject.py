from modules.db.Tables.BaseModel import db
from modules.db.Tables.ChatTables import Chat
from modules.db.Tables.TgUserTables import TgUser
from modules.db.Tables.WalksTables import Place, Walks


class WalkPlace:
    def __init__(self, place: Place):
        self.metro_thread: str = place[2]
        self.metro_station: str = place[3]
        self.location: str = place[4]


class Walk(WalkPlace):
    def __init__(self, chat: Chat | None = None, name: str | None = None, walk_id: int | None = None):
        if walk_id:
            self.walk: Walks = Walks.get_by_id(walk_id)
        else:
            self.walk: Walks = Walks.select().where((Walks.chat == chat) & (Walks.name == name))

        self.name = self.walk.name
        self.time_start = self.walk.time_start
        self.time_end = self.walk.time_end
        self.people_count = self.walk.people_count
        self.people: list[TgUser] = [p for p in self.walk.users]
        super().__init__(db.execute(self.walk.place).fetchone())
