from django.db import models


class RepositoryManager(models.Manager):
    def record(self, user, data):
        pass


class Repository(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey("user.GithubUser", on_delete=models.CASCADE)
    github_id = models.CharField(max_length=45, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = RepositoryManager()

    def __str__(self):
        return "%s / %s" % (self.name, self.owner.username)

    class Meta:
        db_table = "repository"
        unique_together = (('github_id', 'owner'),)
        managed = True
