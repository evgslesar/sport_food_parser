import requests
import lxml.html
import time
import sqlite3
import pandas as pd
from fake_useragent import UserAgent


def get_html(html):
    tree = lxml.html.fromstring(html)
    item_cards = tree.xpath(
        '//div[@class="items-filter"]/div[@class="Items"]/div[@class="sitem"]')

    return item_cards


def get_pages_num(html):
    tree = lxml.html.fromstring(html)
    pages_num = tree.xpath('//div[@class="pagination"]/a')[-2].text
    pages_num = int(pages_num)

    return pages_num


def get_data(item_cards):
    data = []
    for item in item_cards:
        title = item.xpath('.//div[@class="si-desc"]/a')[0].text
        brand = item.xpath('.//div[@class="TItemTop"]')[0].text
        image = item.xpath('.//a/img')[0].attrib['src']
        url = item.xpath('.//div[@class="si-desc"]/a')[0].attrib['href']
        try:
            price = item.xpath(
                './/div[@class="si-desc"]/div[@class="si-price"]/div/span')[0].text
            price = float(price.replace(' ', ''))
        except:
            price = 'Not in stock'
        try:
            portions_num = item.xpath(
                './/div[@class="si-desc"]/div[@class="si-price"]/div/text()[2]')[0].split(' ')[-1]
            portions_num = int(portions_num)
        except:
            portions_num = 'N/A'
        try:
            portion_price = item.xpath(
                './/div[@class="si-desc"]/div[@class="si-price"]//div/text()[3]')[0].split(' ')[-2]
            portion_price = float(portion_price)
        except:
            portion_price = 'N/A'

        item_info = {
            'title': title,
            'price': price,
            'brand': brand,
            'portions_num': portions_num,
            'portion_price': portion_price,
            'image': 'https://sportivnoepitanie.ru'+image,
            'link': 'https://sportivnoepitanie.ru'+url,
        }
        data.append(item_info)

    return data


def save_to_db(total_data):
    df = pd.DataFrame(total_data)
    conn = sqlite3.connect('sport_food.db')
    df.to_sql("sport_food_info", conn)
    conn.close()


if __name__ == '__main__':
    url = 'https://sportivnoepitanie.ru/vitamins-minerals/'
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    html = requests.get(url, headers=headers)
    total_data = []
    pages_num = get_pages_num(html.text)
    for i in range(1, pages_num+1):
        time.sleep(2)
        if i < 2:
            html = html
        else:
            html = requests.get(url+f'?page={i}', headers=headers)
        item_cards = get_html(html.text)
        total_data.extend(get_data(item_cards))

    save_to_db(total_data)
