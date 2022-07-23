import datetime as datetime
class Pot:
    def __init__(self, pin):
        self.pin = pin
        self.lastWater = datetime.datetime.now()