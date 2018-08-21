# encoding: utf-8
from __future__ import unicode_literals

import logging
import os
import importlib

from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

from rashatzim_bot_app.commands import (AdminCommand,
                                        MyDaysCommand,
                                        TrainedCommand,
                                        SelectDaysCommand,
                                        MyStatisticsCommand,
                                        AllTrainingTraineesCommand)
from rashatzim_bot_app.tasks import (WentToGymTask,
                                     NewWeekSelectDaysTask)
from rashatzim_bot_app.bot import updater, dispatcher
from rashatzim_bot_app.decorators import run_for_all_groups

MSG_TIMEOUT = 20

logging.basicConfig(filename='logs/rashatzimbot.log',
                    encoding='utf-8',
                    format='%(asctime)s %(levelname)s - [%(module)s:%(funcName)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


@run_async
def error_callback(bot, update, error):
    logger.info("error %s", error)


@run_for_all_groups
def import_tasks(group):
    job_queue = updater.job_queue
    from tasks.bring_food import callback_minute
    logger.info("callback_minute %s", callback_minute)
    for taskname in ('bring_food',):
        task = getattr(importlib.import_module('tasks.{taskname}'.format(taskname=taskname)), 'task')
        logger.info('task imported: name=%s callback=%s interval=%d first=%d', task.name, task.callback, task.first or 0)
        job_queue.run_repeating(callback=task.callback, interval=task.interval, first=task.first or 0, context=group.id)


def import_modules():
    for modname in ('register_user',):
        module = getattr(importlib.import_module('modules.{modname}'.format(modname=modname)), 'module')
        logger.info('module imported: %s (handlers: %d)', module.name, len(module.handlers))
        for handler in module.handlers:
            dispatcher.add_handler(handler)


def run_rashatzim_bot():

    """ Tasks """
    # BringFoodTask(updater=updater, logger=logger).start()
    # WentToGymTask(updater=updater, logger=logger).start()
    # NewWeekSelectDaysTask(updater=updater, logger=logger).start()

    """ Commands """
    # AdminCommand(updater=updater, logger=logger).start()
    # MyDaysCommand(updater=updater, logger=logger).start()
    # TrainedCommand(updater=updater, logger=logger).start()
    # SelectDaysCommand(updater=updater, logger=logger).start()
    # MyStatisticsCommand(updater=updater, logger=logger).start()
    # AllTrainingTraineesCommand(updater=updater, logger=logger).start(command_name='all_the_botim')

    import_tasks()
    import_modules()
    dispatcher.add_error_handler(error_callback)

    updater.start_polling(poll_interval=MSG_TIMEOUT)
    updater.idle()


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # os.environ['BOT_TOKEN'] = os.environ['BOT_TOKEN_TEST']
        os.environ['MONGODB_URL_CON'] = os.environ['MONGODB_URL_CON_TEST']

    # token = os.environ['BOT_TOKEN']
    db_con_string = os.environ['MONGODB_URL_CON']

    from mongoengine import connect
    connect(host=db_con_string)

    run_rashatzim_bot()
