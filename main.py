import time
import json
import csv

from Get_Brands import get_brands
from Get_Sub_Categories import get_sub_categories
from Get_Products import get_products
from Get_Product_details import get_product_details

main_url = "https://www.mega.pk"

def save_products(cat_name="", sub_cat_name="", brand_name="", product_name="", product_price="", description="", product_image="", product_url="", data=None):
    if data is None:
        data = []

    product_data = {
            "category": f"{cat_name}",
            "subcategory": f"{sub_cat_name}",
            "brand": f"{brand_name}",
            "name": f"{product_name}",
            "price": f"{product_price}",
            "description": f"{description}",
            "image": f"{product_image}",
            "country": "Pakistan",
            "url": f"{product_url}",
            "general":data
    }
    
    # add data to jsonl file
    with open("json_data/data.jsonl", "a", encoding="utf-8") as f:
        json.dump(product_data, f, ensure_ascii=False)
        f.write("\n")
    print("Added data to jsonl file")


if __name__ == "__main__":
    categories = []
    # read categories from csv file
    with open("categories.csv", mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            category_name = row['category_name']
            category_link = row['category_link']
            categories.append((category_name, category_link))
    
    if categories:
        # loop over categories and get brands
        for cat_name, cat_link in categories:
            print("-"*30, f"Category: {cat_name}", "-"*30)

            brand_names, brand_urls, bad_url = get_brands(cat_link)
    
            if brand_urls:
                # loop over each brand url and get data
                for brand_name, brand_url in zip(brand_names, brand_urls):
                    if brand_name == "HP Laptop":
                        continue
                    print("-"*15, f"Brand: {brand_name}", "-"*15)

                    # find all sub_categories
                    sub_cat_names, sub_cat_links = get_sub_categories(brand_url)
                    if sub_cat_links:
                        # loop over each sub category and get products
                        for sub_cat_name, sub_cat_link in zip(sub_cat_names, sub_cat_links):
                            print("-"*10, f"Sub Category: {sub_cat_name}", "-"*10)

                            # get products from sub category
                            product_names, product_urls, product_images, product_prices = get_products(sub_cat_link)
                            print(len(product_names), "Products Found")

                            if product_names:
                                # loop over each product and get details
                                for product_name, product_url, product_image, product_price in zip(product_names, product_urls, product_images, product_prices):
                                    print("-"*5, f"Product: {product_name[:16]}", "-"*5)
                                    time.sleep(1)

                                    # get product details
                                    data, description = get_product_details(product_url)
                                    # save data into jsonl file
                                    save_products(cat_name, sub_cat_name, brand_name, product_name, product_price, description, product_image, product_url, data)

                    else:
                        print("**** Sub Categories are Not Found ****")
                        # get products from brand
                        product_names, product_urls, product_images, product_prices = get_products(brand_url)
                        print(len(product_names), "Products Found")

                        if product_names:
                                # loop over each product and get details
                                for product_name, product_url, product_image, product_price in zip(product_names, product_urls, product_images, product_prices):
                                    print("-"*5, f"Product: {product_name[:16]}", "-"*5)
                                    time.sleep(1)

                                    # get product details
                                    data, description = get_product_details(product_url)
                                    # save data into jsonl file
                                    save_products(cat_name, "", brand_name, product_name, product_price, description, product_image, product_url, data)


            else:
                print("Brands Not Found")
                # find all sub_categories
                sub_cat_names, sub_cat_links = get_sub_categories(cat_link)
                if sub_cat_links:
                    # loop over each sub category and get products
                        for sub_cat_name, sub_cat_link in zip(sub_cat_names, sub_cat_links):
                            print("-"*5, f"Sub Category: {sub_cat_name}", "-"*5)
                            time.sleep(1)

                            # get products from sub category
                            product_names, product_urls, product_images, product_prices = get_products(sub_cat_link)
                            print(len(product_names), "Products Found")

                            if product_names:
                                # loop over each product and get details
                                for product_name, product_url, product_image, product_price in zip(product_names, product_urls, product_images, product_prices):
                                    print("-"*5, f"Product: {product_name[:16]}", "-"*5)
                                    time.sleep(1)

                                    # get product details
                                    data, description = get_product_details(product_url)
                                    # save data into jsonl file
                                    save_products(cat_name, sub_cat_name, "", product_name, product_price, description, product_image, product_url, data)


                else:
                    print("**** Sub Categories are Not Found ****")
                    # get products from category
                    product_names, product_urls, product_images, product_prices = get_products(cat_link)
                    print(len(product_names), "Products Found")

                    if product_names:
                                # loop over each product and get details
                                for product_name, product_url, product_image, product_price in zip(product_names, product_urls, product_images, product_prices):
                                    print("-"*5, f"Product: {product_name[:16]}", "-"*5)

                                    time.sleep(1)

                                    # get product details
                                    data, description = get_product_details(product_url)

                                    # save data into jsonl file
                                    save_products(cat_name, "", "", product_name, product_price, description, product_image, product_url, data)
