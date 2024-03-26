import datetime

import telebot.types

from modules.db.Tables.ChatTables import StopWords
from modules.db.get_data import GetData
from modules.db.TypeObjects.UserObject import User
from modules.domain.cerberus import Cerberus


class Commands:
    def __init__(self, message: telebot.types.Message):
        self.message: telebot.types.Message = message

        self.CERBERUS: Cerberus = Cerberus(message=message)
        self.GET_DATA: GetData = GetData(message=message)
        self.USER: User = self.GET_DATA.full_user_info

    def start(self):  # Проверено
        """
        Отправляет сообщение с ответом на команду /start
        :return:
        """
        self.CERBERUS.send("Привет! Я буду за вами следить и как могу помогать с чатом.")

    def send_user_statistics(self):  # НЕ проверено
        pass

    def send_free_user_days(self):  # Проверено
        """
        Отправляет все дни, которые пользователь
        пометил как свободные
        :return:
        """
        free_days = self.USER.free_days
        self.CERBERUS.send(
            f"{self.USER.username}, твои свободные дни: " +
            f"{', '.join(free_days) if free_days else 'Ты не добавил свободных дней, занятой какой'}"
        )

    def ban_user(self):  # НЕ проверено
        data = self.CERBERUS.extract(cut_start=2, params_types=[str, str])
        user_to_ban = self.GET_DATA.get_by_username(data[0])
        if not user_to_ban or not data:
            return
        self.CERBERUS.ban(reason=data[1], user_id=user_to_ban.id, username=user_to_ban.user_name)

    def add_stop_word(self):  # НЕ проверено
        word = self.CERBERUS.extract(cut_start=3, params_types=[str])[0]
        if not word:
            return
        StopWords.create(
            word=word,
            chat=self.GET_DATA.full_chat_info.db_chat.db_chat
        )

    def delete_stop_word(self):   # НЕ проверено
        word = self.CERBERUS.extract(cut_start=3, params_types=[str])[0]
        if not word:
            return
        try:
            StopWords.delete_by_id(StopWords.get(word=word).id)
        except IndexError:
            self.CERBERUS.error()

    def send_planned_walks(self):  # НЕ проверено
        walks = self.GET_DATA.full_chat_info.db_chat.walks
        self.CERBERUS.send(text="Все запланированные прогулки:\n" + "\n".join(walks))

    def add_walk(self):   # НЕ проверено
        try:
            name, metro_thread, metro_station, location, time_start, time_end = self.CERBERUS.extract(
                cut_start=1, params_types=[str, str, str, str, str, str]
            )
            time_start, time_end = \
                datetime.datetime.strptime(time_start, "%d/%m/%Y"), datetime.datetime.strptime(time_end, "%d/%m/%Y")
        except Exception as e:
            print(e)
            return

        self.GET_DATA.add_walk(
            name=name, time_start=time_start, time_end=time_end, metro_thread=metro_thread, metro_station=metro_station,
            location=location
        )

        self.CERBERUS.reply(
            "Прогулка создана успешно!"
            "\nЗаписаться: /go [имя прогулки]"
            "\nОтписаться: /leave [имя прогулки]"
            "\nУдалить: /delete_walk [имя прогулки]"
            "\nИзменить: /change_walk [параметр][имя прогулки]"
            "\nПозвать всех, кто идет: @[имя прогулки]"
            "\nПодробнее: /walks_info"
        )
