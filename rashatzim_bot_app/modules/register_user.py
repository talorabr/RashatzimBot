import logging
from operator import attrgetter

from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext.dispatcher import run_async

from rashatzim_bot_app.models import Group, TeamLeader
from rashatzim_bot_app.bot import updater

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


@run_async
def on_new_member(bot, update):
    group_id = update.message.chat.id
    logger.info('new members in %d: %d new members', group_id, len(update.message.new_chat_members))

    group = Group.objects.get(id=group_id)
    if group is None:
        logger.info('creating group %d', group_id)
        group = Group.objects.create(id=group_id)

    for user in update.message.new_chat_members:
        logger.info('handling user %d', user.id)
        team_leader_id = user.id
        team_leader = TeamLeader.objects.get(id=team_leader_id)
        if team_leader is None:  # new team leader
            number_of_times_brought_food = min(group.team_leaders, key=attrgetter('number_of_times_brought_food')).\
                number_of_times_brought_food if group.team_leaders else 0

            team_leader = TeamLeader.objects.create(id=team_leader_id,
                                                    first_name=user.first_name,
                                                    number_of_times_brought_food=number_of_times_brought_food)

        if team_leader not in group.team_leaders:
            logger.info('adding %s to %s', team_leader, group)
            group.add_team_leader(new_team_leader=team_leader)


@run_async
def on_left_member(bot, update):
    logger.info('left member in %d', update.message.chat.id)
    group = Group.objects.get(id=update.message.chat_id)
    if group is None:
        logger.info('no group found!')
        return

    group.remove_team_leader(update.message.left_chat_member.id)


class module:
    name = 'register_user'
    handlers = (
        MessageHandler(Filters.status_update.new_chat_members & ~Filters.user(user_id=updater.bot.id), on_new_member),
        MessageHandler(Filters.status_update.left_chat_member & ~Filters.user(user_id=updater.bot.id), on_left_member)
    )
