from datetime import datetime
import time

from logging import exception
from telegram import *
from telegram.ext import * 
from requests import *
import requests
import json
import sys
import random
import datetime
import telepot
import RPi.GPIO as GPIO

import paho.mqtt.publish as publish
import psutil
import string

## ThingSpeak Channel connection
channel_ID = "1806671"
mqtt_host = "mqtt3.thingspeak.com"

# Your MQTT credentials for the device
mqtt_client_ID = "ITgGHjUoFwwZEDIUPCgIJS8"
mqtt_username  = "ITgGHjUoFwwZEDIUPCgIJS8"
mqtt_password  = "51bdD9cJODXzePgbKtaNFKQk"
t_transport = "websockets"
t_port = 80
topic = "channels/" + channel_ID + "/publish"

## AccuWeather API connection
accuKey = "GoxexX06khkOOTkiUFNfFB0Lh0tnAo1x"
cityKey = "214046"

## Raspberry Pi setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)

updater = Updater(token="5434499546:AAE6TfxPDbKsX4ajVIFFcqWQUmIf3RpOt4Q")
dispatcher = updater.dispatcher

water = "Let's water some pots!"
weatherButton = "Weather"
pot11 = "Pot 11"
pot16 = "Pot 16"
back = "Back"

lastPot11 = datetime.datetime.now()
lastPot16 = datetime.datetime.now()
allowedUsernames = ["DanieleDifra"]

def startCommand(update: Update, context: CallbackContext):
    startButtons = [[KeyboardButton(water)], [KeyboardButton(weatherButton)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to my bot!", reply_markup=ReplyKeyboardMarkup(startButtons))

def messageHandler(update: Update, context: CallbackContext, lastPot11: lastPot11, lastPot16: lastPot16):
    if update.effective_chat.username not in allowedUsernames:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not allowed to use this bot")
        return

    if water in update.message.text:
        waterButtons=[[KeyboardButton(back)], [KeyboardButton(pot11)], [KeyboardButton(pot16)]]
        waterText="Sure! Which pot do you want to water?\nLast time pot 11 was watered: " + str(lastPot11) + "\nLast time pot 16 was watered: " + str(lastPot16)
        context.bot.send_message(chat_id=update.effective_chat.id, text=waterText, reply_markup=ReplyKeyboardMarkup(waterButtons))

    ## TO DO
    if back in update.message.text:
       startCommand(Update,CallbackContext)    

    if pot11 in update.message.text:
        GPIO.output(11,True)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Watering pot 11")
        time.sleep(5)
        GPIO.output(11,False)
        lastPot11 = datetime.datetime.now()
        mqttPublish()
        context.bot.send_message(chat_id=update.effective_chat.id, text="Done")
        
    if pot16 in update.message.text:
        GPIO.output(16,True)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Watering pot 16")
        time.sleep(5)
        GPIO.output(16,False)
        lastPot16 = datetime.datetime.now()
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

def mqttPublish():
    payload = "field1=1"
    try:
        print ("Writing Payload = ", payload," to host: ", mqtt_host, " clientID= ", mqtt_client_ID, " User ", mqtt_username, " PWD ", mqtt_password)
        publish.single(topic, payload, hostname=mqtt_host, transport=t_transport, port=t_port, client_id=mqtt_client_ID, auth={'username':mqtt_username,'password':mqtt_password})
    except Exception as e:
        print (e) 