"""Databse table models."""

from datetime import datetime

from peewee import BooleanField, DateTimeField, ForeignKeyField

from cshsso import BaseModel, Circle, CommissionGroup, Convent, User
from peeweeplus import EnumField, FileMixin, HTMLCharField, HTMLTextField


__all__ = ['Group', 'GroupMember', 'Message', 'Attachment']


class Group(BaseModel):
    """A user-defined group."""

    name = HTMLCharField()


class GroupMember(BaseModel):
    """Group members."""

    group = ForeignKeyField(Group, column_name='group', on_delete='CASCADE',
                            lazy_load=False)
    member = ForeignKeyField(User, column_name='member', on_delete='CASCADE',
                             lazy_load=False)
    admin = BooleanField(default=False)


class Message(BaseModel):
    """A user message."""

    created = DateTimeField(default=datetime.now)
    reply_to = ForeignKeyField('self', column_name='reply_to',
                               on_delete='SET NULL', lazy_load=False)
    sender = ForeignKeyField(User, column_name='sender', on_delete='CASCADE',
                             lazy_load=False)
    recipient = ForeignKeyField(User, column_name='recipient', null=True,
                                on_delete='CASCADE', lazy_load=False)
    circle = EnumField(Circle, null=True)
    commission_group = EnumField(CommissionGroup, null=True)
    convent = EnumField(Convent, null=True)
    group = ForeignKeyField(Group, column_name='group', null=True,
                            on_delete='CASCADE', lazy_load=False)
    text = HTMLTextField(null=True)


class Attachment(BaseModel, FileMixin):
    """File attachments."""

    message = ForeignKeyField(Message, column_name='message',
                              on_delete='CASCADE', lazy_load=False)
