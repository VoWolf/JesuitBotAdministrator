from modules.db.Tables.BaseModel import db
from modules.db.Tables.ChatTables import Chat
from modules.db.Tables.WalksTables import Place, Walks


class WalkPlace:
    def __init__(self, place: Place):
        self.metro_thread: str = place[2]
        self.metro_station: str = place[3]
        self.location: str = place[4]


class Walk(WalkPlace):
    def __init__(self, chat: Chat):
        self.walk: Walks = Walks.get(chat=chat)
        self.name = self.walk.name
        self.time_start = self.walk.time_start
        self.time_end = self.walk.time_end
        self.people = self.walk.people
        super().__init__(db.execute(self.walk.place).fetchone())
