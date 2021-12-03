from telegram.ext import Updater
import logging
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler, MessageHandler, Filters


TOKEN = "1932808440:AAEq_BLBIUtGrBMBa8tznQulhzapPdElVd4"
updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def new(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="OLA")


def locations(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{update.message.location.latitude}, {update.message.location.longitude}"
    )


def messages(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


# HANDLERS
start_handler = CommandHandler('start', start)
new_handler = CommandHandler('new', new)
messages_location_handler = MessageHandler(Filters.location, locations)
messages_others_handler = MessageHandler(Filters.text & (~Filters.command), messages)
unknown_handler = MessageHandler(Filters.command, unknown)
# TODO https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py


# ADD HANDLERS
dispatcher.add_handler(start_handler)
dispatcher.add_handler(new_handler)
dispatcher.add_handler(messages_location_handler)
dispatcher.add_handler(messages_others_handler)
dispatcher.add_handler(unknown_handler)


updater.start_polling()
updater.idle()
