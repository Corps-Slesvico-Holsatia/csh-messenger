"""ORM-related functions."""

from datetime import datetime
from itertools import chain
from typing import Optional

from cshsso import CommissionGroup
from cshsso import Convent
from cshsso import Circle
from cshsso import User
from peewee import Expression, ModelSelect

from cshmessenger.orm.models import Attachment, Group, GroupMember, Message


def select_groups() -> ModelSelect:
    """Selects groups."""

    return Group.select(Group, GroupMember).join(GroupMember).group_by(Group)


def select_user_groups(member: User) -> ModelSelect:
    """Selects groups, the user is member of."""

    return select_groups().where(GroupMember.member == member)


def select_administerable_groups(admin: User) -> ModelSelect:
    """Selects groups the user is an admin for."""

    return select_user_groups(admin).where(GroupMember.admin == 1)


def select_messages() -> ModelSelect:
    """Selects messages of the respective user."""

    return Message.select(Message, *Attachment.shallow()).join(
        Attachment).group_by(Message)


def select_slice(
        after: Optional[datetime],
        before: Optional[datetime]
) -> ModelSelect:
    """Selects a message slice."""

    condition = True

    if after is not None:
        condition &= Message.created > after

    if before is not None:
        condition &= Message.created < before

    return select_messages().where(condition)


def select_own_messages(sender: User) -> ModelSelect:
    """Selects own messages."""

    return select_messages().where(Message.sender == sender)


def get_own_message(sender: User, ident: int) -> Message:
    """Returns an own message."""

    return select_own_messages(sender).where(Message.id == ident).get()


def condition_private_conversation(user: User, partner: User) -> Expression:
    """Returns an expression to select a private conversation."""

    return (
        ((Message.sender == user) & (Message.recipient == partner))
        | ((Message.sender == partner) & (Message.recipient == user))
    )


def get_private_conversation_partners(user: User) -> set[User]:
    """Returns a set of users with whom a
    private conversation has taken place.
    """

    return {
        partner for partner in chain.from_iterable(
            (message.sender, message.recipient) for message
            in select_messages().where(
                (Message.sender == user) | (Message.recipient == user)
            )
        )
        if partner != user
    }


def select_private_conversation(user: User, partner: User) -> ModelSelect:
    """Selects a private conversation."""

    return select_messages().where(
        condition_private_conversation(user, partner)
    )


def select_circle_conversation(circle: Circle) -> ModelSelect:
    """Selects a circle conversation."""

    return select_messages().where(Message.circle == circle)


def select_commission_group_conversation(
            commission_group: CommissionGroup
        ) -> ModelSelect:
    """Selects a commission group conversation."""

    return select_messages().where(
        Message.commission_group == commission_group
    )


def select_convent_conversation(convent: Convent) -> ModelSelect:
    """Selects a circle conversation."""

    return select_messages().where(Message.convent == convent)


def select_group_conversation(group: Group) -> ModelSelect:
    """Selects a group conversation."""

    return select_messages().where(Message.group == group)
