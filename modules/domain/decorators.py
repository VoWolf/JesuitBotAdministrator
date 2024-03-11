import telebot.types

from modules.constants.users import OWNER
from modules.db.database import TgUser
from modules.domain.user import User


def creator_guard(message: telebot.types.Message) -> callable:
    """
    Декоратор для проверки статуса администратора: при True вызывает функцию, при False отправляет
    соответствующее сообщение
    """

    def decorator(func: callable):
        def inner(*args, **kwargs):
            if message.from_user.username not in OWNER:
                return
            func(*args, **kwargs)

        return inner

    return decorator


def admin_guard(message) -> callable:
    """
    Декоратор для проверки статуса создателя бота: при True вызывает функцию, при False отправляет
    соответствующее сообщение
    """

    def decorator(func: callable):
        def inner(*args, **kwargs):
            try:
                admin_stat = TgUser.get(telegram_id=message.from_user.id)
            except Exception as e:
                return e

            if not admin_stat:
                return
            func(*args, **kwargs)

        return inner

    return decorator


def reply_guard(message: telebot.types.Message) -> callable:
    """
    Декоратор для проверки реплая (использован ли сообщение ответом): при True вызывает функцию, при False
    отправляет соответствующее сообщение
    """

    def decorator(func: callable):
        def inner(*args, **kwargs):
            if not message.reply_to_message:
                return
            func(*args, **kwargs)

        return inner

    return decorator


def redirect_non_creators_to_vote(
        vote_text: str,
        admins_available: bool = True,
) -> callable:
    """
    Декоратор для проверки статуса создателя (администратора ели admins_available = True): при True вызывает
    функцию, при False начинает голосование на вызов функции
    :param admins_available: проверка на администрацию
    :param vote_text: Текст будущего голосования
    """
    pass


def admins_do_not_banned(user: User) -> callable:
    """
    Проверяет, является ли пользователь администратором. При False выполняет функцию
    """

    def decorator(func: callable):
        def inner(*args, **kwargs):
            if user.is_admin:
                return
            func(*args, **kwargs)

        return inner

    return decorator
