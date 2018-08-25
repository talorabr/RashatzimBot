# encoding: utf-8
from __future__ import unicode_literals

from rashatzim_bot_app.decorators import get_group
from rashatzim_bot_app.commands import Command
from datetime import timedelta


class CancelMeetingCommand(Command):
    """Telegram gym bot my statistics command.

    Sends training statistics of the requested trainee.

    """
    DEFAULT_COMMAND_NAME = 'cancel_meeting'
    CANCEL_MEETING_MSG = 'ישיבת הרש"צים השבוע בוטלה :('

    def __init__(self, *args, **kwargs):
        super(CancelMeetingCommand, self).__init__(*args, **kwargs)

    @get_group
    def _handler(self, bot, update, group):
        """Override method to handle cancel meeting command.

        Cancel meeting and move it to the next week

        """
        self.logger.info('Cancel meeting in %s', group)
        group = group.modify(new=True, set__next_meeting_date=group.next_meeting_date + timedelta(weeks=1))
        self.logger.info('New meeting will occur in: %s', group.next_meeting_date)
        update.message.reply_text(quote=True,
                                  text=self.CANCEL_MEETING_MSG)

