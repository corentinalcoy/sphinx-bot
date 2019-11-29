from django.db import IntegrityError

from bot.remind.signals import reminder_created
from issue.models import Issue
from xlib.utils import extractor


def hook_opened(data):
    remind_info = extractor(data['issue']['body'])

    try:
        issue = Issue.objects.record(data)
    except IntegrityError:
        return False

    if remind_info is None:
        return False

    if data['action'] not in ['closed', 'deleted']:
        reminder_created.send(sender=issue, issue=issue, author=issue.author, remind_info=remind_info)
    return True


def hook_edited(data):
    return hook_opened(data)


def hook_closed(data):
    return hook_opened(data)


def hook_reopened(data):
    return hook_opened(data)


def hook_deleted(data):
    return hook_opened(data)
