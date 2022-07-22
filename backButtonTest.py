import os
from telegram.ext import Updater, ConversationHandler, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove


FIRST, SECOND, MAIN_MENU = range(3)


def get_main_menu():
    return [[InlineKeyboardButton("First", callback_data='first')],
            [InlineKeyboardButton("Second", callback_data='second')]]


def add_main_menu_button(bot, update, message, menu):
    query = update.callback_query
    menu.append([InlineKeyboardButton("Back to main menu", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(menu)

    bot.edit_message_text(message, chat_id=query.message.chat_id, message_id=query.message.message_id,
                          reply_markup=reply_markup)


def back_to_main_menu(bot, update):
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(get_main_menu())
    bot.edit_message_text("Example example 2", chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup)

    return MAIN_MENU


def second(bot, update):
    add_main_menu_button(bot, update, "E e", list())


def first(bot, update):
    add_main_menu_button(bot, update, "T t", list())


def start(bot, update):
    reply_markup = InlineKeyboardMarkup(get_main_menu())
    update.message.reply_text("Example example 1", reply_markup=reply_markup)

    return MAIN_MENU


def cancel(bot, update):
    update.message.reply_text('Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():
    updater = Updater(os.environ["5434499546:AAE6TfxPDbKsX4ajVIFFcqWQUmIf3RpOt4Q"])

    conversation_handler = ConversationHandler(entry_points=[CommandHandler('start', start)],

    states={FIRST: [CallbackQueryHandler(back_to_main_menu, pattern='^main_menu$')],
            SECOND: [CallbackQueryHandler(back_to_main_menu, pattern='^main_menu$')],
            MAIN_MENU: [CallbackQueryHandler(first, pattern='first'), 
                        CallbackQueryHandler(second)]},

    fallbacks=[CommandHandler('cancel', cancel)],
    allow_reentry=True
    )

    updater.dispatcher.add_handler(conversation_handler)

    updater.start_polling()
    updater.idle()