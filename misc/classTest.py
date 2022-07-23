import datetime as datetime
import time

class Pot:
    def __init__(self,pin):
        self.pin = pin
        self.last = datetime.datetime.now()

pot1 = Pot(1)
pot2 = Pot(2)

print(pot1.last)

def change():
    time.sleep(2)
    pot2.last = datetime.datetime.now()
    print(pot2.last.strftime("%d/%m/%Y - %H:%M"))

change()



