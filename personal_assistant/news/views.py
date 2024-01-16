import requests
from django.http import HttpResponse
from django.shortcuts import render

from .tasks import scraping_ukraine, scraping_finance, scraping_culture, scraping_sport, scraping_suspilne


def main_news(request):
    api_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    response = requests.get(api_url)

    if response.status_code == 200:
        currencies = response.json()
        currencies = [currency for currency in currencies if currency['cc'] in ['USD', 'EUR', 'PLN']]
        return render(request, "news/main_news.html", {'currencies': currencies})
    else:
        error_message = 'Failed to fetch data from API'
        return HttpResponse(error_message, status=response.status_code, content_type='text/plain')


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
