from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


def user_directory_path(instance, filename):
    extension = filename.split('.')[-1]
    user_folder = f'{instance.user.id}/' if instance.user else ''
    return f'files/{user_folder}{extension}/{filename}'


class File(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return f"{self.title}"
