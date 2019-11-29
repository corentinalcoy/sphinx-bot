from django.dispatch import receiver, Signal
from django.utils.timezone import timedelta, datetime

from bot.remind.models import Remind

reminder_created = Signal(providing_args=['issue', 'author', 'remind_info'])


@receiver(reminder_created)
def register_reminder(**kwargs):
    issue = kwargs['issue']
    remind_info = kwargs['remind_info']
    author = kwargs['author']
    scheduled = datetime.utcnow() + timedelta(**{remind_info[1]: remind_info[0]})
    timedelta()
    Remind.objects.update_or_create(author=author, issue=issue, defaults={
        'scheduled': scheduled.astimezone(),
        'is_reminded': False
    })
