from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError

from issue.api import api_issue_comment_record
from issue.models import Issue
from user.models import GithubUser


class CommentManager(models.Manager):
    def record(self, data):
        author = self._get_author(data['comment']['user'])
        issue = self._get_issue(data)

        try:
            comment = api_issue_comment_record(author, issue, {"github_id": data['comment']['id']}, Comment)
        except IntegrityError as e:
            raise e
        return comment

    def _get_issue(self, data):
        try:
            issue = Issue.objects.get(github_id=data['issue']['id'])
        except ObjectDoesNotExist:
            issue = Issue.objects.record(data)

        return issue

    def _get_author(self, data):
        try:
            user = GithubUser.objects.get(github_id=data['id'])
        except ObjectDoesNotExist:
            user = GithubUser.objects.record(data)
        return user


class Comment(models.Model):
    github_id = models.CharField(max_length=45)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(GithubUser, on_delete=models.CASCADE)

    objects = CommentManager()

    def __str__(self):
        return "%s %s" % (self.author, self.issue)

    class Meta:
        db_table = "issue_comment"
        managed = True
