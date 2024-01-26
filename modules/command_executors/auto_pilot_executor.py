import time


class AutoPilotData:
    """Helps with storage of values for autopilot"""

    def __init__(self, mute_time, mute_break_time, auto_is_on):
        self.mute_time: int = mute_time
        self.mute_break_time: int = mute_break_time
        self.autopilot_is_on: bool = auto_is_on
        self.warned_users: dict = {}

    @staticmethod
    def check_warned_users():
        for el in list(autopilot_values.warned_users.keys()):
            if autopilot_values.warned_users[el] < time.time():
                del autopilot_values.warned_users[el]


autopilot_values = AutoPilotData(mute_time=0, mute_break_time=0, auto_is_on=False)
