from django.db import models

from issue.models import Issue
from user.models import GithubUser


class CommentManager(models.Manager):
    pass


class Comment(models.Model):
    github_id = models.CharField(max_length=45)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(GithubUser, on_delete=models.CASCADE)

    objects = CommentManager()

    class Meta:
        db_table = "issue_comment"
        managed = True
