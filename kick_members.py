"""
This is a simple script to create a telegram bot.
This telegram bot removes group member for a day 
if member uses words which contains `aww`
"""
import datetime
import logging
import os

import sentry_sdk
import telebot
from dotenv import load_dotenv
from telebot.apihelper import ApiTelegramException

logger = logging.getLogger(__name__)

# initialize dot env
load_dotenv()

# initialize sentry
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    environment=os.getenv("SENTRY_ENV"),
    traces_sample_rate=1.0,
)

# load BOT_TOKEN from env file
token = os.getenv("BOT_TOKEN")

# initialize bot with API TOKEN
# use https://t.me/botfather to generate your own
bot = telebot.TeleBot(token)

# i'm setting one day time limit to unban group members (update this as per need)
untildate = datetime.datetime.today() + datetime.timedelta(days=1)

# convert time limit to unix timestamp
unix_untildate = untildate.strftime("%s")


@bot.message_handler(func=lambda m: True)
def kick_member(message):
    """
    This methods kicks out members whose messages contains `aww`
    """
    if "aww" in (message.text).lower():
        chat_id = message.chat.id
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        try:
            bot.kick_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                until_date=unix_untildate,
            )
        except ApiTelegramException as err:
            # check if the message which contains `aww` sent by group owner
            if "can't remove chat owner" in err.result_json.get("description"):
                bot.send_message(
                    chat_id, "Oops, Chat Owner can use these forbidden words!"
                )
            # check if the message which contains `aww` sent by group admin
            elif "user is an administrator of the chat" in err.result_json.get(
                "description"
            ):
                bot.send_message(
                    chat_id, "Chat Admins can also use these forbidden words!"
                )
            # checks if message is sent directly to bot
            elif (
                "chat member status can't be changed in private chats"
                in err.result_json.get("description")
            ):
                bot.send_message(chat_id, "Sorry, This doesn't work in private chats!")
            # otherwise log errors to sentry
            else:
                logger.error(err)
                sentry_sdk.capture_exception(err)
        else:
            bot.send_message(
                chat_id,
                f"{first_name} have used a forbidden word and will be banned for a day from this group.",
            )


bot.polling()
