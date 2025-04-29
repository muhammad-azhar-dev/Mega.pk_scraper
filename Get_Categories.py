from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup

# This function will get all categories from the main page of Mega.pk
# It will return a list of all categories names, links and images
def get_all_categories(Proxies):
    all_categories_name = []
    all_categories_link = []
    all_categories_img = []
    try:
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random,
        }
        RandomProxy = random.choice(Proxies)
        response = requests.get(main_url, proxies={RandomProxy[1]: RandomProxy[0]}, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all category
        all_categories = soup.find_all('a', attrs={'class': 'home-cat-link'})
        if all_categories:
            for category in all_categories:
                cat_link = category.get('href')
                cat_name = category.find('h3').get_text().strip()
                cat_img_data = category.find('img').get('src')
                if cat_img_data.startswith('http'):
                    cat_img = cat_img_data
                else:
                    cat_img = f"{main_url}/{cat_img_data}"

                # add category to list
                all_categories_name.append(cat_name)
                all_categories_link.append(cat_link)
                all_categories_img.append(cat_img)

        return all_categories_name, all_categories_link, all_categories_img

    except Exception as error:
        print(f"Error: in get_all_categories: {error}")
        return all_categories_name, all_categories_link, all_categories_img