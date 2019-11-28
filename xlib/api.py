"""
Github API Class
"""

__title__ = "github-api"
__version__ = "0.0.1"
__author__ = "Corentin Allohoumbo @ corentinalcoy@gmail.com"
__license__ = "MIT"

from json import dumps as jsonencode

import jwt
from django.conf import settings
from django.utils.timezone import datetime, timedelta
from requests import request

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class GithubAPI(object):
    """ GithubAPI Class """

    def __init__(self, token, **kwargs):
        self.url = "https://api.github.com"
        self.token = "token %s" % token if token else "Bearer %s" % self.__generate_token().decode()
        self.timeout = kwargs.get("timeout", 5)

    def __get_url(self, endpoint):
        """ Get URL for requests """
        url = self.url

        if url.endswith("/") is False:
            url = "%s/" % url

        return "%s%s" % (url, endpoint)

    def __generate_token(self):

        payload = {
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=5),
            'iss': settings.GITHUB_APP_KEY,
        }

        return jwt.encode(payload, settings.GITHUB_APP_SECRET, algorithm='RS256')

    def __request(self, method, endpoint, data, params=None, **kwargs):
        """ Do requests """
        if params is None:
            params = {}
        url = self.__get_url(endpoint)

        headers = {
            "user-agent": "Github API Client-Python/%s" % __version__,
            "accept": "application/vnd.github.machine-man-preview+json",
            "Authorization": self.token
        }

        if data is not None:
            data = jsonencode(data, ensure_ascii=False).encode('utf-8')
            headers["content-type"] = "application/json;charset=utf-8"

        return request(
            method=method,
            url=url,
            params=params,
            data=data,
            timeout=self.timeout,
            headers=headers,
            **kwargs
        )

    def get(self, endpoint, **kwargs):
        """ Get requests """
        return self.__request("GET", endpoint, None, **kwargs)

    def post(self, endpoint, data, **kwargs):
        """ POST requests """
        return self.__request("POST", endpoint, data, **kwargs)

    def put(self, endpoint, data, **kwargs):
        """ PUT requests """
        return self.__request("PUT", endpoint, data, **kwargs)

    def delete(self, endpoint, **kwargs):
        """ DELETE requests """
        return self.__request("DELETE", endpoint, None, **kwargs)

    def options(self, endpoint, **kwargs):
        """ OPTIONS requests """
        return self.__request("OPTIONS", endpoint, None, **kwargs)
