from django.db import transaction, IntegrityError


@transaction.atomic
def api_github_user_record(github_id, data, model):
    assert "username" in data, "Missing 'username' parameter."
    assert "url" in data, "Missing 'url' parameter."

    try:
        instance, created = model.objects.update_or_create(github_id=github_id, defaults=data)
    except IntegrityError as e:
        raise e

    return instance


@transaction.atomic
def api_connector_record(github_user, data, model):
    assert "installation_id" in data, "Missing 'installation_id' parameter."

    try:
        instance, created = model.objects.update_or_create(github_user=github_user, defaults=data)
    except IntegrityError as e:
        raise e

    return instance
