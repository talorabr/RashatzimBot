# encoding: utf-8
from __future__ import unicode_literals

from datetime import datetime, timedelta, time

from mongoengine import (Document,
                         ListField,
                         StringField,
                         LongField,
                         BooleanField,
                         DateTimeField,
                         EmbeddedDocument,
                         LazyReferenceField,
                         CachedReferenceField,
                         )

from rashatzim_bot_app import DAYS_NAME
from rashatzim_bot_app.query_sets import ExtendedQuerySet
from rashatzim_bot_app.utils import _get_target_datetime_until_day_and_time


class Day(EmbeddedDocument):
    name = StringField(required=True, max_length=64)
    selected = BooleanField(default=False)

    @classmethod
    def get_week_days(cls):
        return [cls(day_name) for day_name in DAYS_NAME]

    def __repr__(self):
        return '<Day {day_name} {selected}>'.format(day_name=self.name,
                                                    selected='selected' if self.selected
                                                             else 'not selected')

    def __str__(self):
        return repr(self)

    def __unicode__(self):
        return repr(self)


class TeamLeader(Document):
    id = StringField(required=True, primary_key=True)
    first_name = StringField(required=True)
    number_of_times_brought_food = LongField(required=True)

    class TeamLeaderQuerySet(ExtendedQuerySet):
        def create(self, id, first_name, number_of_times_brought_food):

            return super(TeamLeader.TeamLeaderQuerySet, self).create(id=unicode(id),
                                                                     first_name=unicode(first_name),
                                                                     number_of_times_brought_food=number_of_times_brought_food)

    meta = {
        'queryset_class': TeamLeaderQuerySet,
    }

    @property
    def groups(self):
        return Group.objects.filter(trainees__contains=self)

    def __repr__(self):
        return '<TeamLeader {id} {first_name}>'.format(id=self.id,
                                                    first_name=self.first_name)

    def __str__(self):
        return repr(self)

    def __unicode__(self):
        return repr(self)


class TrainingDayInfo(Document):
    trainee = LazyReferenceField(document_type=TeamLeader)
    date = DateTimeField(default=datetime.now)
    trained = BooleanField()

    meta = {
        'indexes': [('trainee', '-date')],
        'index_background': True,
    }

    def __repr__(self):
        return '<TrainingDayInfo trainee {trainee_pk} {trained} {date}>'.format(trainee_pk=self.trainee.pk,
                                                                                trained='trained' if self.trained
                                                                                        else 'did not train',
                                                                                date=self.date.strftime('%d-%m-%Y %H:%M:%S'))

    def __str__(self):
        return repr(self)

    def __unicode__(self):
        return repr(self)


class Group(Document):
    id = StringField(required=True, primary_key=True)
    team_leaders = ListField(CachedReferenceField(TeamLeader, auto_sync=True))
    next_meeting_date = DateTimeField(required=True, default=_get_target_datetime_until_day_and_time('Sunday',
                                                                                                     time(hour=12,
                                                                                                          minute=0,
                                                                                                          second=0,
                                                                                                          microsecond=0)))

    class GroupQuerySet(ExtendedQuerySet):
        def create(self, id, team_leaders=[], next_meeting_date=_get_target_datetime_until_day_and_time('Sunday',
                                                                                                        time(hour=12,
                                                                                                             minute=0,
                                                                                                             second=0,
                                                                                                             microsecond=0)
                                                                                                        )):
            return super(Group.GroupQuerySet, self).create(id=unicode(id),
                                                           team_leaders=team_leaders,
                                                           next_meeting_date=next_meeting_date)

    meta = {
        'queryset_class': GroupQuerySet,
    }

    def add_team_leader(self, new_team_leader):
        self.update(push__team_leaders=new_team_leader)
        return self

    def remove_team_leader(self, team_leader_id):
        for team_leader in self.team_leaders:
            if team_leader.id == team_leader_id:
                team_leader.delete()

    def __repr__(self):
        return '<Group {id}>'.format(id=self.id)

    def __str__(self):
        return repr(self)

    def __unicode__(self):
        return repr(self)

    def __iter__(self):
        return iter(self.team_leaders)


class Admin(Document):
    id = StringField(required=True, primary_key=True)

    class AdminQuerySet(ExtendedQuerySet):
        def create(self, id):
            return super(Admin.AdminQuerySet, self).create(id=unicode(id))

        def is_admin(self, id):
            return bool(self.get(id=id))

    meta = {
        'queryset_class': AdminQuerySet,
    }

    def __repr__(self):
        return '<Admin {id}>'.format(id=self.id)

    def __str__(self):
        return repr(self)

    def __unicode__(self):
        return repr(self)
