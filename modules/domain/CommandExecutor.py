from datetime import datetime, timedelta

import telebot.types
from telebot.formatting import hlink

from modules.constants.PyMorphy3_analyzer import MORPH
from modules.db.Tables.BaseModel import db
from modules.db.Tables.ChatTables import StopWords
from modules.db.Tables.TgUserTables import InactiveData, TgUser
from modules.db.Tables.WalksTables import UserWalks, Walks, Place
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
        free_days = ", ".join(self.USER.free_days)
        self.CERBERUS.send(f"{self.USER.username}, {f'твои свободные дни: ' + free_days if free_days else 'ты не добавил свободных дней, занятой какой'}")

    def ban_user(self):
        data: list[str] = telebot.util.extract_arguments(self.message.text).split()

        try:
            username, reason = data[0], " ".join([data[1]] + data[2:])
        except IndexError:
            return

        user_to_ban = self.GET_DATA.get_by_username(username[1:])
        if not user_to_ban:
            return

        self.CERBERUS.ban(reason=" ".join(data[1:]), user_id=user_to_ban.telegram_id, username=user_to_ban.user_name)

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
        data: list[str] = telebot.util.extract_arguments(self.message.text).split("|")
        data = list(map(str.strip, data))
        try:
            name, metro_thread, metro_station, location = data[0:4]
            time_start, long = datetime.strptime(data[4], "%d/%m/%Y %H:%M"), int(data[5])
        except (IndexError, ValueError) as e:
            print(e)
            self.CERBERUS.reply("Данные указаны неверно! Формат и пример использования команды: /new_walk_input_help")
            return

        self.GET_DATA.add_walk(
            name=name.lower(),
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
            "\nлока - локация"
            "\nстарт - время сбора",
            parse="HTML"
        )

    def delete_current_user_from_walk(self):
        try:
            UserWalks.delete_by_id(
                UserWalks.get(user=self.GET_DATA.full_user_info.db_user).id
            )
            walk: Walks = Walks.get(name=telebot.util.extract_arguments(self.message.text))
            walk.people_count -= 1
            Walks.save(walk)
        except Exception as e:
            print(e)
            return

        self.CERBERUS.send(f"Вы удалены из прогулки {walk.name}")

    def delete_walk(self):
        try:
            name = telebot.util.extract_arguments(self.message.text).lower()
            walk = Walks.select().where((Walks.chat == self.GET_DATA.full_chat_info.db_chat) & (Walks.name == name))[0]
            db.execute(UserWalks.delete().where(UserWalks.walk == walk))
            db.execute(Place.delete().where(Place.walk == walk))
            Walks.delete_by_id(walk.id)
        except Exception as e:
            print(e)
            return

        self.CERBERUS.reply("Прогулка удалена!")

    def add_current_user_to_walk(self):
        try:
            try:
                UserWalks.get(user=self.GET_DATA.full_user_info.db_user)
                self.CERBERUS.reply("Вы уже записаны на эту прогулку!")
                return
            except Exception as e:
                print(e)
                UserWalks.create(
                    user=self.GET_DATA.full_user_info.db_user,
                    walk=Walks.get(name=telebot.util.extract_arguments(self.message.text).lower())
                )
                walk: Walks = Walks.get(name=telebot.util.extract_arguments(self.message.text))
                walk.people_count += 1
                Walks.save(walk)
        except Exception as e:
            print(e)
            return

        self.CERBERUS.reply("Вы записаны")

    def change_walk(self):
        data = telebot.util.extract_arguments(self.message.text)
        try:
            name, param, new_value = data[0], data[1], data[2] + data[3:]
            if param == "старт":
                new_value = datetime.strptime(new_value, "%d/%m/%Y %H:%M")
            walk: Walks = Walks.get(chat=self.GET_DATA.full_chat_info.db_chat)
        except (IndexError, ValueError):
            self.CERBERUS.reply("Вы вызвали команду неправильно! Пример использования: /change_walk_data_help")
            return

        match param:
            case "имя":
                walk.name = new_value
                Walks.save(walk)
            case "лока":
                walk.place[0].location = new_value
                Walks.save(walk)
            case "старт":
                walk.time_start = new_value
                Walks.save(walk)

    @staticmethod
    def check_input_format_week_days(value: str) -> bool:
        try:
            return value.isalnum() and 0 <= int(value) <= 6
        except ValueError:
            return False

    def add_free_day(self):
        week_day = telebot.util.extract_arguments(self.message.text)
        if not self.check_input_format_week_days(telebot.util.extract_arguments(self.message.text)):
            self.CERBERUS.reply(
                "Ты указал несуществующий день недели! Необходимо указать число 0 - 6 "
                "(0 - понедельник, 6 - воскресенье)"
            )
            return

        data: InactiveData = InactiveData.get(user=self.GET_DATA.full_user_info.db_user)
        if data.free_days != "null":
            data.free_days += week_day
        else:
            data.free_days = week_day
        InactiveData.save(data)

        self.CERBERUS.send("Список ваших свободных дней изменен!")

    def del_free_day(self):
        week_day = telebot.util.extract_arguments(self.message.text)
        if not self.check_input_format_week_days(telebot.util.extract_arguments(self.message.text)):
            self.CERBERUS.reply(
                "Ты указал несуществующий день недели! Необходимо указать число 0 - 6 "
                "(0 - понедельник, 6 - воскресенье)"
            )
            return

        data: InactiveData = InactiveData.get(user=self.GET_DATA.full_user_info.db_user)
        free = list(data.free_days)
        try:
            del free[free.index(week_day)]
        except ValueError:
            return

        data.free_days = "".join(free) if not "".join(free) else "null"
        InactiveData.save(data)

        self.CERBERUS.send("Список ваших свободных дней изменен!")

    def mute_user(self):
        if self.message.reply_to_message:
            self.CERBERUS.mute(TgUser.get(telegram_id=self.message.reply_to_message.from_user.id), is_reply=True)
        else:
            self.CERBERUS.mute(self.GET_DATA.get_by_username(telebot.util.extract_arguments(self.message.text).split()[0][1:]), is_reply=False)

    def unmute_user(self):
        if self.message.reply_to_message:
            self.CERBERUS.unmute(TgUser.get(telegram_id=self.message.reply_to_message.from_user.id))
        else:
            self.CERBERUS.unmute(self.GET_DATA.get_by_username(telebot.util.extract_arguments(self.message.text).split()[0][1:]))

    def check_calls(self, text):
        text = text.lower()
        match text:
            case _ if text in ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]:
                week_day_num = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота",
                                "воскресенье"].index(text)
                users_to_tag = InactiveData.select(InactiveData.user).where(InactiveData.free_days.in_([str(week_day_num)]))
            case ["админы", "admins"]:
                users_to_tag = TgUser.select(TgUser.user_name).where(TgUser.is_administrator_in_bot is True)
            case _:
                walk = Walks.select().where((Walks.chat == self.GET_DATA.full_chat_info.db_chat) & (Walks.name == text))
                if not walk:
                    self.CERBERUS.reply("Таково варианта призыва нема!")
                    return
                users_to_tag = [user for user in walk[0].users]

        try:
            users_to_tag = [user.user.user_name for user in users_to_tag]
            result_call = list(map(lambda user: hlink("|", f"t.me/{user}"), users_to_tag))

            self.CERBERUS.send(f"Зову...\n{''.join(result_call) if result_call else 'никого нету'}", parse="HTML")
        except Exception as e:
            print(e)
            self.CERBERUS.reply("Не могу позвать:(")
