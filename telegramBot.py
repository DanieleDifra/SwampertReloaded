"""

"""

## Dependencies
import datetime
import time
import logging
import Models
from ssl import PROTOCOL_TLSv1_1
from typing import Any, Dict, Tuple

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

import requests
import json

import paho.mqtt.publish as publish
import psutil
import string

import RPi.GPIO as GPIO

## Variables declaration
# AccuWeather API connection
accuKey = "GoxexX06khkOOTkiUFNfFB0Lh0tnAo1x"
cityKey = "214046"

## Raspberry Pi setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT, initial=GPIO.HIGH) # pot 3
GPIO.setup(25, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(6, GPIO.OUT, initial=GPIO.HIGH) # to empty the water tank
GPIO.setup(24, GPIO.OUT, initial=GPIO.HIGH) # pot 2
GPIO.setup(23, GPIO.OUT, initial=GPIO.HIGH) # pot 1
GPIO.setup(22, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(27, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(18, GPIO.OUT, initial=GPIO.HIGH)

# Initializing classes
pot1 = Models.Pot(23)
pot2 = Models.Pot(24)
pot3 = Models.Pot(5)
pots = [ pot1, pot2, pot3 ]

# Water time (seconds)
WATER_TIME = 60 

## Telegram code
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# State definitions for top level conversation
SELECTING_ACTION, WATER_POTS, WEATHER, DESCRIBING_SELF = map(chr, range(4))
# State definitions for second level conversation
SELECTING_LEVEL, SELECTING_GENDER = map(chr, range(4, 6))
# Meta states
STOPPING, INFO = map(chr, range(8, 10))
# Shortcut for ConversationHandler.END
END = ConversationHandler.END

# Different constants for this example
(
    PARENTS,
    CHILDREN,
    SELF,
    EVERY,
    POT1,
    POT2,
    POT3,
    NAME,
    START_OVER,
    FEATURES,
    CURRENT_FEATURE,
    CURRENT_LEVEL,
) = map(chr, range(10, 22))

# Top level conversation callbacks
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: water the plants or check the weather"""

    last1 = pot1.lastWater.strftime("%d/%m/%Y - %H:%M")
    last2 = pot2.lastWater.strftime("%d/%m/%Y - %H:%M")
    last3 = pot3.lastWater.strftime("%d/%m/%Y - %H:%M")

    text = (
        "You may choose to water the plants, check the weather of Milan, get some info about the developer or"
        "just end the conversation. To abort, simply type /stop.\n\n"
        "Last time pot 1 was watered: " + last1 + 
        "\nLast time pot 2 was watered: " + last2 + 
        "\nLast time pot 3 was watered: " + last3
    )

    # Making sure that the valves are closed
    for p in pots:
        GPIO.output(p.pin,1)

    buttons = [
        [
            InlineKeyboardButton(text="Water some pots!", callback_data=str(WATER_POTS)),
            InlineKeyboardButton(text="Check weather", callback_data=str(WEATHER)),
        ],
        [
            InlineKeyboardButton(text="Info", callback_data=str(INFO)),
            InlineKeyboardButton(text="Done", callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
   
    # If we're starting over we don't need to send a new message
    if context.user_data.get(START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        await update.message.reply_text(
            "Hi, I'm Swampert manager. Here you can control your home irrigation system"
        )
        await update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False
    return SELECTING_ACTION


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Informations about the bot"""

    context.user_data[CURRENT_LEVEL] = SELF
    msg = "This bot is made by Daniele Di Francesco for the IOT course in PoliMi"
    buttons = [[InlineKeyboardButton(text="Back", callback_data=str(END))]]
    keyboard = InlineKeyboardMarkup(buttons)

    user_data = context.user_data
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=msg, reply_markup=keyboard)
    user_data[START_OVER] = True

    return INFO


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Weather informations"""

    context.user_data[CURRENT_LEVEL] = SELF

    weather = getWeather()
    condition = str(weather[0]['WeatherText'])
    temp = str(weather[0]['Temperature']['Metric']['Value'])
    msg = ( "The weather today in Milan is " + condition.lower() + "!\n"
          "It is " + temp + " degrees Celsius" )
    buttons = [[InlineKeyboardButton(text="Back", callback_data=str(END))]]
    keyboard = InlineKeyboardMarkup(buttons)

    user_data = context.user_data
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=msg, reply_markup=keyboard)
    user_data[START_OVER] = True

    return WEATHER


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End Conversation by command."""
    await update.message.reply_text("Okay, bye.")

    return END


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End conversation from InlineKeyboardButton."""
    await update.callback_query.answer()

    text = "See you around!"
    await update.callback_query.edit_message_text(text=text)

    return END


# Second level conversation callbacks
async def select_pot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Choose the pot to water"""

    context.user_data[CURRENT_LEVEL] = SELF

    text = "Choose the pot to water, or choose to water all the pots together"
    buttons = [
        [
            InlineKeyboardButton(text="Pot 1", callback_data=str(POT1)),
            InlineKeyboardButton(text="Pot 2", callback_data=str(POT2)),
        ],
        [
            InlineKeyboardButton(text="Pot 3", callback_data=str(POT3)),
            InlineKeyboardButton(text="Everything", callback_data=str(EVERY)),
        ],
        [   InlineKeyboardButton(text="Back", callback_data=str(END))
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    user_data = context.user_data
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    user_data[START_OVER] = True

    return SELECTING_LEVEL

async def water1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Water pot1"""
    text = "Watering pot 1 ..."
    buttons = [[   InlineKeyboardButton(text="Back", callback_data=str(END))]]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    
    GPIO.output(pot1.pin,0) #Open the valve
    time.sleep(WATER_TIME)
    GPIO.output(pot1.pin,1) #Close the valve
    pot1.lastWater = datetime.datetime.now()

    text += "\n...\n... done"
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return POT1

async def water2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Water pot2"""
    text = "Watering pot 2 ..."
    buttons = [[   InlineKeyboardButton(text="Back", callback_data=str(END))]]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    
    GPIO.output(pot2.pin,0) #Open the valve
    time.sleep(WATER_TIME)
    GPIO.output(pot2.pin,1) #Close the valve
    pot2.lastWater = datetime.datetime.now()

    text += "\n...\n...\ndone"
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return POT2

async def water3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Water pot3"""
    text = "Watering pot 3 ..."
    buttons = [[   InlineKeyboardButton(text="Back", callback_data=str(END))]]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    
    GPIO.output(pot3.pin,0) #Open the valve
    time.sleep(WATER_TIME)
    GPIO.output(pot3.pin,1) #Close the valve
    pot3.lastWater = datetime.datetime.now()

    text += "\n...\n...\ndone"
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return POT3

async def waterAll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Water every pot"""
    text = "Watering all the pots ..."
    buttons = [[InlineKeyboardButton(text="Back", callback_data=str(END))]]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    
    for p in pots:
        GPIO.output(p.pin,0)
        time.sleep(0.5) # I don't want the valves to open simultaneously
        
    time.sleep(WATER_TIME)
    for p in pots:
        GPIO.output(p.pin,1)
        p.lastWater = datetime.datetime.now()


    text += "\n...\n...\ndone"
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return EVERY

async def end_second_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Return to top level conversation."""
    context.user_data[START_OVER] = True
    await start(update, context)

    return END

async def end_describing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End gathering of features and return to parent conversation."""
    user_data = context.user_data
    level = user_data[CURRENT_LEVEL]
    if not user_data.get(level):
        user_data[level] = []
    user_data[level].append(user_data[FEATURES])

    # Print upper level menu
    if level == SELF:
        user_data[START_OVER] = True
        await start(update, context)
    else:
        await select_pot(update, context)

    return END

async def stop_nested(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Completely end conversation from within nested conversation."""
    await update.message.reply_text("Okay, bye.")

    return STOPPING

## Weather function
def getWeather():
    weather_url = "http://dataservice.accuweather.com/currentconditions/v1/"+cityKey+"?apikey="+accuKey
    response = requests.get(weather_url)
    if response.status_code == 200:
       json_response = json.loads(response.text)
       return json_response
    else:
       return exception

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5434499546:AAE6TfxPDbKsX4ajVIFFcqWQUmIf3RpOt4Q").build()

    # Set up second level ConversationHandler (adding a person)
    pot_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(select_pot, pattern="^" + str(WATER_POTS) + "$")],
        states={
            SELECTING_LEVEL: [
                CallbackQueryHandler(water1, pattern="^" + str(POT1) + "$"),
                CallbackQueryHandler(water2, pattern="^" + str(POT2) + "$"),
                CallbackQueryHandler(water3, pattern="^" + str(POT3) + "$"),
                CallbackQueryHandler(waterAll, pattern="^" + str(EVERY) + "$"),
            ]
        },
        fallbacks=[
            CallbackQueryHandler(end_second_level, pattern="^" + str(END) + "$"),
            CommandHandler("stop", stop_nested),
        ],
        map_to_parent={
            # Return to top level menu
            END: SELECTING_ACTION,
            # End conversation altogether
            STOPPING: END,
        },
    )

    # Set up top level ConversationHandler (selecting action)
    selection_handlers = [
        pot_conv,
        CallbackQueryHandler(info, pattern="^" + str(INFO) + "$"),
        CallbackQueryHandler(weather, pattern="^" + str(WEATHER) + "$"),
        CallbackQueryHandler(end, pattern="^" + str(END) + "$")
    ]
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            INFO: [CallbackQueryHandler(start, pattern="^" + str(END) + "$")],
            WEATHER: [CallbackQueryHandler(start, pattern="^" + str(END) + "$")],
            SELECTING_ACTION: selection_handlers,
            SELECTING_LEVEL: selection_handlers,
            STOPPING: [CommandHandler("start", start)],
        },
        fallbacks=[CommandHandler("stop", stop)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()