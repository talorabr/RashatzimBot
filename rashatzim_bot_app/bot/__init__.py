import os
from telegram.ext import Updater

updater = Updater(token=os.environ.get('BOT_TOKEN') or '')
dispatcher = updater.dispatcher
jobs = {}