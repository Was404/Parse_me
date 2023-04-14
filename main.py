import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

from config import URL_TEMPLATE, FILE_NAME


def parse(url = URL_TEMPLATE):
    result_list = {'href': [], 'title': [], 'about': []} # создаем словарь, в котором будем хранить результаты парсинга сайта work.ua
    r = requests.get(url) # отправляем GET-запрос на сайт

    # парсим HTML-страницу при помощи BeautifulSoup
    # используем для этого html.parser
    soup = bs(r.text, "html.parser")
    vacancies_names = soup.find_all('h2', class_='add-bottom-sm') # ищем все элементы по тегу 'h2' и классу 'add-bottom-sm' (т.е. наименования вакансий)
    vacancies_info = soup.find_all('p', class_='overflow') # ищем все элементы по тегу 'p' и классу 'overflow' (т.е. описания вакансий)

    for name in vacancies_names: # проходим по каждому элементу списка vacancies_names
    # и добавляем в словарь result_list значения ключа 'href' (ссылку на вакансию) и ключа 'title' (наименование вакансии)
        result_list['href'].append('https://www.work.ua'+name.a['href'])
        result_list['title'].append(name.a['title'])

    for info in vacancies_info: # проходим по каждому элементу списка vacancies_info
    # и добавляем в словарь result_list значение ключа 'about' (описание вакансии)
        result_list['about'].append(info.text)
    return result_list


df = pd.DataFrame(data=parse())
df.to_csv(FILE_NAME)

if __name__ == '__main__':
    parse()
