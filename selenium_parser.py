import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_items(driver):
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(
        (By.XPATH, '//div[@class="product-bl"]'))
    )

    items = []
    item_cards = driver.find_elements(By.XPATH, '//div[@class="product-bl"]')

    for element in item_cards:
        try:
            link = element.find_element(By.XPATH, './/a').get_attribute('href')
        except:
            link = 'N/A'
        try:
            image = element.find_element(
                By.XPATH, './/descendant::picture/img').get_attribute('src')
        except:
            image = 'N/A'
        try:
            price = element.find_element(
                By.XPATH, './/div[@class="product-bl-txt"]/div[@class="product-price"]/span[1]').text.split('/')[0].split()[0]
        except:
            price = 'N/A'
        try:
            packing_size = element.find_element(
                By.XPATH, './/div[@class="product-bl-txt"]/div[@class="product-price"]/span[1]').text.split('/')[-1]
        except:
            packing_size = 'N/A'
        try:
            title = element.find_element(
                By.XPATH, './/div[@class="product-bl-txt"]/a').text
        except:
            title = 'N/A'
        try:
            article_id = element.find_element(
                By.XPATH, './/div[@class="product-bl-txt"]/div[@class="product-art"]').text.split(' ')[-1]
        except:
            article_id = 'N/A'
        try:
            old_price = element.find_element(
                By.XPATH, './/div/descendant::span[@class="old-price"]').text.split()[0]
        except:
            old_price = 'N/A'
        try:
            discount = element.find_element(
                By.XPATH, './/span/descendant::span[@class="price-old-badge"]').text
        except:
            discount = 'No discount'

        data = {
            "title": title,
            "image": image,
            "price": price,
            "packing_size": packing_size,
            "article_id": article_id,
            "old_price": old_price,
            "discount": discount,
            "link": link
        }
        items.append(data)

    return items


def save_to_file(items):
    with open('med_conf_foods.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['title', 'image', 'price', 'packing_size',
                        'article_id', 'old_price', 'discount', 'link'])
        for item in items:
            writer.writerow(list(item.values()))

    return


if __name__ == '__main__':
    url = 'https://www.med-konfitur.ru/catalog/sportivnoe_pitanie/'
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    all_items = []
    for i in range(1, 18):
        if i == 1:
            driver.get(url)
        else:
            driver.get(url+f'?PAGEN_7={i}')
        items = get_items(driver)
        all_items.extend(items)

    save_to_file(all_items)
    driver.close()