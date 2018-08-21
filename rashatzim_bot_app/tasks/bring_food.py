# encoding: utf-8
from __future__ import unicode_literals
import logging


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def callback_minute(bot, job):
    logger.info("starting callback for bring_food task, chat id: %d!", job.context)
    bot.send_message(chat_id=job.context, text='SPAM FOR SOUFI')


class task:
    name = 'bring_food'
    interval = 60
    first = 0
    callback = callback_minute
