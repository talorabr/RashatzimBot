import logging
from operator import attrgetter

from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext.dispatcher import run_async

from rashatzim_bot_app.models import Group, TeamLeader


class RegisterUser(object):
    def __init__(self, updater, logger):
        self.updater = updater
        self.logger = logger

    @run_async
    def on_new_member(self, update):
        group_id = update.message.chat.id
        group = Group.objects.get(id=group_id)
        if group is None:
            group = Group.objects.create(id=group_id)

        self.logger.info('new members in %d: %d new members', group_id, len(update.message.new_chat_members))
        for user in update.message.new_chat_members:
            team_leader_id = user.id
            team_leader = TeamLeader.objects.get(id=team_leader_id)
            if team_leader is None:  # new team leader
                team_leader = TeamLeader.objects.create(id=team_leader_id,
                                                    first_name=user.first_name,
                                                    number_of_times_brought_food=min(group.team_leaders, attrgetter('number_of_times_brought_food')).number_of_times_brought_food)

            if team_leader not in group.team_leaders:
                group.add_team_leader(new_team_leader=team_leader)

    @run_async
    def on_left_member(self, update):
        self.logger.info('left member in %d', update.message.chat.id)
        group = Group.objects.get(id=update.message.chat_id)
        if group is None:
            self.logger.info('no group found!')
            return

        group.remove_team_leader(update.message.left_chat_member.id)