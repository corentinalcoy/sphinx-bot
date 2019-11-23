from django.db import models, IntegrityError

from user.api import api_github_user_record
from xlib.enums import UserTypeEnum


class GithubUserManager(models.Manager):
    def record(self, data):
        clean_data = self._get_cleaned_data(data)
        github_id = data['id']

        try:
            user = api_github_user_record(github_id, clean_data, model=GithubUser)
        except IntegrityError as e:
            raise e

        return user

    def _get_cleaned_data(self, data):
        return {
            'username': data['login'],
            'url': data['html_url'],
            'type': data["type"].lower(),
            'is_active': True,
        }


class GithubUser(models.Model):
    username = models.CharField(max_length=200)
    github_id = models.CharField(max_length=45)
    is_active = models.BooleanField(default=True)
    url = models.URLField()
    type = models.CharField(max_length=20, choices=UserTypeEnum.values(), default="user")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = GithubUserManager()

    def __str__(self):
        return "%s / %s" % (self.username, self.url)

    @property
    def connector(self):
        return self.connector_set

    def uninstall(self):
        self.is_active = False
        self.save(update_fields=['is_active'])

    class Meta:
        db_table = "github_user"
        managed = True
