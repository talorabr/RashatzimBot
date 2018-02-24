# encoding: utf-8
from __future__ import unicode_literals
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, ForeignKey, Integer, String, create_engine

Base = declarative_base()

user_and_days_association_table = Table('user_and_days', Base.metadata,
    Column('day', String, ForeignKey('day.name'),  primary_key=True),
    Column('user', Integer, ForeignKey('user.id'),  primary_key=True)
)

user_and_groups_association_table = Table('user_and_groups', Base.metadata,
    Column('group', Integer, ForeignKey('group.id')),
    Column('user', Integer, ForeignKey('user.id'))
)


class Day(Base):
    __tablename__ = 'day'
    name = Column(String(255), primary_key=True)
    users = relationship('User', secondary=user_and_days_association_table, backref='days')

    def __repr__(self):
        return '{name}'.format(name=self.name)

    def __unicode__(self):
        return repr(self)

    def __str__(self):
        return repr(self)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=True)

    def __repr__(self):
        return "<User(id='%s', first name='%s')>" % (self.id, self.first_name)

    def __unicode__(self):
        return repr(self)

    def __str__(self):
        return repr(self)


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    users = relationship('User', secondary=user_and_groups_association_table, backref='group')

    def __repr__(self):
        return "<Group(id='%s')>" % self.id

    def __unicode__(self):
        return repr(self)

    def __str__(self):
        return repr(self)


# engine = create_engine('sqlite:///sqlalchemy_example.db')
engine = create_engine('postgres://bmkeltax:mj9riixCKwtgLVg30HMk7x_KX8lTgZXS@horton.elephantsql.com:5432/bmkeltax')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)