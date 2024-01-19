import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import localtime

from .models import PomodoroSession
from django.utils import timezone,formats


@login_required
def start_pomodoro(request, session_type):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        data = json.loads(request.body)
        duration_text = data.get('duration')
        new_session = PomodoroSession.objects.create(
            user=request.user,
            start_time=timezone.now(),
            duration=duration_text,
            session_type=session_type
        )
        formatted_start_time = formats.date_format(localtime(new_session.start_time), "d E Y р. H:i")
        return JsonResponse({
            "success": True,
            "session_type": new_session.get_session_type_display(),
            "start_time": formatted_start_time,
            "duration": new_session.duration
        })
    return JsonResponse({"success": False}, status=400)


def index(request):
    sessions = PomodoroSession.objects.filter(user=request.user).order_by('-start_time')
    return render(request, 'pomodoro/pomodoro.html', {'sessions': sessions})
