from datetime import datetime, timedelta

import telebot.types

from modules.constants.PyMorphy3_analyzer import MORPH
from modules.db.Tables.ChatTables import StopWords
from modules.db.Tables.WalksTables import UserWalks, Walks
from modules.db.TypeObjects.WalkObject import Walk
from modules.db.get_data import GetData
from modules.db.TypeObjects.UserObject import User
from modules.domain.cerberus import Cerberus


class Commands:
    def __init__(self, message: telebot.types.Message):
        self.message: telebot.types.Message = message

        self.CERBERUS: Cerberus = Cerberus(message=message)
        self.GET_DATA: GetData = GetData(message=message)
        self.USER: User = self.GET_DATA.full_user_info

    def start(self):
        """
        Отправляет сообщение с ответом на команду /start
        :return:
        """
        self.CERBERUS.send("Привет! Я буду за вами следить и как могу помогать с чатом.")

    def send_user_statistics(self):
        pass

    def send_free_user_days(self):
        """
        Отправляет все дни, которые пользователь
        пометил как свободные
        :return:
        """
        free_days = "".join(self.USER.free_days)
        self.CERBERUS.send(f"{self.USER.username}, {f'твои свободные дни: {free_days}' if free_days else 'ты не добавил свободных дней, занятой какой'}")

    def ban_user(self):
        data: list[str] = telebot.util.extract_arguments(self.message.text).split()

        try:
            username, reason = data[0], " ".join([data[1]] + data[2:])
        except IndexError:
            return

        user_to_ban = self.GET_DATA.get_by_username(username)
        if not user_to_ban:
            return

        self.CERBERUS.ban(reason=data[1], user_id=user_to_ban.id, username=user_to_ban.user_name)

    def add_stop_word(self):
        """
        Извлекает из текста сообщения слово и во всех формах
        добавляет в таблицу StopWords
        :return:
        """
        word: str = telebot.util.extract_arguments(self.message.text)
        if not word:
            return

        word_parse = MORPH.parse(word.capitalize())[0]
        normal_form = word_parse.normal_form
        db_chat = self.GET_DATA.full_chat_info.db_chat
        base_forms: list[str] = [w.word for w in word_parse.lexeme]
        for w in base_forms:
            StopWords.create(
                word=w,
                word_base_form=normal_form,
                chat=db_chat
            )

        self.CERBERUS.send(f"Слово {normal_form} успешно пополнило список запрещенных слов!")

    def delete_stop_word(self):
        """
        Извлекает из текста сообщения слово и удаляет записи со всеми
        его формами из таблицы StopWords
        :return:
        """
        word: str = telebot.util.extract_arguments(self.message.text)
        if not word:
            return

        normal_form = MORPH.parse(word.capitalize())[0].normal_form
        all_word_records = [rec.id for rec in StopWords.select().where(StopWords.word_base_form == normal_form)]
        for ID in all_word_records:
            StopWords.delete_by_id(ID)

        self.CERBERUS.send(f"Слово {normal_form} удалено из списка запрещенных слов. Развлекайтесь!")

        # word = self.CERBERUS.extract(cut_start=3, params_types=[str])[0]
        # if not word:
        #     return
        # try:
        #     StopWords.delete_by_id(StopWords.get(word=word).id)
        # except IndexError:
        #     self.CERBERUS.error()

    def send_planned_walks(self):
        walks = [w.name + f" | Подробнее: /walk_{w.id}" for w in self.GET_DATA.full_chat_info.walks]
        self.CERBERUS.send(
            text="Все запланированные прогулки:\n" +
                 "\n".join(walks) if walks else "Нет запланированных прогулок!"
        )

    def add_walk(self):   # Проверено
        data: list[str] = telebot.util.extract_arguments(self.message.text).split("::")
        try:
            name, metro_thread, metro_station, location = data[0:4]
            time_start, long = datetime.strptime(data[4], "%d/%m/%Y %H:%M"), int(data[5])
        except (IndexError, ValueError) as e:
            print(e)
            self.CERBERUS.reply("Данные указаны неверно! Формат и пример использования команды: /new_walk_input_help")
            return

        self.GET_DATA.add_walk(
            name=name,
            time_start=time_start,
            time_end=time_start + timedelta(hours=long),
            metro_thread=metro_thread,
            metro_station=metro_station,
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
            "\nДругие прогулки: /walks"
        )

    def get_walk_by_command_id(self, walk_id):
        try:
            walk = Walk(walk_id=int(walk_id))
            print(walk)
        except Exception as e:
            print(e)
            return
        self.CERBERUS.send(
            "Подробная информация о прогулке..."
            f"\nНазвание: {walk.name}"
            f"\nНачало: ~{walk.time_start}"
            f"\nКонец: ~{walk.time_end} (Но это не точно)"
            "\nЛокация------------------------#"
            f"\nВетка метро: {walk.metro_thread}"
            f"\nСтанция метро: {walk.metro_station}"
            f"\nМесто: {walk.location}"
            f"\nЛюдей идет: {walk.people_count}"
            "\nИдут---------------------------#"
            f"\n{'Никто не записан' if not walk.people else ', '.join([p.user_nik for p in walk.people])}")

    def send_help_info_walks(self):
        self.CERBERUS.send(
            "<b>Все, что вам нужно знать о механике с прогулками:</b>"
            "\n\n<b>#Как создать--------------------#</b>"
            "\nИспользуйте команду /add_walk. После нее укажите: [название прогулки]::[ветка метро]::[станция метро]::"
            "[локация]::[время сбора]::[длительность]. Формат времени: дд/мм/гггг чч:мин."
            "\n\n<b>Пример:</b> '/add_walk Компаш в авик :: БКЛ :: ЦСКА :: тц Авиапарк :: 24/2/2024 13:00 :: 5'"
            "\n\nБот автоматически добавит вас в список тех, кто идет и отправит опрос с соответствующим вопросом. "
            "Каждый, кто проголосует за вариант 'иду' будет добавлен к прогулке. Позвать всех, кто записался можно "
            "написав @[имя прогулки, регистр неважен] (Для примера: '@Компаш в авик')"
            "\n\n<b>#Команды------------------------#</b>"
            "\n/go [имя прогулки] - Записаться на прогулку"
            "\n/leave [имя прогулки] - отписаться от прогулки"
            "\n/delete_walk [имя прогулки] - Удалить прогулку"
            "\n/change_walk [параметр*][имя прогулки] - поменять данные о прогулке"
            "\n/walks - список всех прогулок, открытых в этом чате."
            "\nКогда время совпадет со временем конца прогулки, та будет автоматически удалена"
            "\n\n*Параметры: "
            "\nимя - название прогулки"
            "\nветка - ветка метро"
            "\nстанция - станция метро"
            "\nлока - локация"
            "\nстарт - время сбора",
            parse="HTML"
        )

    @staticmethod
    def check_calls(text):
        text = text.lower()
        match text:
            case _ if "понедельник" in text:
                pass
            case _ if "вторник" in text:
                pass
            case _ if "среда" in text:
                pass
            case _ if "четверг" in text:
                pass
            case _ if "пятница" in text:
                pass
            case _ if "суббота" in text:
                pass
            case _ if "воскресенье" in text:
                pass

    def delete_current_user_from_walk(self):
        try:
            UserWalks.delete_by_id(
                UserWalks.get(user=self.GET_DATA.full_user_info.db_user).id
            )
        except Exception as e:
            print(e)
            return

        self.CERBERUS.send(f"Вы удалены из прогулки {self.message.text[1:]}")

    def delete_walk(self):
        try:
            name = telebot.util.extract_arguments(self.message.text)
            Walks.delete_by_id(
                Walks.select().where((Walks.chat == self.GET_DATA.full_chat_info.db_chat) & (Walks.name == name)).id
            )
        except Exception as e:
            print(e)
            return

        self.CERBERUS.reply("Прогулка удалена!")

    def add_current_user_from_walk(self):
        try:
            UserWalks.create(
                user=self.GET_DATA.full_user_info.db_user,
                walk=Walks.get(name=telebot.util.extract_arguments(self.message.text))
            )
        except Exception as e:
            print(e)
            return

        self.CERBERUS.reply("Вы записаны")
