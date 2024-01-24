from modules.instances.bot_instance import bot as tserberus
from modules.command_executors.admin_check_executor import check_admin
from modules.work_with_user_stuff.user_klass import UserData


def mute_user(message):
    if message.reply_to_message:
        user = UserData(
            username=message.reply_to_message.from_user.username,
            user_id=message.reply_to_message.from_user.id
        )
        if check_admin(message):
            duration = 5
            try:
                args = message.text.split()[1]
            except IndexError:
                args = None
            if args:
                try:
                    duration = int(args)
                except ValueError:
                    tserberus.reply_to(message, "Неправильный формат времени!")
                    return
                if duration < 1:
                    tserberus.reply_to(message, "Минимальное время 1 минута!")
                    return
                if duration > 1440:
                    tserberus.reply_to(message, "Максимальное время 24 часа (1440 минут)!")
                    return
            if message.reply_to_message.from_user.username in ["innorif2099", "IezyitskyGuardBot"]:
                tserberus.reply_to(message, "К сожалению, бога забанить невозможно!")
                return
            user.do_user_strict(message=message, duration=duration)
            tserberus.reply_to(
                message, f"Пользователь {user.username} замучен на {duration} минут."
            )
        else:
            tserberus.reply_to(message, "Ты не можешь этого сделать!)")
    else:
        tserberus.reply_to(message, "Эту команду надо использовать ответом на сообщение!")


def unmute_user(message):
    if message.reply_to_message:
        user = UserData(
            username=message.reply_to_message.from_user.username,
            user_id=message.reply_to_message.from_user.id
        )
        user.do_user_free(message)
        tserberus.reply_to(message, f"{user.username} освобожден!")
    else:
        tserberus.reply_to(message, "Эту команду надо использовать ответом на сообщение!")
