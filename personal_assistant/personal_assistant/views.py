from django.shortcuts import render


def main(request):
    return render(request, "personal_assistant/main.html")
