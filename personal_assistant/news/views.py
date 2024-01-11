from django.shortcuts import render


def all_news(request):
    return render(request, "news/all_news.html")
