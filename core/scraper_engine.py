from bs4 import BeautifulSoup
import requests
import lxml
import csv
import time
import random

 
# Function to fetch laptop details from Jumia
def fetch_product_from_page(soup, selector):
    # List to store the laptop details
    results = []

    # Enclosing the scraping logic in a try-except block to handle potential errors    
    try: 
        item_info = soup.select(selector["id"]) 
        if not item_info:
            print("No items found on this page.")
            return results
         
        # Loop through each laptop and extract details
        for item in item_info: 
            name = item.select_one(selector["name"]).text
            price = item.select_one(selector["price"]).text
            ratings = item.select_one(selector["ratings"]).text if item.select_one(selector["ratings"]) else "No ratings"   
            link = item.find("a", href=True) 
            link = "https://www.jumia.com.ng" + link['href'] if link else "No link available"
            
            results.append({"Name":name ,"Price": price, "Ratings": ratings,"Description Link": link})  
        
         
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching products details: {e}")
        
         
    return results

# Function which primarily fetches all laptops across all existing pages  
def fetch_all_products(base_url, headers, selector):
    page = 1
    final_results = []
    while True:
        print(f"Scraping page {page}...")

        # Enclosing the request in a try-except block to handle potential errors
        try:
            # Calling the url within the function
            url = f"{base_url}?page={page}"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "lxml")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching page {page}: {e}")
            break    

        product = fetch_product_from_page(soup, selector)  
        if not product:
            print("No more products found for page {product}, ending pagination.") 
            break

        final_results.extend(product)

        next_page = soup.select_one(selector["page_next"])
        if not next_page:
            break   
        page += 1
        time.sleep(random.uniform(5, 10)) # Mickmicking human behavior with random delays between page requests  
    
    print(f"\n📦 Total products scraped: {len(final_results)}")
    return final_results
 
 