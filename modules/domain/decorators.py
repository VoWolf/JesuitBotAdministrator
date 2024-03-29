import telebot.types

from modules.db.get_data import GetData
from modules.domain.cerberus import Cerberus


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
