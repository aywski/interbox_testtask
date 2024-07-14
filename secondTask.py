import requests
from bs4 import BeautifulSoup
import json

class EbayScraper:
    def __init__(self, url):
        self.url = url
        self.data = self.scrape_data()

    def scrape_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Отримуємо назву товару
            title_tag = soup.find('h1', {'class': 'x-item-title__mainTitle'})
            title = title_tag.get_text(strip=True) if title_tag else "N/A"

            # Отримуємо посилання на фото
            target_div = soup.find('div', class_='ux-image-carousel-item image-treatment active image')
            img_tag = target_div.find('img')
            image_url = img_tag['src'] if img_tag else "N/A"

            # Отримуємо ціну
            target_div = soup.find('div', class_='x-price-primary')
            price_tag = target_div.find('span', {'class': 'ux-textspans'})
            price = price_tag.get_text(strip=True) if price_tag else "N/A"

            # Отримуємо продавця
            seller_tag = soup.find('div', {'class': 'x-sellercard-atf__info__about-seller'})
            seller = seller_tag["title"] if seller_tag else "N/A"

            # Отримуємо ціну доставки
            target_div = soup.find('div', class_='ux-labels-values col-12 ux-labels-values--shipping')
            target_div = target_div.find('div', class_='ux-labels-values__values-content')
            shipping_tag = target_div.find('span', {'class': 'ux-textspans'})
            shipping_price = shipping_tag.get_text(strip=True) if shipping_tag else "N/A"

            data = {
                'title': title,
                'image_url': image_url,
                'product_url': self.url,
                'price': price,
                'seller': seller,
                'shipping_price': shipping_price
            }

            return data

        except requests.exceptions.RequestException as e:
            print(f"Error loading page: {e}")
            return None

    def print_data(self):
        if self.data:
            print(json.dumps(self.data, ensure_ascii=False, indent=4))

    def save_to_file(self, filename):
        if self.data:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)

# Використання класу
url = "https://www.ebay.com/itm/284324150302"
scraper = EbayScraper(url)
scraper.print_data() 
scraper.save_to_file('product_data.json')
