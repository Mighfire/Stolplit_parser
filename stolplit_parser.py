# pip install requests beautifulsoup4 lxml
import json
import os

import requests
from bs4 import BeautifulSoup as BS


# количество страниц
def page_number(headers):
    url = 'https://www.stolplit.ru/internet-magazin/katalog-mebeli/24-kuxonnye-garnitury/?PAGEN_1=1'
    r = requests.get(url, headers=headers)
    soup = BS(r.content, "lxml")
    last_page = soup.find(class_='pagination__list').find('a', id='nav_next').find_previous_sibling().text
    return int(last_page)


headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}
product_data_base = []

for i in range(1, page_number(headers) + 1):
    url = 'https://www.stolplit.ru/internet-magazin/katalog-mebeli/24-kuxonnye-garnitury/?PAGEN_1=' + f"{i}"

    r = requests.get(url, headers=headers)

    soup = BS(r.content, "lxml")

    product_info = soup.find_all(class_='flex-layout__item js-product-info')

    for products in product_info:
        product_price = products.find(class_='product__mobile-price').find(class_='price--current').find('span', class_='price').text
        product_name = products.find(class_='product__info').find('a').text
        product_url = products.find(class_='product__info').find('a').get('href')
        product_data_base.append(
            {
                'Название товара:': product_name.strip(),
                'Цена товара': product_price.strip() + ' руб',
                'URL': 'https://www.stolplit.ru' + product_url
            }
        )
    print('Страница ' + f'{i}' + ' записана')

#создание папки
try:
    os.mkdir("data")
except:
    pass

# запись в json
with open('data/products_data.json', 'w', encoding='utf-8') as file:
    json.dump(product_data_base, file, indent=4, ensure_ascii=False)
