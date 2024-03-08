class Decorator:
    def __init__(self):
        pass

    def admin_guard(self, func: callable, *args, **kwargs) -> callable:
        """
        Декоратор для проверки статуса администратора: при True вызывает функцию, при False отправляет
        соответствующее сообщение
        :param func: функция, которая (не)будет вызвана
        :param args: неопределенное количество позиционных аргументов (с ними будет вызвана функция)
        :param kwargs: неопределенное количество именованных аргументов (с ними будет вызвана функция)
        """
        pass

    def creator_guard(self, func: callable, *args, **kwargs) -> callable:
        """
        Декоратор для проверки статуса создателя бота: при True вызывает функцию, при False отправляет
        соответствующее сообщение
        :param func: функция, которая (не)будет вызвана
        :param args: неопределенное количество позиционных аргументов (с ними будет вызвана функция)
        :param kwargs: неопределенное количество именованных аргументов (с ними будет вызвана функция)
        """
        pass

    def reply_guard(self, func: callable, *args, **kwargs) -> callable:
        """
        Декоратор для проверки реплая (использован ли сообщение ответом): при True вызывает функцию, при False
        отправляет соответствующее сообщение
        :param func: функция, которая (не)будет вызвана
        :param args: неопределенное количество позиционных аргументов (с ними будет вызвана функция)
        :param kwargs: неопределенное количество именованных аргументов (с ними будет вызвана функция)
        """
        pass

    def redirect_non_creators_to_vote(
            self,
            func: callable,
            vote_text: str,
            admins_available: bool = True,
            *args,
            **kwargs
    ) -> callable:
        """
        Декоратор для проверки статуса создателя (администратора ели admins_available = True): при True вызывает
        функцию, при False начинает голосование на вызов функции
        :param func: функция, которая (не)будет вызвана
        :param args: неопределенное количество позиционных аргументов (с ними будет вызвана функция)
        :param kwargs: неопределенное количество именованных аргументов (с ними будет вызвана функция)
        :param admins_available: проверка на администрацию
        :param vote_text: Текст будущего голосования
        """
        pass

    def message_exists_guard(self, func: callable, message_id, *args, **kwargs) -> callable:
        pass

    def admins_do_not_banned(self, func: callable, *args, **kwargs) -> callable:
        pass
