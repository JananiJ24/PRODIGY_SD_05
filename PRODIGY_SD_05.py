import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def fetch_webpage(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
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

    for product in soup.select('.s-main-slot .s-result-item'):
        name = product.select_one('h2 .a-text-normal')
        price = product.select_one('.a-price .a-offscreen')
        rating = product.select_one('.a-icon-alt')

        if name and price and rating:
            products.append({
                'Name': name.get_text(strip=True),
                'Price': price.get_text(strip=True),
                'Rating': rating.get_text(strip=True)
            })

    return products

def save_to_csv(products, filename):
    df = pd.DataFrame(products)
    df.to_csv(filename, index=False)
    print(f'CSV file saved to: {os.path.abspath(filename)}')  # Print the absolute path

def main():
    base_url = 'https://www.amazon.in/s?k=nike+sneakers+for+men&page='
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
        time.sleep(2)  # Be polite and avoid getting blocked

    save_to_csv(all_products, 'amazon_products.csv')
    print(f'Successfully saved {len(all_products)} products to amazon_products.csv')

if __name__ == '__main__':
    main()
