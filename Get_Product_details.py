from fake_useragent import UserAgent
from selenium import webdriver
import time
from bs4 import BeautifulSoup

def get_product_details(url):
    product_details = []
    product_description = ""
    
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

        # --------- Extract product description ------------------
        try:
            product_description = soup.find("p", class_="item_desc").get_text().strip()
        except Exception:
            pass

        # --------- Extract product detail table -----------------
        try:
            main_table = soup.find("table", attrs={"id": "laptop_detail"})
            current_section = None
            current_data = []

            for tr in main_table.find_all("tr"):
                # Check if it's a new section header
                heading = ""
                try:
                    heading = tr.find("th", class_="h2").get_text().strip()
                except Exception:
                    pass

                if heading:
                    # Save the last section before starting new one
                    if current_section:
                        product_details.append({
                            "section": current_section,
                            "data": current_data
                        })
                    current_section = heading
                    current_data = []
                    continue  # Skip to next row for data

                # Try getting name-value pair
                try:
                    tds = tr.find_all("td")
                    if len(tds) >= 1:
                        name = tds[0].get_text().strip()
                        value = tds[1].get_text().strip() if len(tds) > 1 else ""
                        current_data.append([name, value])
                except Exception:
                    pass

            # Append the last section
            if current_section:
                product_details.append({
                    "section": current_section,
                    "data": current_data
                })

        except Exception as e:
            print(f"Error in product detail table: {e}")

        return product_details, product_description

    except Exception as e:
        print(f"Driver error: {e}")
        return product_details, product_description