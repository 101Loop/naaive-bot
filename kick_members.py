"""
This is a simple script to create a telegram bot.
This telegram bot removes group member for a day 
if member uses words which contains `aww`
"""
import os
import datetime
from dotenv import load_dotenv
import telebot
from telebot.apihelper import ApiTelegramException

load_dotenv()

# load BOT_API from env file
bot_api = os.getenv("BOT_API")

# initialize bot with API KEY
# use https://t.me/botfather to generate your own
bot = telebot.TeleBot(bot_api)

# set one day time limit to unban group members
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
        try:
            bot.kick_chat_member(
                chat_id=message.chat.id,
                user_id=message.from_user.id,
                until_date=unix_untildate,
            )
            bot.reply_to(
                message,
                "You've used a forbidden word, you'll be banned for a day from this group.",
            )
        except ApiTelegramException:
            bot.reply_to(message, "Oops, Chat Owner can use these forbidden words!")


bot.polling()
