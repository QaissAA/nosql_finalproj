import urllib3
from bs4 import BeautifulSoup
import json
import time
import random
import logging


logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


http = urllib3.PoolManager(headers={"User-Agent": "Mozilla/5.0"})

BASE_URL = "https://moyo.moda"
CATEGORY_URL = f"{BASE_URL}/muzh/catalog"
MAX_PRODUCTS_PER_CATEGORY = 15  

def get_category_urls():
    CATEGORY_URL = "https://moyo.moda/muzh/catalog"
    print(f"Сканируем главную категорию: {CATEGORY_URL}")

    try:
        response = http.request('GET', CATEGORY_URL)
        if response.status != 200:
            print(f"Ошибка загрузки каталога ({response.status})")
            return []
    except Exception as e:
        print(f"Ошибка при запросе каталога: {CATEGORY_URL}\n{e}")
        return []

    soup = BeautifulSoup(response.data, 'html.parser')

    # Список разрешённых категорий
    allowed_categories = [
        "/muzh/catalog/muzhskie-maiki-futbolki",
        "/muzh/catalog/muzhskie-rubashki",
        "/muzh/catalog/muzhskoe-verkhnyaya-odezhda",
        "/muzh/catalog/muzhskie-bruki-djinsi",
        "/muzh/catalog/acsessuary-muzhskie"
    ]

    category_links = []
    for a_tag in soup.find_all("a", class_="category-card__link"):
        href = a_tag.get("href")
        if href in allowed_categories:
            full_link = "https://moyo.moda" + href
            category_links.append(full_link)

    print(f"Найдено {len(category_links)} разрешённых категорий.")
    return category_links


def get_product_urls(category_url):
    """Получает ссылки на товары в категории"""
    print(f" Сканируем категорию: {category_url}")

    try:
        response = http.request('GET', category_url, timeout=10)
        if response.status != 200:
            logging.warning(f"Ошибка загрузки категории {category_url}: статус {response.status}")
            return []
    except Exception as e:
        logging.error(f"Ошибка при запросе {category_url}: {e}")
        return []

    soup = BeautifulSoup(response.data, 'html.parser')
    product_links = [BASE_URL + a["href"] for a in soup.select("a.card-color") if a.get("href")]

    print(f" Найдено {len(product_links)} товаров (макс. {MAX_PRODUCTS_PER_CATEGORY}).")
    return product_links[:MAX_PRODUCTS_PER_CATEGORY]

def get_product_info(url, category_name):
    """Собирает информацию о товаре"""
    print(f" Парсим товар: {url}")

    try:
        response = http.request('GET', url, timeout=10)
        if response.status != 200:
            logging.warning(f"Ошибка загрузки товара {url}: статус {response.status}")
            return None
    except Exception as e:
        logging.error(f"Ошибка при запросе товара {url}: {e}")
        return None

    soup = BeautifulSoup(response.data, 'html.parser')

    def extract_text(selector, default="Не найдено"):
        tag = soup.select_one(selector)
        return tag.get_text(strip=True) if tag else default

    name = extract_text("span.product-card__brand", "Название не найдено")
    price = extract_text("div.card-price__actual", "Цена не найдена")

    image_tag = soup.select_one("img.product-card__pic")
    image_url = image_tag["src"] if image_tag and image_tag.get("src") else "Изображение не найдено"

    colors = [a["aria-label"] for a in soup.select("div.product-card__colors a") if a.get("aria-label")]

    product_id = url.rstrip("/").split("/")[-1].split("?")[0]

    return {
        "id": product_id,
        "name": name,
        "price": price,
        "image_url": image_url,
        "colors": colors,
        "url": url,
        "category": category_name  
    }

all_products_by_category = {}

category_urls = get_category_urls()

for category_url in category_urls:
    category_name = category_url.split("/")[-1]
    print(f"\n Обрабатываем категорию: {category_name}")

    product_urls = get_product_urls(category_url)
    if not product_urls:
        print(f" Пропускаем категорию '{category_name}', так как товары не найдены.")
        continue

    all_products_by_category[category_name] = []

    for count, url in enumerate(product_urls):
        product_info = get_product_info(url, category_name)
        if product_info:
            all_products_by_category[category_name].append(product_info)
            print(f" {count + 1}/{MAX_PRODUCTS_PER_CATEGORY}: {product_info['name']}")
        else:
            print(f" Ошибка при парсинге товара: {url}")

        time.sleep(random.uniform(1, 3))  

with open('moyo_products.json', 'w', encoding='utf-8') as file:
    json.dump(all_products_by_category, file, ensure_ascii=False, indent=4)

print("\n🎉 Данные успешно сохранены в 'moyo_products.json'!")
