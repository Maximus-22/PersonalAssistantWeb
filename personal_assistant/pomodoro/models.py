from django.db import models
from django.contrib.auth.models import User


class PomodoroSession(models.Model):
    SESSION_CHOICES = [
        ('P', 'Pomodoro'),
        ('SB', 'Short Break'),
        ('LB', 'Long Break')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    duration = models.CharField(max_length=10)
    session_type = models.CharField(max_length=2, choices=SESSION_CHOICES, default='P')

    def __str__(self):
        return f"{self.user} - {self.session_type} at {self.start_time}"

