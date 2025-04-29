from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium import webdriver
import time


# This function will get all brand names and urls if found. otherwise it will return provided url
def get_brands(url):
    brand_names = []
    brand_urls = []
    bad_url = ""

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
        driver.quit()

        # find all brands
        try:
            main_brand_div = soup.find('div', attrs={'class': 'brand-shrt-div'})
            if main_brand_div:
                brand_row = main_brand_div.find_all('div', attrs={'class': 'row'})[0]
                for div in brand_row.find_all('div', attrs={'class': 'brand-box'}):
                    brand_div = div.find('div', attrs={'class': 'brand-logos'})
                    brand_anchor_tags = brand_div.find_all('a')

                    brand_url = brand_anchor_tags[1].get('href')
                    brand_name = brand_anchor_tags[1].find('h3').get_text().strip()
                    if brand_name == "Gaming Laptop":
                        pass
                    else:
                        brand_names.append(brand_name)
                        brand_urls.append(brand_url)
            else:
                bad_url = url
                return brand_names, brand_urls, url

            return brand_names, brand_urls, bad_url

        except Exception as er:
            print("Brands are Not Found", er)
            return brand_names, brand_urls, bad_url

    except Exception as error:
        print('Error: in get_brands_and_subcategories()', error)
        return brand_names, brand_urls, bad_url