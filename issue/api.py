from django.db import transaction, IntegrityError


@transaction.atomic
def api_issue_record(author, repository, data, model):
    assert "title" in data, "Missing 'title' parameter."
    assert "state" in data, "Missing 'state' parameter."
    assert "number" in data, "Missing 'number' parameter."
    assert "github_id" in data, "Missing 'github_id' parameter."

    github_id = data.pop('github_id')  # Todo remove this line

    try:
        instance, created = model.objects.update_or_create(author=author,
                                                           repository=repository,
                                                           github_id=github_id, defaults=data)
    except IntegrityError as e:
        raise e
    return instance


@transaction.atomic
def api_issue_comment_record(author, issue, data, model):
    assert "github_id" in data, "Missing 'github_id' parameter."

    try:
        instance, created = model.objects.update_or_create(author=author, issue=issue, defaults=data)
    except IntegrityError as e:
        raise e
    return instance
