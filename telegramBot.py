from logging import exception
from telegram import *
from telegram.ext import * 
from requests import *
import requests
import json
import sys
import time
import random
import datetime
import telepot
import RPi.GPIO as GPIO

accuKey = "GoxexX06khkOOTkiUFNfFB0Lh0tnAo1x"
cityKey = "214046"

# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
# set up GPIO output channel
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)

updater = Updater(token="5434499546:AAE6TfxPDbKsX4ajVIFFcqWQUmIf3RpOt4Q")
dispatcher = updater.dispatcher

water = "Let's water some pots!"
weatherButton = "Weather"
pot11 = "Pot 11"
pot16 = "Pot 16"
back = "Back"

allowedUsernames = ["DanieleDifra"]

def startCommand(update: Update, context: CallbackContext):
    startButtons = [[KeyboardButton(water)], [KeyboardButton(weatherButton)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to my bot!", reply_markup=ReplyKeyboardMarkup(startButtons))

def messageHandler(update: Update, context: CallbackContext):
    if update.effective_chat.username not in allowedUsernames:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not allowed to use this bot")
        return

    if water in update.message.text:
        waterButtons=[[KeyboardButton(back)], [KeyboardButton(pot11)], [KeyboardButton(pot16)]]
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sure! Wich pot do you want to water?", reply_markup=ReplyKeyboardMarkup(waterButtons))

    if back in update.message.text
       startCommand(Update,CallbackContext)    

    if pot11 in update.message.text:
        GPIO.output(11,True)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Watering pot 11")
        time.sleep(5)
        GPIO.output(11,False)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Done")
        
    if pot16 in update.message.text:
        GPIO.output(16,True)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Watering pot 16")
        time.sleep(5)
        GPIO.output(16,False)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Done")

    if weatherButton in update.message.text:
        weather = getWeather()
        msg = "The weather today in Milan is " + weather[0]['WeatherText'] + "!\nThere are " + str(weather[0]['Temperature']['Metric']['Value']) + " degrees"
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))

updater.start_polling()

def getWeather():
    weather_url = "http://dataservice.accuweather.com/currentconditions/v1/214046?apikey=GoxexX06khkOOTkiUFNfFB0Lh0tnAo1x"
    response = requests.get(weather_url)
    if response.status_code == 200:
       json_response = json.loads(response.text)
       return json_response
    else:
       return exception
     
