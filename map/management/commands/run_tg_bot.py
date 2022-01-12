from django.core.management.base import BaseCommand
from django.urls import reverse
from django.utils import timezone
import datetime

from telegram.ext import Updater
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from users.models import User
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
from users.models import User
import requests
from rest_framework.authtoken.models import Token


TOKEN = "1932808440:AAEq_BLBIUtGrBMBa8tznQulhzapPdElVd4"
updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

LOCATION_COORDS, LOCATION_NAME, DISASTER_TYPE, DISASTER_LEVEL = range(4)
DISASTER_LEVELS = [['1', '2', '3', '4', '5']]
DISASTER_TYPES = [['fire', 'water', 'geo', 'meteo']]


def send_data_to_service(data):
    data['name'] = 'from Telegram Bot.'
    print('!!!!')
    print(data)
    import ipdb; ipdb.set_trace()
    # TODO: get token, create request
    user = User.objects.filter(telegram_id=data['user'].id)
    if user.exists():
        user = user.first()
    else:
        return ConversationHandler.END

    token = Token.objects.get(user=user).key

    data = {
        'name': data['name'],
        'coordinates': f"{data['latitude']},{data['longitude']}",
        'disaster_type': data['disaster_type'],
        'disaster_level': data['disaster_level'],
    }
    response = requests.post(
        'http://127.0.0.1:8000/api/points/',  # TODO change to reverse.  example: reverse('point-list'),
        json=data,
        headers={'Authorization': f"token {token}"},
    )
    print(response.status_code)
    print(response.text)
    print(response.content)
    import ipdb; ipdb.set_trace()
    # return ConversationHandler.END



def sign_up(update: Update, context: CallbackContext):
    update.message.reply_text("Добро пожаловать в диалог с DisasterNotifierBot!")
    update.message.reply_text(f"Для регистрации перейдите по ссылке: {'http://127.0.0.1:8000/'}.")


def link_tg_acc_to_service(user_id, telegram_id):  # TODO think about name
    user = User.objects.filter(id=user_id)
    if user.exists():
        user = user.first()
        user.telegram_id = telegram_id
        user.save()


def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(
        f'Выход из диалога. До свидания, {user.first_name} {user.last_name}!',
        reply_markup=ReplyKeyboardRemove(),
    )
    # update.message.reply_text('Bye form cancel.')
    return ConversationHandler.END


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Добро пожаловать в диалог с DisasterNotifierBot!")
    message_text = update.message.text.split()
    if len(message_text) > 1:
        link_tg_acc_to_service(message_text[1], update.message.from_user.id)
        update.message.reply_text("Ваш Телеграм-аккаунт успешно привязан с DisasterNotifier!")
    update.message.reply_text("Отправьте своё местоположение или введите /cancel для выхода.")
    return 1


def send_location(update: Update, context: CallbackContext):
    update.message.reply_text("Местоположение получено.")
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    context.user_data['latitude'] = latitude
    context.user_data['longitude'] = longitude
    update.message.reply_text(
        'Введите тип ЧП:',
        reply_markup=ReplyKeyboardMarkup(
            DISASTER_TYPES, one_time_keyboard=True,  # input_field_placeholder='HEHEHE?'
        ),
    )
    return 2


def send_disaster_type(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Тип ЧП получен.')
    disaster_type = update.message.text
    context.user_data['disaster_type'] = disaster_type
    # context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

    update.message.reply_text(
        'Введите уровень опасности ЧП:',
        reply_markup=ReplyKeyboardMarkup(
            DISASTER_LEVELS, one_time_keyboard=True,  # input_field_placeholder='HEHEHE?'
        ),
    )
    return 3


def send_disaster_level(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Уровень опасности ЧП получен.')
    disaster_level = update.message.text
    user = update.message.from_user
    context.user_data['disaster_level'] = disaster_level
    context.user_data['user'] = user
    update.message.reply_text(
        f'Спасибо за вашу заботу, {user.first_name} {user.last_name}!',
        reply_markup=ReplyKeyboardRemove()
    )
    send_data_to_service(context.user_data)
    return ConversationHandler.END


# HANDLERS
conv_add_location_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        1: [MessageHandler(Filters.location, send_location)],
        # 2: [MessageHandler(Filters.text & ~Filters.command, send_location_name)],
        2: [MessageHandler(Filters.text & ~Filters.command, send_disaster_type)],
        3: [MessageHandler(Filters.text & ~Filters.command, send_disaster_level)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
# start_handler = CommandHandler('start', start) no need because in conv  # TODO remove later
signup_handler = CommandHandler('signup', sign_up)

# DISPATCHERS
# dispatcher.add_handler(start_handler)  no need because in conv # TODO remove later
dispatcher.add_handler(conv_add_location_handler)
dispatcher.add_handler(signup_handler)

updater.start_polling()
updater.idle()


class Command(BaseCommand):
    help = 'Run DisasterNotifier Telegram Bot.'

    def handle(self, *args, **kwargs):
        print('Stop Telegram Bot.')
        # time = timezone.now().strftime('%X')
        # self.stdout.write("It's now %s" % time)
        # print(datetime.datetime.now())
        # print(User.objects.all())
