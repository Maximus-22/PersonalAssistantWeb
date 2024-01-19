from django.contrib.auth.models import User
from django.db import models


class AddressBook(models.Model):
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=False, null=False)
    phone = models.CharField(max_length=255, blank=False, null=False, unique=True)
    email = models.CharField(max_length=255, blank=False, null=False, unique=True)
    birthday = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
