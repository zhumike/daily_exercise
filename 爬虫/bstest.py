# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :daily_exercise
# @File     :bstest
# @Date     :2024/4/13 09:12
# @Author   :zhuzhenzhong
# @Software :PyCharm
-------------------------------------------------
"""
import requests
from bs4 import BeautifulSoup

# Replace 'your_user_agent_string' with your actual user agent
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}


def fetch_product_info(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example: finding product titles on a Taobao product page
    # You need to inspect the HTML structure and update the tag and class accordingly
    products = soup.find_all('div', class_='product_class')  # Update 'div' and 'product_class' as per actual HTML tags

    for product in products:
        name = product.find('span', class_='name_class').text  # Update 'span' and 'name_class' as per actual HTML
        price = product.find('span', class_='price_class').text  # Update 'span' and 'price_class' as per actual HTML
        print(f'Product Name: {name}, Price: {price}')


# Example URL, replace with an actual product page URL
fetch_product_info('https://www.taobao.com/product_page_url')