from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re


# This function will check if the page exist or not
# It will return the number of pages if exist otherwise it will return 0
def check_page_exist(soup):
    try:
        # Find Navigation
        pagination_div = soup.find('div', attrs={'class':'pagination'})
        if pagination_div:
            # Find the last anchor tag in the pagination div
            last_anchor_tag = pagination_div.find_all('a')[-1]
            last_page_url = last_anchor_tag.get('href')
            # extract number from url
            match = re.search(r"/(\d+)/?$", last_page_url)
            if match:
                number = match.group(1)
                return number
        else:
            return 0


    except Exception as error:
        print("Error: in get_products()", error)   
        return 0


# This function will get all products from the provided url
# It will return a list of all product_names, product_urls, product_images, product_prices
def get_products(url):
    product_names = []
    product_urls = []
    product_images = []
    product_prices = []
    try:
        ua = UserAgent()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument(f'--user-agent={ua.random}')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(2)
        html_content = driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')
        number = check_page_exist(soup)
        driver.quit()

        if number != 0:
            print(number, "Pages Found")
            ua = UserAgent()
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument(f'--user-agent={ua.random}')
            driver = webdriver.Chrome(options=options)
            for i in range(1, int(number)+1):
                page_url = f"{url}{i}/"
                print("Visiting Page:", i)
                print('page_url',page_url)
                driver.get(page_url)
                time.sleep(2)
                html_content = driver.page_source
                soup = BeautifulSoup(html_content, 'html.parser')

                # find all products
                products_main_div = soup.find('div', attrs={'class': 'product-grid-div'})
                if products_main_div:
                    ul = products_main_div.find('ul', attrs={'class': 'item_grid'})
                    all_li = ul.find_all('li', attrs={'class': 'col-md-4'})
                    print(len(all_li), f"Products Found on Page-{i}")
                    for product_li in all_li:
                        name_div = product_li.find('div', attrs={'id': 'lap_name_div'})
                        # find product name and url
                        product_name = name_div.find('h3').get_text().strip()
                        product_url = name_div.find('a').get('href')

                        # find product image
                        product_image = ""
                        image_div = product_li.find('div', attrs={'class': 'image'})
                        img_tag = image_div.find('img', attrs={'class':'tt'})
                        if img_tag and img_tag.has_attr('data-original'):
                            product_image = img_tag['data-original']
                        
                        # find product price
                        price_div = product_li.find('div', attrs={'class': 'cat_price'})
                        price_data = price_div.get_text().strip()
                        price_span = price_div.find('span').get_text().strip()
                        product_price = ""
                        if price_span in price_data:
                            product_price = price_data.replace(price_span, "", 1).strip()   

                        # add product_name and product_url to list
                        product_names.append(product_name)
                        product_urls.append(product_url) 
                        product_images.append(product_image)
                        product_prices.append(product_price)

            driver.quit()
                        
        else:
            ua = UserAgent()
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument(f'--user-agent={ua.random}')
            driver = webdriver.Chrome(options=options)
            print("Only One Page Found")
            print("Visiting Page:", 1)
            driver.get(url)
            time.sleep(2)
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            driver.close()

            # find all products
            products_main_div = soup.find('div', attrs={'class': 'product-grid-div'})
            if products_main_div:
                ul = products_main_div.find('ul', attrs={'class': 'item_grid'})
                all_li = ul.find_all('li', attrs={'class': 'col-md-4'})
                print(len(all_li),"Products Found on Page-1")
                for product_li in all_li:
                    name_div = product_li.find('div', attrs={'id': 'lap_name_div'})
                    # find product name and url
                    product_name = name_div.find('h3').get_text().strip()
                    product_url = name_div.find('a').get('href')

                    # find product image
                    product_image = ""
                    image_div = product_li.find('div', attrs={'class': 'image'})
                    img_tag = image_div.find('img', attrs={'class':'tt'})
                    if img_tag and img_tag.has_attr('data-original'):
                        product_image = img_tag['data-original']

                    # find product price
                    price_div = product_li.find('div', attrs={'class': 'cat_price'})
                    price_data = price_div.get_text().strip()
                    price_span = price_div.find('span').get_text().strip()
                    product_price = ""
                    if price_span in price_data:
                        product_price = price_data.replace(price_span, "", 1).strip()

                    # add product details to the list
                    product_names.append(product_name)
                    product_urls.append(product_url)
                    product_images.append(product_image)
                    product_prices.append(product_price)

        return product_names, product_urls, product_images, product_prices

    except Exception as error:
        print("Error: in get_products()", error)
        return product_names, product_urls, product_images, product_prices