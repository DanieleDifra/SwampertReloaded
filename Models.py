from isodate import datetime_isoformat


import datetime as datetime
class Pot:
    def __init__(self, pin):
        self.pin = pin
        lastWater = datetime.datetime.now()