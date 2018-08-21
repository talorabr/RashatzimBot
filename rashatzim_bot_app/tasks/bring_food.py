# encoding: utf-8
from __future__ import unicode_literals
import logging
from rashatzim_bot_app.models import Group
from operator import attrgetter

from telegram.utils.helpers import mention_html
from telegram.parsemode import ParseMode

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

BRING_FOOD_MSG = u'תורך להביא היום אוכל {team_leader}'


def callback_bring_food(bot, job):
    group = Group.objects.get(id=job.context)
    logger.info("starting callback for bring_food task for group %s %s", group, group.team_leaders)

    if not group.team_leaders:
        logger.info("no one in group %s!", group)
        return

    team_leader_to_bring_food = min(group.team_leaders, key=attrgetter('number_of_times_brought_food'))
    bring_food_msg = BRING_FOOD_MSG.format(mention_html(team_leader_to_bring_food.id, team_leader_to_bring_food.first_name))
    bot.send_message(chat_id=group.id, text=bring_food_msg, parse_mode=ParseMode.HTML)


class task:
    name = 'bring_food'
    interval = 60
    first = 0
    callback = (callback_bring_food,)
