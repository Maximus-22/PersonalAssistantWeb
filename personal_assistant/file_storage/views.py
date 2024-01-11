from django.shortcuts import render


def all_files(request):
    return render(request, "file_storage/all_files.html")
