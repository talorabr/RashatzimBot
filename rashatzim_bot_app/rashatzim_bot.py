# encoding: utf-8
from __future__ import unicode_literals

import logging
import os

from telegram.ext import Updater, MessageHandler, Filters

from rashatzim_bot_app.commands import (AdminCommand,
                                        MyDaysCommand,
                                        TrainedCommand,
                                        SelectDaysCommand,
                                        MyStatisticsCommand,
                                        AllTrainingTraineesCommand)
from rashatzim_bot_app.tasks import (BringFoodTask,
                                     WentToGymTask,
                                     NewWeekSelectDaysTask)
from rashatzim_bot_app.register_user import RegisterUser


MSG_TIMEOUT = 20

logging.basicConfig(filename='logs/rashatzimbot.log',
                    encoding='utf-8',
                    format='%(asctime)s %(levelname)s - [%(module)s:%(funcName)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.DEBUG)


def run_rashatzim_bot(token, logger):
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    register_user = RegisterUser(updater=updater, logger=logger)

    """ Handlers """
    dispatcher.add_handler(
        MessageHandler(Filters.status_update.new_chat_members & ~Filters.user(user_id=updater.bot.id),
                       register_user.on_new_member))
    dispatcher.add_handler(
        MessageHandler(Filters.status_update.left_chat_member & ~Filters.user(user_id=updater.bot.id),
                       register_user.on_left_member))

    """ Tasks """
    BringFoodTask(updater=updater, logger=logger).start()
    # WentToGymTask(updater=updater, logger=logger).start()
    # NewWeekSelectDaysTask(updater=updater, logger=logger).start()

    """ Commands """
    # AdminCommand(updater=updater, logger=logger).start()
    # MyDaysCommand(updater=updater, logger=logger).start()
    # TrainedCommand(updater=updater, logger=logger).start()
    # SelectDaysCommand(updater=updater, logger=logger).start()
    # MyStatisticsCommand(updater=updater, logger=logger).start()
    # AllTrainingTraineesCommand(updater=updater, logger=logger).start(command_name='all_the_botim')

    updater.start_polling(timeout=MSG_TIMEOUT)
    updater.idle()


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        os.environ['BOT_TOKEN'] = os.environ['BOT_TOKEN_TEST']
        os.environ['MONGODB_URL_CON'] = os.environ['MONGODB_URL_CON_TEST']

    token = os.environ['BOT_TOKEN']
    db_con_string = os.environ['MONGODB_URL_CON']

    from mongoengine import connect
    connect(host=db_con_string)

    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler())

    run_rashatzim_bot(token, logger)
