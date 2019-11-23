from django.db import IntegrityError

from issue.models import Issue


def hook_opened(data):
    try:
        issue = Issue.objects.record(data)
    except IntegrityError:
        return False

    return True


def hook_edited(data):
    return hook_opened(data)


def hook_closed(data):
    return hook_opened(data)


def hook_reopened(data):
    return hook_opened(data)


def hook_deleted(data):
    return hook_opened(data)
