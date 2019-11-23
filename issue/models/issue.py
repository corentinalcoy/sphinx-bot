from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError

from issue.api import api_issue_record
from repository.models import Repository
from user.models import Connector, GithubUser


class IssueManager(models.Manager):
    def record(self, data):
        clean_data = self._get_cleaned_data(data['issue'])
        connector = self._get_connector(data['installation'])
        repository = self._get_github_repository(data['repository'], connector)

        author = self._get_author(data['issue']['user'])

        try:
            issue = api_issue_record(author, repository, clean_data, Issue)
        except IntegrityError:
            return None
        return issue

    def _get_cleaned_data(self, data):
        return {
            'title': data['title'],
            'state': data['state'],
            'number': data['number'],
            'github_id': data['id'],
        }

    def _get_github_repository(self, data, connector):
        repository, created = Repository.objects.get_or_create(github_id=data['id'], defaults={
            'name': data['name'],
            'github_user': connector.github_user
        })

        return repository

    def _get_author(self, data):
        try:
            user = GithubUser.objects.get(github_id=data['id'])
        except ObjectDoesNotExist:
            user = GithubUser.objects.record(data)
        return user

    def _get_connector(self, data):
        try:
            connector = Connector.objects.get(installation_id=data['id'])
        except ObjectDoesNotExist:
            return None
        return connector


class Issue(models.Model):
    github_id = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    title = models.CharField(max_length=100)
    number = models.IntegerField()
    author = models.ForeignKey("user.GithubUser", on_delete=models.CASCADE, related_name="issue_set")
    repository = models.ForeignKey("repository.Repository", on_delete=models.CASCADE, related_name="issue_set",
                                   null=True)

    objects = IssueManager()

    def __str__(self):
        return "%s %s" % (self.title, self.author.username)

    class Meta:
        db_table = "issue"
        managed = True
