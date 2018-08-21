# encoding: utf-8
from __future__ import unicode_literals


def callback_minute(bot, job):
    bot.send_message(chat_id=job.context, text='SPAM FOR SOUFI')


class task:
    name = 'bring_food'
    interval = 60
    first = 0
    callback = callback_minute
