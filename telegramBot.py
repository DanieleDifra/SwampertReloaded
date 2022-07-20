from telegram import *
from telegram.ext import * 
from requests import *
import sys
import time
import random
import datetime
import telepot
import RPi.GPIO as GPIO

# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
# set up GPIO output channel
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)

updater = Updater(token="5434499546:AAE6TfxPDbKsX4ajVIFFcqWQUmIf3RpOt4Q")
dispatcher = updater.dispatcher

pot11 = "Water pot 11"
pot16 = "Water pot 16"

allowedUsernames = ["DanieleDifra"]

def startCommand(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton(pot11)], [KeyboardButton(pot16)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to my bot!", reply_markup=ReplyKeyboardMarkup(buttons))

def messageHandler(update: Update, context: CallbackContext):
    if update.effective_chat.username not in allowedUsernames:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not allowed to use this bot")
        return
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

dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))

updater.start_polling()
