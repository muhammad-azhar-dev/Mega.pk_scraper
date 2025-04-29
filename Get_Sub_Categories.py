from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium import webdriver
import time

def get_sub_categories(url):
    sub_cat_names = []
    sub_cat_links = []
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

        # find all sub categories
        try:
            # Find all divs with class containing 'sub-cat'
            sub_cat_divs = soup.find_all('div', class_='sub-cat')
            # Filter out any that also have 'row' in their class list
            for div in sub_cat_divs:
                class_list = div.get('class', [])
                if 'row' not in class_list:
                    sub_cat_div = div
                    break

            all_anchor_tags = sub_cat_div.find_all('a')
            print('Sub Categories Found')

            for anchor_tag in all_anchor_tags:
                sub_cat_link = anchor_tag.get('href')
                sub_cat_name_data = anchor_tag.get_text().strip()
                sub_cat_span = anchor_tag.find('span').get_text().strip()
                if sub_cat_span in sub_cat_name_data:
                    sub_cat_name = sub_cat_name_data.replace(sub_cat_span, "", 1).strip()
                
                if sub_cat_span == "0":
                    pass 
                else:
                    sub_cat_names.append(sub_cat_name)
                    sub_cat_links.append(sub_cat_link)  

            return sub_cat_names, sub_cat_links

            
        except Exception as er:
            print('Sub Category Not Found', er)
            return sub_cat_names, sub_cat_links


    except Exception as error:
        print("Error: in get_sub_categories()", error)
        return sub_cat_names, sub_cat_links