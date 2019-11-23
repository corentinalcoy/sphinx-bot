from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from repository.models import Repository
from user.models import GithubUser, Connector


def hook_created(data):
    try:
        user = GithubUser.objects.record(data['installation']['account'])
    except (IntegrityError, AssertionError) as e:
        return False

    connector_data = {
        'installation_id': data['installation']['id']
    }
    connector = Connector.objects.record(user, connector_data)
    connector.install()

    repositories = []

    for repository in data['repositories']:
        repositories.append(
            Repository(github_id=repository['id'], name=repository['name'], github_user=user))
    Repository.objects.bulk_create(repositories, ignore_conflicts=True)

    return True


def hook_deleted(data):
    github_id = data['installation']['account']['id']
    try:
        github_user = GithubUser.objects.get(github_id=github_id)
    except ObjectDoesNotExist:
        return False

    github_user.uninstall()
    github_user.connector.uninstall()

    return True
