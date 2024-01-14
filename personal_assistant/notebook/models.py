from django.contrib.auth.models import User
from django.db import models


class Notebook(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', through='NotebookTag', related_name='notebooks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title}"


class Tag(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)

    class Meta:
        verbose_name_plural = "Tags"
        verbose_name = "Tag"

    def __str__(self):
        return f"{self.name}"


class NotebookTag(models.Model):
    notebook_id = models.ForeignKey(Notebook, on_delete=models.CASCADE, related_name='notebook_tags')
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag_notebooks')
