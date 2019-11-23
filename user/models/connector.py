from django.db import models, IntegrityError
from django.utils.timezone import datetime

from user.api import api_connector_record
from xlib.api import GithubAPI


class ConnectorManager(models.Manager):
    def record(self, user, data):
        try:
            connector = api_connector_record(user, data, model=Connector)
        except IntegrityError:
            return None
        return connector


class Connector(models.Model):
    installation_id = models.CharField(max_length=45)
    access_token = models.CharField(max_length=512, null=True, blank=True)
    github_user = models.OneToOneField("user.GithubUser", on_delete=models.CASCADE, related_name="connector_set")
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ConnectorManager()

    __api = None

    @property
    def api(self):
        if self.expires_at is None or self.expires_at.isoformat() < datetime.now().isoformat():
            self.__get_token_access()
        self.__api = GithubAPI(token=self.access_token)
        return self.__api

    def install(self):
        self.__get_token_access()
        self.is_active = True

        self.save(update_fields=['is_active'])
        return True

    def __get_token_access(self):
        api = GithubAPI(token=None)
        response = api.post(f"app/installations/{self.installation_id}/access_tokens", data=None)
        assert response.status_code == 201
        response = response.json()
        self.access_token = response['token']
        self.expires_at = response['expires_at']

        self.save(update_fields=['access_token', 'expires_at'])

    def uninstall(self):
        self.is_active = False
        self.save(update_fields=['is_active'])

    def __str__(self):
        return "%s / %s" % (self.installation_id, self.github_user.username)
