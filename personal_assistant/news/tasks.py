from datetime import datetime

import requests
from bs4 import BeautifulSoup


def scraping_ukraine():
    result = []

    response = requests.get("https://www.unian.ua/society")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.select('div[class=list-thumbs__item]')

        for item in content:
            news_data = {}

            title_element = item.find('a', class_='list-thumbs__title')
            if title_element:
                news_data['title'] = title_element.text.strip()

            link_element = item.find('a', class_='list-thumbs__image')
            if link_element:
                news_data['link'] = link_element['href']

            time_element = item.find('div', class_='list-thumbs__time')
            if time_element:
                news_data['time'] = time_element.text.strip()
            if news_data:
                result.append(news_data)

    return result


def scraping_finance():
    result = []

    response = requests.get("https://minfin.com.ua/ua/news/")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.select('li[class=item]')
        print(content)

        for item in content:
            news_data = {}

            title_element = item.find('a')
            if title_element:
                news_data['title'] = title_element.text.strip()

            link_element = item.find('a')
            if link_element:
                news_data['link'] = link_element['href']

            time_element = item.find('span', class_='data')
            if time_element:
                datetime_str = time_element['content']
                datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
                formatted_time = datetime_object.strftime('%H:%M, %d.%m.%Y')

                news_data['time'] = formatted_time

            print(news_data)
            if news_data:
                result.append(news_data)

    return result


def scraping_culture():
    return scraping_suspilne("https://suspilne.media/culture/culture-ukraine/")


def scraping_sport():
    return scraping_suspilne("https://suspilne.media/sport/sport-ukraine/")


def scraping_suspilne(url):
    result = []

    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        print("OK")
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.select('div.c-article-card')  # Use dot notation for class selection
        print(content)

        for item in content:
            news_data = {}

            # Use 'h2' tag instead of 'a' for the title
            title_element = item.find('h2', class_='c-article-card__headline-inner')
            if title_element:
                news_data['title'] = title_element.text.strip()

            # Use 'a' tag for link
            link_element = item.find('a', class_='c-article-card__headline')
            if link_element:
                news_data['link'] = link_element['href']

            # Use 'time' tag for time
            time_element = item.find('time', class_='c-article-card__info__time--clock')
            if time_element:
                datetime_str = time_element['datetime']
                datetime_object = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M+02:00')
                formatted_time = datetime_object.strftime('%H:%M, %d.%m.%Y')

                news_data['time'] = formatted_time

            print(news_data)
            if news_data:
                result.append(news_data)

    return result
