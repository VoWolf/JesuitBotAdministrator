import time

from modules.command_executors.auto_pilot_executor import autopilot_values
from modules.domain.user import User
from modules.instances.bot_instance import bot as cerberus


def message_handle(message):
    if check_message(message):
        user_in_question = User(
            username=message.from_user.username, user_id=message.from_user.id
        )

        cerberus.delete_message(message.chat.id, message.id)

        if autopilot_values.autopilot_is_on:
            autopilot_values.check_warned_users()
            if user_in_question.username in list(autopilot_values.warned_users.keys()):
                user_in_question.mute(
                    message=message, duration=autopilot_values.mute_time
                )
                cerberus.send_message(
                    message.chat.id,
                    f"Попуск {user_in_question.username} лишен права отправлять сообщения на "
                    f"{autopilot_values.mute_time}  минут за повторное наружение правил (Отдыхай)",
                )
            else:
                cerberus.send_message(
                    message.chat.id,
                    f"{user_in_question.username}, вы нарушили правила! За повторное нарушение в "
                    f"ближайшие {autopilot_values.mute_break_time} минут то вы будете замучены!",
                )
                autopilot_values.warned_users[user_in_question.username] = (
                        time.time() + autopilot_values.mute_break_time
                )
        else:
            cerberus.send_message(
                message.chat.id, f"Сообщение от {user_in_question.username} скрыто"
            )


def check_message(message):
    for el in autopilot_values.FORBIDDEN_WORDS:
        if el in message.text.lower():
            return True
    return False
