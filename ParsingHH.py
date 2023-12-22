import bs4
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json


url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
headers_generator = Headers(os="win", browser="firefox")

response = requests.get(url, headers=headers_generator.generate())
main_soup = bs4.BeautifulSoup(response.text, 'lxml')
vacancy_result = main_soup.find('div', attrs={'data-qa': 'vacancy-serp__results'})
link = vacancy_result.find_all('div', class_='vacancy-serp-item__layout')

result = []
for vacancy in link:
    title_link = vacancy.find('a', class_='serp-item__title')
    title = title_link['href']
    title_text = title_link.text
    company = vacancy.find('div', class_='vacancy-serp-item__meta-info-company').text
    city = vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
    salary = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
    if salary is None:
        salary = "Не указана"
    else:
        salary = salary.text

    response = requests.get(title, headers=headers_generator.generate())
    vacancy_content = response.text
    vacancy_soup = bs4.BeautifulSoup(vacancy_content, 'lxml')
    desc = vacancy_soup.find('div', class_ = 'g-user-content').text

    if "django" in (title_text + desc).lower() or "flask" in (title_text + desc).lower():
        result.append(
            {
                'link': title,
                'company': company,
                'city': city,
                'salary': salary,
            }
        )
with open("result.json", "w", encoding="utf-8") as file:
    json.dump(result, file, ensure_ascii=False, indent=2)