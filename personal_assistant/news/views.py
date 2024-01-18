import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import City
from .tasks import scraping_ukraine, scraping_finance, scraping_culture, scraping_sport, get_weather_data


@login_required
def main_news(request):
    cities = City.objects.all()

    api_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    response = requests.get(api_url)

    if response.status_code == 200:
        currencies = response.json()
        currencies = [currency for currency in currencies if currency['cc'] in ['USD', 'EUR', 'PLN']]
        return render(request, "news/main_news.html", {'currencies': currencies, 'cities': cities})
    else:
        error_message = 'Failed to fetch data from API'
        return HttpResponse(error_message, status=response.status_code, content_type='text/plain')


def get_weather(request):
    selected_city = request.GET.get('city')
    try:
        selected_city = City.objects.get(name=selected_city)
        json_data = get_weather_data(selected_city.name, selected_city.latitude, selected_city.longitude)
        return JsonResponse({'weather_data': json_data})
    except City.DoesNotExist:
        print('City not found')


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
