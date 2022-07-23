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
GPIO.setup(11, GPIO.OUT)

updater = Updater(token="5434499546:AAE6TfxPDbKsX4ajVIFFcqWQUmIf3RpOt4Q")
dispatcher = updater.dispatcher

randomPeopleText = "Random Person"
randomImageText = "Random Image"
ledOn = "LED on"
ledOff = "LED off"
randomPeopleUrl = "https://thispersondoesnotexist.com/image"
randomPImageUrl = "https://picsum.photos/1200"

likes = 0
dislikes = 0

allowedUsernames = ["DanieleDifra"]

def startCommand(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton(ledOn)], [KeyboardButton(ledOff)], [KeyboardButton(randomImageText)], [KeyboardButton(randomPeopleText)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to my bot!", reply_markup=ReplyKeyboardMarkup(buttons))

def messageHandler(update: Update, context: CallbackContext):
    if update.effective_chat.username not in allowedUsernames:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not allowed to use this bot")
        return
    if ledOn in update.message.text:
        GPIO.output(11,True)
    if ledOff in update.message.text:
        GPIO.output(11, False)
    if randomPeopleText in update.message.text:
        image = get(randomPeopleUrl).content
    if randomImageText in update.message.text:
        image = get(randomPImageUrl).content

    if image:
        context.bot.sendMediaGroup(chat_id=update.effective_chat.id, media=[InputMediaPhoto(image, caption="")])

        buttons = [[InlineKeyboardButton("👍", callback_data="like")], [InlineKeyboardButton("👎", callback_data="dislike")]]
        context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="Did you like the image?")

def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()

    global likes, dislikes

    if "like" in query:
        likes +=1
    
    if "dislike" in query:
        dislikes +=1

    print(f"likes => {likes} and dislikes => {dislikes}")


dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
dispatcher.add_handler(CallbackQueryHandler(queryHandler))

updater.start_polling()
