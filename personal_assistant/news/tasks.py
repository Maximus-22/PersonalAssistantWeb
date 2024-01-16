from datetime import datetime

import requests
from bs4 import BeautifulSoup


def scraping_ukraine(limit=10):
    result = []

    response = requests.get("https://www.unian.ua/society")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.select('div[class=list-thumbs__item]')
        count = 0

        for item in content:

            if count >= limit:
                break
            news_data = {}

            title_element = item.find('a', class_='list-thumbs__title')
            if title_element:
                news_data['title'] = title_element.text.strip()

            link_element = item.find('a', class_='list-thumbs__image')
            if link_element:
                news_data['link'] = link_element['href']

                img_element = link_element.find('img')

                if img_element:
                    news_data['image'] = img_element['data-src']

            time_element = item.find('div', class_='list-thumbs__time')
            if time_element:
                news_data['time'] = time_element.text.strip()

            print(news_data)
            if news_data:
                result.append(news_data)

            count += 1

    return result[:limit]


def scraping_finance(limit=10):
    result = []

    response = requests.get("https://minfin.com.ua/ua/news/")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.select('li[class=item]')
        print(content)

        count = 0

        for item in content:
            if count >= limit:
                break

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

            count += 1

    return result[:limit]


def scraping_culture():
    return scraping_suspilne("https://suspilne.media/culture/culture-ukraine/")


def scraping_sport():
    return scraping_suspilne("https://suspilne.media/sport/sport-ukraine/")


def scrape_news_items(soup, selector, title_class, link_class, time_class, img_class):
    result = []

    content = soup.select(selector)

    for item in content:
        news_data = {}

        title_element = item.find('h2', class_=title_class)
        if title_element:
            news_data['title'] = title_element.text.strip()

        link_element = item.find('a', class_=link_class)
        if link_element:
            news_data['link'] = link_element['href']

        time_element = item.find('time', class_=time_class)
        if time_element:
            datetime_str = time_element['datetime']
            datetime_object = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M+02:00')
            formatted_time = datetime_object.strftime('%H:%M, %d.%m.%Y')
            news_data['time'] = formatted_time

        img_element = item.find('img', class_=img_class)
        if img_element:
            news_data['image'] = img_element['src']

        print(news_data)
        if news_data:
            result.append(news_data)

    return result


def scraping_suspilne(url):
    result = []

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # For the first card format
        result.extend(scrape_news_items(soup, 'div.c-article-card-bgimage', 'c-article-card-bgimage__headline-inner',
                                        'c-article-card-bgimage__headline', 'c-article-card-bgimage__info__time--clock',
                                        'c-article-card-bgimage__image'))

        # For the second card format
        result.extend(
            scrape_news_items(soup, 'div.c-article-card', 'c-article-card__headline-inner', 'c-article-card__headline',
                              'c-article-card__info__time--clock', 'c-article-card__image'))

    return result
