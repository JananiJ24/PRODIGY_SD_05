import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def fetch_webpage(url):
    headers = {
        "User-Agent": "https://www.amazon.in/s?k=nike+sneakers+for+men&crid=DJGB5SIBW5RE&sprefix=nik%2Caps%2C256&ref=nb_sb_ss_pltr-data-refreshed_2_3"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def parse_webpage(html):
    soup = BeautifulSoup(html, 'html.parser')
    products = []

    for item in soup.select('.s-item'):
        name = item.select_one('.s-item__title')
        price = item.select_one('.s-item__price')
        rating = item.select_one('.x-star-rating')

        if name and price:
            rating_text = rating.get_text(strip=True) if rating else "No rating"
            products.append({
                'Name': name.get_text(strip=True),
                'Price': price.get_text(strip=True),
                'Rating': rating_text
            })

    return products

def save_to_csv(products, filename):
    df = pd.DataFrame(products)
    df.to_csv(filename, index=False)
    print(f'CSV file saved to: {filename}')

def main():
    base_url = 'https://www.ebay.com/sch/i.html?_nkw=laptops&_pgn='
    all_products = []

    for page in range(1, 6):  # Adjust the range for more pages
        url = base_url + str(page)
        print(f"Fetching URL: {url}")
        html = fetch_webpage(url)
        if html:
            products = parse_webpage(html)
            all_products.extend(products)
            print(f"Scraped {len(products)} products from page {page}")
        else:
            print(f"Failed to fetch page {page}")
        time.sleep(random.uniform(1, 3))  # Randomized delay to avoid detection

    save_to_csv(all_products, 'ebay_products.csv')
    print(f'Successfully saved {len(all_products)} products to ebay_products.csv')

if __name__ == '__main__':
    main()
