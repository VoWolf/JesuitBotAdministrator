from modules.db.Tables.BaseModel import db
from modules.db.Tables.ChatTables import Chat
from modules.db.Tables.WalksTables import Place, Walks


class WalkPlace:
    def __init__(self, place: Place):
        self.city: str = Place.city
        self.metro_thread: str = place.metro_thread
        self.metro_station: str = place.metro_station
        self.location: str = place.location


class Walk(WalkPlace):
    def __init__(self, chat: Chat):
        self.walk: Walks = Walks.get(chat=chat)
        self.time_start = self.walk.time_start
        self.time_end = self.walk.time_end
        self.how_many_people = self.walk.how_many_people
        super().__init__(db.execute(self.walk.place).fetchone())
