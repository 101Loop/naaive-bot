# NaaiveBot - Simple Telegram Bot

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/101Loop/naaive-bot/main.svg)](https://results.pre-commit.ci/latest/github/101Loop/naaive-bot/main)

A simple telegram bot which kicks out users from a group or channel when forbidden words like `aww` are used.

# Motivation
Just a random discussion in one of our company's group and [Himanshu Shankar](https://github.com/iamhssingh) said that create a bot which removes group members whenever they say words which contains `aww` and I thought **why not**.:wink:
# How To Use
- Go to https://t.me/beepstarbot and add it to your group or channel.
- Give admin permission to the bot, so that it can remove members whenever they use words which contains `aww`.
- Members will be removed for a day and will not be able to join using invite links in that period.
- Group **owners** & **admins** can add them again if they want to :joy:.
- **Group owners can use any words, they won't be removed.**

# How To Deploy Your Instance Of This Bot
You need **Python 3** and **PIP** installed for this to work

- Fork this repo to your profile
- `git clone link-to-repo.git` - Clone your copy of this repo to your local machine
- `cd naaive-bot` - Move to the repo folder
- Activate virtual environment. (We're expecting that you've created virtual environment by now.)
- Run `pip install -r requirements.txt` to  install dependencies
- Create a new bot using [Botfather](https://t.me/botfather) and get your **BOT_TOKEN**.
- Copy `.env.example` file to `.env` and add **BOT_TOKEN** & **SENTRY_DSN**(this is optional, leave this empty if you want. But [Sentry](https://sentry.io/) is a nice tool to log errors.)
- Run `python kick_members.py`
- Now your bot is up and running.

# How To Contribute
- Create an issue in case you find one with the bot. Please mention how you got to that issue in brief.
- Fork this repo and create a feature/bug branch and make your changes to that.
- Create PR from feature/bug branch to master of this repo.
