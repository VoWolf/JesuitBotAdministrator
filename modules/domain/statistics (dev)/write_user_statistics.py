import _io
import datetime
import os

from modules.constants.PyMorphy3_analyzer import MORPH
from modules.db.TypeObjects.ChatObject import ChatInfo
from modules.db.TypeObjects.UserObject import User
from modules.db.get_data import GetData
from modules.domain.statistics._Schedule_class import MakeStata


class WriteUserStatisticsFile:
    def __init__(self, get_data: GetData):
        self.GET_DATA = get_data
        self.user: User = self.GET_DATA.full_user_info
        self.current_chat: ChatInfo = self.GET_DATA.full_chat_info

        self.file_name: str | None = None
        self.file_way: str | None = None
        self.file: _io.TextIOWrapper | None = None

    def create_folders(self):
        if not os.path.exists("text_statistics"):
            os.mkdir("text_statistics")
        if not os.path.exists(f"text_statistics/{self.current_chat.chat_id}"):
            os.mkdir(f"text_statistics/{self.current_chat.chat_id}")
        self.file_way = f"text_statistics/{self.current_chat.chat_id}"

    def create_file(self):
        self.file_name = f"{self.file_way}/@user_{self.user.username}.txt"
        self.file = open(self.file_name, "w")

    def delete_file(self):
        os.remove(self.file_name)

    def write_info_about_active(self):
        self.file.write(f"СТАТИСТИКА ПОЛЬЗОВАТЕЛЯ {self.user.username} ({self.user.usernik}):\n\n")

        stat = [
            (self.user.statistics.messages_per_previous_24_hours, "час"),
            (self.user.statistics.messages_per_previous_16_days, "день"),
            (self.user.statistics.messages_per_previous_16_weeks, "неделя")
        ]

        for el in stat:
            graph = MakeStata(el[0])
            graph.count_sizes()
            TIME_CUT = MORPH.parse(el[1])[0].make_agree_with_number(graph.horizontal_size).word
            LAST = MORPH.parse('последний')[0].make_agree_with_number(graph.horizontal_size).word
            self.file.write(
                f"Изменение количества отправляемых в чат сообщений за {LAST} {graph.horizontal_size} {TIME_CUT}:\n{graph.build_graph()}\n"
            )

        self.file.write("\n")

    def write_info_about_user(self):
        walks_count = len(self.user.walks_registered_in)
        WALK = MORPH.parse("прогулка")[0].make_agree_with_number(walks_count).word
        walks = ["\n".join(["* {}".format(w[0]) for w in self.user.walks_registered_in])]
        self.file.write(f"""
        Имя пользователя: @{self.user.username}
        ID пользователя: {self.user.user_id}
        Ник пользователя: {self.user.usernik}
        #-------------------------------#
        Ранг: {'администратор' if self.user.is_administrator_in_bot else 'обычный участник'}
        Дни, помеченные как свободные: {''.join(self.user.free_days)}
        Предупредил администрацию о возможном уходе: {'да' if self.user.warned_to_leave else 'нет'}
        {f'Время до которого предупреждение действительно: {self.user.warned_to_leave_valid_until}' if self.user.warned_to_leave else ''}
        #-------------------------------#
        Записан на {walks_count} {WALK}:
        {walks}
        #-------------------------------#
        @TserberusGuard, от {datetime.datetime.now()}.
        """)
        self.file.close()

    def self_start(self):
        self.create_folders()
        self.create_file()

        self.write_info_about_active()
        self.write_info_about_user()
