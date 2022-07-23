import datetime as datetime
import time

class Pot:
    def __init__(self,pin):
        self.pin = pin
        self.last = datetime.datetime.now

pot1 = Pot(1)
pot2 = Pot(2)

print(str(pot1.last))

def change(p):
    time.sleep(2)
    p.last = datetime.datetime.now

change(pot2)
print(str(pot2.last))

