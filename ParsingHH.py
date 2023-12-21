import bs4
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json


url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
headers_generator = Headers(os="win", browser="firefox")

response = requests.get(url, headers=headers_generator.generate())
main_soup = bs4.BeautifulSoup(response.text, 'lxml')


result = []
for vacancy in main_soup.find_all(class_ = 'vacancy-serp-item__layout'):
    link = vacancy.find(class_ = 'serp-item__title')
    title = link.text
    company = vacancy.find('div', class_ = 'vacancy-serp-item__meta-info-company').text
    city = vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
    salary = vacancy.find(class_='bloko-header-section-2')
    if salary is None:
        salary = "Не указана"
    else:
        salary = salary.text

    desc_item = main_soup.find(class_='g-user-content')
    desc = desc_item.text if desc_item is not None else ""
    if "django" in (title + desc).lower() or "flask" in (title + desc).lower():
        result.append(
            {
                'link': link['href'],
                'company': company,
                'city': city,
                'salary': salary,
            }
        )

with open("result.json", "w", encoding="utf-8") as file:
    json.dump(result, file, ensure_ascii=False, indent=2)
