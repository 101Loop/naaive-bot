"""
This is a simple script to create a telegram bot.
This telegram bot removes group member for a day
if member uses words which contains `aww`.
"""

import datetime
import logging
import os
from typing import List

import sentry_sdk
import telebot
from dotenv import load_dotenv
from sentry_sdk.integrations.logging import LoggingIntegration
from telebot.apihelper import ApiTelegramException

from constants import ErrorMessages, BotPermissions

logger = logging.getLogger(__name__)

# initialize dot env
load_dotenv()

sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)

# initialize sentry
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    environment=os.getenv("SENTRY_ENV"),
    release=os.getenv("SENTRY_RELEASE"),
    traces_sample_rate=1.0,
    integrations=[sentry_logging],
)

# load BOT_TOKEN from env file
token = os.getenv("BOT_TOKEN")

# initialize bot with API TOKEN
# use https://t.me/botfather to generate your own
bot = telebot.TeleBot(token)

# i'm setting one day time limit to unban group members (update this as per need)
until_date: datetime = datetime.datetime.now() + datetime.timedelta(days=1)


@bot.message_handler(func=lambda m: True)
def kick_member(message: [telebot.types.Message]):
    """
    This methods kicks out members whose messages contains `aww`
    """
    if "aww" not in message.text.lower():
        return
    chat_id = message.chat.id
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    try:
        bot.ban_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            until_date=until_date,
        )
    except ApiTelegramException as err:
        # check if bot has admin permissions
        err_msg: str = err.result_json.get("description")
        if ErrorMessages.CHAT_ADMIN_REQUIRED in err_msg:
            handle_chat_admin_required(chat_id, first_name, user_id)
        elif ErrorMessages.NOT_ENOUGH_RIGHTS in err_msg:
            send_not_enough_permissions(chat_id)
        # check if message which contains `aww` sent by group owner
        elif ErrorMessages.CAN_NOT_REMOVE_CHAT_OWNER in err_msg:
            send_user_is_owner(chat_id, first_name)
        # check if the message which contains `aww` sent by group admin
        elif ErrorMessages.USER_IS_AN_ADMIN in err_msg:
            send_user_is_admin(chat_id, first_name)
        # checks if message is sent directly to bot
        elif ErrorMessages.BOT_USED_IN_PRIVATE_CHAT in err_msg:
            bot.send_message(chat_id, "Sorry mate, this doesn't work in private chats!")
        # otherwise, log errors to sentry
        else:
            logger.error(err)
            sentry_sdk.capture_exception(err)
    else:
        bot.send_message(
            chat_id,
            f"🚨 {first_name} have used a forbidden word and will be banned for a day from this group.",  # noqa
        )


def handle_chat_admin_required(chat_id, first_name, user_id):
    admins: List[telebot.types.ChatMember] = bot.get_chat_administrators(chat_id)
    if any(admin.user.is_bot for admin in admins):
        # somehow we're getting wrong error message even if bot has admin permissions
        # handling it here
        if bot.get_chat_member(chat_id, user_id).status == BotPermissions.CREATOR:
            send_user_is_owner(chat_id, first_name)
        else:
            send_user_is_admin(chat_id, first_name)
    else:
        send_not_enough_permissions(chat_id)


def send_user_is_admin(chat_id, first_name):
    bot.send_message(chat_id, f"{first_name} is an admin and admins are allowed to say forbidden words!")


def send_user_is_owner(chat_id, first_name):
    bot.send_message(
        chat_id=chat_id,
        text=f"Sorry folks, {first_name} is owner here . I can't do anything.",
    )


def send_not_enough_permissions(chat_id):
    bot.send_message(
        chat_id,
        "Forbidden Word used but I don't have enough permissions to kick members. "
        "Please make me an admin 🙏 .",
    )


bot.polling()
