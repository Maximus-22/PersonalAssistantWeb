import os

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


def user_directory_path(instance, filename):
    name, extension = os.path.splitext(filename)
    user_folder = f'{instance.user.id}/'
    subfolder = 'others' if extension == '' else extension[1:]
    return f'{user_folder}{subfolder}/{filename}'


class File(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return f"{self.title}"
