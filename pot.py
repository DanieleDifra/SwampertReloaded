from isodate import datetime_isoformat


class Pot:
    def __init__(self, pin, lastWater):
        self.pin = pin
        self.lastWater = lastWater