from django.db import IntegrityError

from bot.remind.signals import reminder_created
from issue.models import Comment
from xlib.utils import extractor


def hook_created(data):
    remind_info = extractor(data['comment']['body'])

    try:
        comment = Comment.objects.record(data)
    except IntegrityError:
        return False

    if remind_info is None:
        return False

    if data['action'] not in ['closed', 'deleted']:
        reminder_created.send(sender=comment, issue=comment.issue, author=comment.author, remind_info=remind_info)
    return True


def hook_edited(data):
    return hook_created(data)


def hook_deleted(data):
    return hook_created(data)

