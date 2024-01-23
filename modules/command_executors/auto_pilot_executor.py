from modules.command_executors.admin_check_executor import check_admin
from modules.instances.bot_instance import bot as tserberus
import time


class AutoPilotData:
    """Helps with storage of values for autopilot"""
    def __init__(self, mute_time, mute_break_time, auto_is_on):
        self.mute_time: int = mute_time
        self.mute_break_time: int = mute_break_time
        self.autopilot_is_on: bool = auto_is_on
        print(self.autopilot_is_on)
        self.warned_users: dict = {}
        self.forbidden_words = [
            "сука", "пидор", "долбоеб", "еблан", "шлюх", "хуесос", "пидар", "немощь", "тупой", "тупая",
            "далбаеб", "клоун", "даун", "аутист", "птеух", "дебил", "дибил", "шавка", "шафка", "гнида",
            "лох", "лохушка", "мразь", "мудак", "нахал", "паскуда", "поскуда", "проститутка", "сволочь",
            "тварь", "ублюдок", "выродок", "уебан", "писька", "пэска", "гандон", "бомж", "глупый",
            "урод", "пиздюк", "хуила", "хуйло", "гей в панам", "пидрила", "хуило", "уебище", "шалав", "обезьян"
        ]

    @staticmethod
    def check_warned_users():
        for el in list(autopilot_values.warned_users.keys()):
            if autopilot_values.warned_users[el] < time.time():
                del autopilot_values.warned_users[el]


autopilot_values = AutoPilotData(
                mute_time=0,
                mute_break_time=0,
                auto_is_on=False
)


def auto_pilot_on(message):
    """Turns on auto mute"""
    global autopilot_values
    if check_admin(message):
        try:
            autopilot_values = AutoPilotData(
                mute_time=int(message.text.split()[1]),
                mute_break_time=int(message.text.split()[2]),
                auto_is_on=True
            )
        except IndexError:
            tserberus.reply_to(message, "Тебе нужно указать время автомута и время автоудаления после предупреждения"
                                        " через пробел от команды!")
            return
        except ValueError:
            tserberus.reply_to(message, "Тебе нужно указать время автомута и время автоудаления после предупреждения "
                                        "через пробел от команды. \n*Для дураков: ЭТО ЧИСЛА!")
            return
        tserberus.reply_to(
            message, f"Автомут включен!\nСведения:\nВремя между предупреждениями: {autopilot_values.mute_break_time} "
            f"минут\nВремя автомута: {autopilot_values.mute_time} минут"
        )
    else:
        tserberus.reply_to(message, "Ты не можешь этого сделать!)")


def auto_pilot_off(message):
    """Turns off auto mute"""
    global autopilot_values
    if check_admin(message):
        autopilot_values.autopilot_is_on = False
        tserberus.reply_to(message, "Автомут отключен!")
    else:
        tserberus.reply_to(message, "Ты не можешь этого сделать!)")