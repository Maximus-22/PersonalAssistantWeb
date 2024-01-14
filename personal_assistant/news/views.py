from django.shortcuts import render

from .tasks import scraping_ukraine, scraping_finance, scraping_culture, scraping_sport


def all_news(request):
    return render(request, "news/all_news.html")


def ukraine_news(request):
    print("Start scraping")
    scraped_data = scraping_ukraine()
    context = {'scraped_data': scraped_data, 'active_tab': 'ukraine', 'title': 'Україна'}
    return render(request, "news/news.html", context)


def finance_news(request):
    print("Start scraping")
    scraped_data = scraping_finance()
    context = {'scraped_data': scraped_data, 'active_tab': 'finance', 'title': 'Фінанси'}
    return render(request, "news/news.html", context)


def culture_news(request):
    print("Start scraping")
    scraped_data = scraping_culture()
    context = {'scraped_data': scraped_data, 'active_tab': 'culture', 'title': 'Культура'}
    return render(request, "news/news.html", context)


def sport_news(request):
    print("Start scraping")
    scraped_data = scraping_sport()
    context = {'scraped_data': scraped_data, 'active_tab': 'sport', 'title': 'Спорт'}
    return render(request, "news/news.html", context)
