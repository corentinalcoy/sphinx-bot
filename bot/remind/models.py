from django.db import models

from issue.models import Issue
from user.models import GithubUser


class RemindManager(models.Manager):
    pass


class Remind(models.Model):
    author = models.ForeignKey(GithubUser, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    scheduled = models.DateTimeField()
    is_reminded = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = RemindManager()

    def __str__(self):
        return "%s %s at %s" % (self.issue, self.author, self.scheduled.isoformat())

    class Meta:
        db_table = "remind"
        unique_together = [('issue', 'author')]
        managed = True
