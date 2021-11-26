from telegram.ext import Updater
import logging

TOKEN = "1932808440:AAEq_BLBIUtGrBMBa8tznQulhzapPdElVd4"
updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


from telegram import Update
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def new(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="OLA")

from telegram.ext import CommandHandler

start_handler = CommandHandler('start', start)
new_handler = CommandHandler('new', new)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(new_handler)

updater.start_polling()


