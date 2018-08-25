# encoding: utf-8
from __future__ import unicode_literals
import logging
from rashatzim_bot_app.models import Group
from rashatzim_bot_app.utils import _get_target_datetime_until_day_and_time
from operator import attrgetter
from datetime import timedelta, time, datetime

from telegram.utils.helpers import mention_html
from telegram.parsemode import ParseMode

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

BRING_FOOD_MSG = u'תורך להביא אוכל {team_leader}'


def callback_bring_food(bot, job):
    group = Group.objects.get(id=job.context)
    logger.info("starting callback for bring_food task for group %s %s", group, group.team_leaders)
    current_day = datetime.now()

    if not (current_day.date() == group.next_meeting_date.date() or
       current_day.date() == (group.next_meeting_date - timedelta(days=1)).date()):
        logger.info("not performing any action this day: %s!", current_day)
        return

    if not group.team_leaders:
        logger.info("no one in group %s!", group)
        return

    team_leader_to_bring_food = min(group.team_leaders, key=attrgetter('number_of_times_brought_food'))
    logger.info("chosen team leader is: %s", team_leader_to_bring_food)
    bring_food_msg = BRING_FOOD_MSG.format(team_leader=mention_html(int(team_leader_to_bring_food.id), team_leader_to_bring_food.first_name))
    bot.send_message(chat_id=group.id, text=bring_food_msg, parse_mode=ParseMode.HTML)
    if current_day.date() == group.next_meeting_date.date():
        logger.info("meeting occurs today, updating parameters")
        group.modify(set__next_meeting_date=group.next_meeting_date + timedelta(weeks=1))
        team_leader_to_bring_food.modify(upsert=True, new=True, inc__number_of_times_brought_food=1)


class task:
    name = 'bring_food'
    interval = timedelta(hours=12)
    first = min(_get_target_datetime_until_day_and_time(datetime.now().strftime("%A"),
                                                        time(hour=20, minute=30, second=0, microsecond=0)),
                _get_target_datetime_until_day_and_time(datetime.now().strftime("%A"),
                                                        time(hour=8, minute=30, second=0, microsecond=0)))
    callback = (callback_bring_food,)
