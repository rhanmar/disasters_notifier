from telegram.ext import Updater
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
from users.models import User

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


def start(update: Update, context: CallbackContext):
    print('!!!!!')
    print(update.message.from_user.id)
    user_unique_code = update.message.text.split()[1]
    user = User.objects.filter(unique_code=user_unique_code)
    if user.exists():
        user.first().telegram_id = update.message.from_user.id
        user.first().save()
    # import ipdb;
    # ipdb.set_trace()
    # update.message.from_user.name
    # import ipdb; ipdb.set_trace()
    # context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    update.message.reply_text("Добро пожаловать в диалог с DisasterNotifierBot!")
    update.message.reply_text("Отправьте своё местоположение")
    return 1


def new(update: Update, context: CallbackContext):
    # import ipdb;
    # ipdb.set_trace()
    context.bot.send_message(chat_id=update.effective_chat.id, text="OLA")


def locations(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{update.message.location.latitude}, {update.message.location.longitude}"
    )


def messages(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'{update.message.text} !!')


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def send_location(update: Update, context: CallbackContext):
    update.message.reply_text("Местоположение получено.")
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    context.user_data['latitude'] = latitude
    context.user_data['longitude'] = longitude
    # context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text=f"Your location is ({latitude}, {longitude})"
    # )
    # update.message.reply_text('Test reply_text from send_location.')
    # update.message.reply_text(f"Your location is ({latitude}, {longitude})")

    update.message.reply_text(
        'Введите тип ЧП:',
        reply_markup=ReplyKeyboardMarkup(
            DISASTER_TYPES, one_time_keyboard=True,  # input_field_placeholder='HEHEHE?'
        ),
    )
    return 2


# def send_location_name(update: Update, context: CallbackContext):
#     update.message.reply_text('Введите имя локации2.')
#     # context.user_data['zxc'] = 123
#     location_name = update.message.text
#     context.user_data['location_name'] = location_name
#     context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text=f"Your location name is {location_name}"
#     )
#     update.message.reply_text('Test reply_text from send_location_name.')
#     update.message.reply_text('Введите тип ЧП.')
#     return 3



def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(
        f'Выход из диалога. До свидания, {user.first_name} {user.last_name}!',
        reply_markup=ReplyKeyboardRemove(),
    )
    # update.message.reply_text('Bye form cancel.')
    return ConversationHandler.END


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


def send_data_to_service(data):
    data['name'] = 'from Telegram Bot.'
    print('!!!!')
    print(data)
    # return ConversationHandler.END


def send_disaster_level(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Уровень опасности ЧП получен.')
    disaster_level = update.message.text
    user = update.message.from_user
    context.user_data['disaster_level'] = disaster_level
    context.user_data['user'] = user

    # context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text="I'm a bot, please talk to me!"
    # )
    update.message.reply_text(
        f'Спасибо за вашу заботу, {user.first_name} {user.last_name}!',
        reply_markup=ReplyKeyboardRemove()
    )
    send_data_to_service(context.user_data)
    return ConversationHandler.END


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


# conv_sign_up_handler = ConversationHandler(
#
# )

def sign_up(update: Update, context: CallbackContext):
    update.message.reply_text('Добро пожаловать в диалог регистрации!')


def test(update: Update, context: CallbackContext):
    import ipdb;ipdb.set_trace()
    update.message.reply_text('YYYYYYY!')

# HANDLERS
start_handler = CommandHandler('start', start)
test_handler = CommandHandler('test', test)
# sign_up_handler = CommandHandler('sign up', sign_up)
# new_handler = CommandHandler('new', new)
# messages_location_handler = MessageHandler(Filters.location, locations)
# messages_others_handler = MessageHandler(Filters.text & (~Filters.command), messages)
# unknown_handler = MessageHandler(Filters.command, unknown)
# TODO https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py


# ADD HANDLERS
# dispatcher.add_handler(start_handler)
dispatcher.add_handler(conv_add_location_handler)
dispatcher.add_handler(test_handler)
# dispatcher.add_handler(conv_sign_up_handler)
# dispatcher.add_handler(new_handler)
# dispatcher.add_handler(messages_location_handler)
# dispatcher.add_handler(messages_others_handler)
# dispatcher.add_handler(unknown_handler)


updater.start_polling()
updater.idle()
