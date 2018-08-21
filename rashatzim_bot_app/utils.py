# encoding: utf-8
from __future__ import unicode_literals
from datetime import datetime, timedelta
import logging

import telegram

from rashatzim_bot_app import DAYS_NAME


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def day_name_to_day_idx(day_name):
    """Convert day name to day index.

    Args:
        day_name(str): name of the day to convert.

    Returns:
        int. index of the given day.

    """
    return DAYS_NAME.index(day_name.capitalize())


def number_of_days_until_next_day(target_day_name):
    """Calculate the number of days until the next occurrence of target day.

    Args:
        target_day_name(str): name of the target day.

    Returns:
        int. number of days until the target day.

    """
    today = datetime.today().strftime('%A')
    return (DAYS_NAME.index(target_day_name.capitalize()) - DAYS_NAME.index(today)) % len(DAYS_NAME)


def trainee_already_marked_training_date(trainee, training_date):
    """Check whether trainee already marked the given training date.

    If trainee already has training day info it means he/she answered marked the given date.

    Args:
        trainee(models.TeamLeader): trainee instance to check whether already marked the given date.
        training_date(datetime.date): training date to check.

    Returns:
        bool. True if trainee already marked the given date, otherwise False.

    """
    return bool(trainee.get_training_info(training_date=training_date))


def get_trainees_that_selected_today_and_did_not_train_yet(group):
    """Get all trainees in group that selected today as training day but did not train yet.

    Args:
        group(models.Group): group instance to filter trainees that selected today as training day and did not
                              train yet.

    Returns:
         list. all trainees in group that selected today as training day but did not train by now.

    """
    today_date = datetime.now().date()
    today_training_trainees = group.get_trainees_of_today()
    did_not_train_yet_trainees = [trainee for trainee in today_training_trainees
                                  if not trainee_already_marked_training_date(trainee=trainee,
                                                                              training_date=today_date)]
    return did_not_train_yet_trainees


def find_instance_in_args(obj, args):
    """find instance of given object type args.

    Args:
        obj(type): type of object to look for.
        args(iterable): arguments to search for the given object type.

    Returns:
        obj. instance of the obj type that found in args.

    """
    return filter(lambda arg: isinstance(arg, obj), args)[0]


def get_bot_and_update_from_args(args):
    """Find bot and update instance in the given args.

    Args:
        args(iterable): arguments to search for the bot and update.

    Returns:
        tuple.
          telegram.Bot. instance of bot that found in args.
          telegram.Upate. instance of update that found in args.

    """
    bot = find_instance_in_args(telegram.bot.Bot, args)
    update = find_instance_in_args(telegram.update.Update, args)
    return bot, update


def _get_target_datetime_until_day_and_time(target_day_name, target_time):
    """Calculate the number of seconds until the next occur of the target day and time.

    Args:
        target_day_name(str): name of the target day.
        target_time(time.time): target time of the day.

    Returns.
        int. number of seconds until the given day and time.

    """
    logger.info('Requested target day is %s and time is %s', target_day_name, target_time)
    now = datetime.today()
    days_until_next_target_day = number_of_days_until_next_day(target_day_name)

    target_datetime = now.replace(hour=target_time.hour,
                                  minute=target_time.minute,
                                  second=target_time.second,
                                  microsecond=target_time.microsecond)

    # if today is the requested day and the target time already passed.
    if days_until_next_target_day is 0 and now.time() > target_time:
        logger.debug('Today is the requested day but the time already passed, targeting time for next week')
        target_datetime += timedelta(weeks=1)
    else:
        logger.debug('Number of days left until the target day is %s', days_until_next_target_day)
        target_datetime += timedelta(days=days_until_next_target_day)

    logger.debug('Requested target datetime is %s', target_datetime)
    return target_datetime
