from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


def user_directory_path(instance, filename):
    extension = filename.split('.')[-1]

    # return f'files/test/{extension}/{filename}'
    # return f'files/{instance.user.id}/{extension}/{filename}'
    user_folder = f'{instance.user.id}/' if instance.user else ''
    return f'files/{user_folder}{extension}/{filename}'


class File(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    file_path = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return f"{self.title}"
