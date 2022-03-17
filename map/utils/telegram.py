from telegram.ext import ExtBot
import os
from map.models import Point
from datetime import datetime


ACTION_RESOLVER = {
    "create": "Добавлена новая подтверждённая точка.",
    "update": "Одна из точек была подтверждена.",
}


def send_message_about_verification(action: str, point: Point) -> None:
    """Send message about verification to the channel and to private messages."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    channel = os.getenv("TELEGRAM_CHANNEL")
    bot = ExtBot(token)
    bot.send_message(channel, ACTION_RESOLVER[action])  # TO CHANNEL

    current_time = datetime.now().strftime('%d.%m.%Y %H:%M')
    author_telegram_id = point.created_by.telegram_id
    message = f"Ваша точка '{point.name}' была подтверждена в {current_time}"
    bot.send_message(author_telegram_id, message)  # TO PRIVATE MESSAGES
