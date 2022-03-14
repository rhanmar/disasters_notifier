from telegram.ext import ExtBot
import os


ACTION_RESOLVER = {
    "create": "Добавлена новая подтверждённая точка.",
    "update": "Одна из точек была подтверждена.",
}


def send_message_about_verification_to_channel(action):
    """TODO"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    channel = os.getenv("TELEGRAM_CHANNEL")
    bot = ExtBot(token)
    bot.send_message(channel, ACTION_RESOLVER[action])
