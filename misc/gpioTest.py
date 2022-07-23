import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(25, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(6, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(24, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(23, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(22, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(27, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(18, GPIO.OUT, initial=GPIO.HIGH)