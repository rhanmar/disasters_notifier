import os

from django.core.management.base import BaseCommand
from map.models import DisasterTypes, Point
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater)
from users.models import User

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


LOCATION_COORDS, LOCATION_NAME, DISASTER_TYPE, DISASTER_LEVEL = range(4)
DISASTER_LEVELS = ['0', '1', '2', '3', '4', '5']
DISASTER_TYPES_info = list(DisasterTypes.RESOLVER.values())
DISASTER_TYPES = [
    [DISASTER_TYPES_info[0]],
    [DISASTER_TYPES_info[1]],
    [DISASTER_TYPES_info[2]],
    [DISASTER_TYPES_info[3]],
    [DISASTER_TYPES_info[4]],
]


def send_data_to_service(data: dict) -> None:
    try:
        Point.objects.create(
            name=data['name'],
            description=data['description'],
            coordinates=f"{data['latitude']},{data['longitude']}",
            disaster_type=DisasterTypes.TRANSLATOR[data['disaster_type']],
            disaster_level=data['disaster_level'],
            created_by=data['user'],
        )
    except Exception:
        pass


def sign_up(update: Update, context: CallbackContext):
    update.message.reply_text("Добро пожаловать в диалог с DisasterNotifierBot!")
    update.message.reply_text(f"Для регистрации перейдите по ссылке: {'http://127.0.0.1:8000/'}.")  # TODO to reverse


def link_tg_acc_to_service(user_id: str, telegram_id: int) -> None:  # TODO think about name
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
    return ConversationHandler.END


def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Добро пожаловать в диалог с DisasterNotifierBot!")
    message_text = update.message.text.split()
    if len(message_text) > 1:
        link_tg_acc_to_service(message_text[1], update.message.from_user.id)
        update.message.reply_text("Ваш Телеграм-аккаунт успешно привязан с DisasterNotifier!")

    user = update.message.from_user
    user_search = User.objects.filter(telegram_id=user.id)
    if not user_search.exists():
        update.message.reply_text("Ваш необходимо привязать ваш Телеграм-аккаунт к аккаунту сервиса. "
                                  "Для этого введите /signup")
        return ConversationHandler.END

    context.user_data['user'] = user_search.first()
    update.message.reply_text("Укажите краткое название точки или введитите /cancel для выхода.")
    return 1


def get_point_name(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Краткое название получено.')
    point_name = update.message.text
    context.user_data['name'] = point_name
    update.message.reply_text('Опишите событие.')
    return 2


def get_point_description(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Описание события получено.')
    point_description = update.message.text
    context.user_data['description'] = point_description
    update.message.reply_text("Отправьте своё местоположение.")
    return 3


def get_location(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Местоположение получено.")
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    context.user_data['latitude'] = latitude
    context.user_data['longitude'] = longitude
    update.message.reply_text(
        'Введите тип ЧП:',
        reply_markup=ReplyKeyboardMarkup(
            DISASTER_TYPES,
            one_time_keyboard=True,
        ),
    )
    return 4


def get_disaster_type(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Тип ЧП получен.')
    disaster_type = update.message.text
    context.user_data['disaster_type'] = disaster_type
    update.message.reply_text(
        'Введите уровень опасности ЧП:',
        reply_markup=ReplyKeyboardMarkup(
            DISASTER_LEVELS, one_time_keyboard=True,
        ),
    )
    return 5


def get_disaster_level(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Уровень опасности ЧП получен.')
    disaster_level = update.message.text
    user = update.message.from_user
    context.user_data['disaster_level'] = disaster_level
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
        1: [MessageHandler(Filters.text, get_point_name)], # 4
        2: [MessageHandler(Filters.text, get_point_description)], # 5
        3: [MessageHandler(Filters.location, get_location)], # 1
        4: [MessageHandler(Filters.text & ~Filters.command, get_disaster_type)], # 2
        5: [MessageHandler(Filters.text & ~Filters.command, get_disaster_level)], # 3

    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
signup_handler = CommandHandler('signup', sign_up)

# DISPATCHERS
dispatcher.add_handler(conv_add_location_handler)
dispatcher.add_handler(signup_handler)

updater.start_polling()
updater.idle()


class Command(BaseCommand):
    help = 'Run DisasterNotifier Telegram Bot.'

    def handle(self, *args, **kwargs):
        print('Stop Telegram Bot.')
