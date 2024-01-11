from django.shortcuts import render


def all_notes(request):
    return render(request, "notebook/all_notes.html")
