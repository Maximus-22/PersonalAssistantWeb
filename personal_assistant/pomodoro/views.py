import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import PomodoroSession
from django.utils import timezone


@login_required
def start_pomodoro(request, session_type):
    print("Request received:", request.method, request.headers.get('X-Requested-With'))
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        data = json.loads(request.body)
        duration = data.get('duration')
        print("Duration received:", duration)
        new_session = PomodoroSession.objects.create(
            user=request.user,
            start_time=timezone.now(),
            duration=duration,
            session_type=session_type
        )
        return JsonResponse({
            "success": True,
            "session_type": new_session.get_session_type_display(),
            "start_time": new_session.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration": new_session.duration
        })
    return JsonResponse({"success": False}, status=400)


def index(request):
    sessions = PomodoroSession.objects.filter(user=request.user).order_by('-start_time')
    return render(request, 'pomodoro/pomodoro.html', {'sessions': sessions})
