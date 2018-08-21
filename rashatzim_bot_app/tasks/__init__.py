import logging
import importlib

from rashatzim_bot_app.tasks.task import Task
from rashatzim_bot_app.tasks.went_to_gym import WentToGymTask
from rashatzim_bot_app.tasks.new_week_select_days import NewWeekSelectDaysTask
from rashatzim_bot_app.bot import updater


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def import_tasks(group):
    job_queue = updater.job_queue
    for taskname in ('bring_food',):
        task = getattr(importlib.import_module('rashatzim_bot_app.tasks.{taskname}'.format(taskname=taskname)), 'task')
        logger.info('task imported: name=%s callback=%s interval=%d first=%d', task.name, task.callback[0], task.interval, task.first or 0)
        job_queue.run_repeating(callback=task.callback[0], interval=task.interval, first=task.first or 0, context=group.id)
