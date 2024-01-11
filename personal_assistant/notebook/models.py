from django.db import models


class Notebook(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class Tag(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class NotebookTag(models.Model):
    notebook_id = models.ForeignKey(Notebook, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
