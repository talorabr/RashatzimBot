# encoding: utf-8
from __future__ import unicode_literals

from datetime import time, timedelta
from operator import attrgetter

from rashatzim_bot_app.tasks import Task
from rashatzim_bot_app.decorators import repeats, run_for_all_groups


class BringFoodTask(Task):
    """Telegram rashatzim bot bring food task."""
    DEFAULT_TARGET_DAY = 'Saturday'
    DEFAULT_TARGET_TIME = time(hour=22, minute=50, second=0, microsecond=0)

    BRING_FOOD_INDIVIDUAL = 'תורך להביא מחר אוכל @{team_leader}'

    def __init__(self, target_day=None, target_time=None, *args, **kwargs):
        super(BringFoodTask, self).__init__(*args, **kwargs)
        self.target_day = target_day or self.DEFAULT_TARGET_DAY
        self.target_time = target_time or self.DEFAULT_TARGET_TIME

    def get_start_time(self):
        """Start time of go to gym task based on the target time."""
        return self._seconds_until_day_and_time(target_day_name=self.target_day,
                                                target_time=self.target_time)

    @repeats(every_seconds=timedelta(weeks=1).total_seconds())
    @run_for_all_groups
    def execute(self, group):
        """Override method to execute bring food task.

        Sends bring food message with the team leader of today to the given group chat.

        """
        self.logger.info('Executing bring food task with %s', group)

        relevant_team_leaders = group.team_leaders
        self.logger.debug('Relevant team leaders %s', relevant_team_leaders)

        relevant_team_leader = min(relevant_team_leaders, key=attrgetter('number_of_times_brought_food'))
        self.logger.debug('Relevant team leader %s', relevant_team_leader)

        if not relevant_team_leader:
            self.logger.debug('There is no relevant team leader')
            return

        bring_food_msg = self._get_bring_food_msg(team_leader=relevant_team_leader)
        self.updater.bot.send_message(chat_id=group.id, text=bring_food_msg)

    def _get_bring_food_msg(self, team_leader):
        """Generate go to gym message based on the given trainees.

        Args:
            team_leader(TeamLeader): trainees that will be included in the message.

        Returns:
            str. message of go to gym with the given trainees.

        """

        self.logger.debug('Creating msg for individual')
        bring_food_msg = self.BRING_FOOD_INDIVIDUAL.format(team_leader=team_leader.first_name)

        return bring_food_msg
