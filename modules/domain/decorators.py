import telebot.types

from modules.constants.users import OWNER
from modules.db.get_data import GetData
from modules.domain.add_vote import Vote


def redirect_non_creators_to_vote(
        vote_sample_text: str,
        admins_available: bool = False
):
    def decorator(
        func: callable
    ) -> callable:
        def inner(message):
            user = GetData(message=message)
            user_info = user.full_user_info
            if not user_info["is_owner"] and not user_info["is_administrator_in_bot"]:
                return
            if not admins_available and not user_info["is_administrator_in_bot"]:
                return

            func(message)

        return inner

    return decorator


# def q(test_text):
#     def redirect_to_vote(
#         func
#     ) -> callable:
#         def inner(message):
#             print(test_text)
#             func(message)
#
#         return inner
#     return redirect_to_vote