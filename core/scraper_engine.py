from bs4 import BeautifulSoup
import requests
import html5lib
import csv
import time

base_url = "https://www.jumia.com.ng/laptops/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64), AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}

# Define the laptop selectors inorder to prevent hardcoding and follow the DRY principle
# Added selector for pagination  
selector = {
     "laptop_card": "article.prd._fb.col.c-prd",
     "name": "h3.name",
     "price": "div.prc",
     "ratings": "div.stars._s",  
     "page_next":"a.pg[aria-label='Next Page']"    
}  
         
response = requests.get(base_url, headers=headers)  
soup = BeautifulSoup(response.text, "html5lib")

# Function to fetch laptop details from Jumia
def fetch_product_from_page(soup, selector, search_item):
    try: 
        laptop_info = soup.select(selector["laptop_card"])  
        # List to store the laptop details
        results = []
        
        # Loop through each laptop and extract details
        for laptop in laptop_info: 
            laptop_name = laptop.select_one(selector["name"]).text
            
            if any(item in laptop_name.lower() for item in search_item):   
                price = laptop.select_one(selector["price"]).text
                ratings = laptop.select_one(selector["ratings"]).text if laptop.select_one(selector["ratings"]) else "No ratings"   
                link = laptop.find("a", href=True) 
                link = "https://www.jumia.com.ng" + link['href'] if link else "No link available"
                results.append({"Name":laptop_name ,"Price": price, "Ratings": ratings,"Description Link": link})  
        
        return results 
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching laptop details: {e}")
        
        return[] #This returns an empty list if there is an error 


# Function which primarily fetches all laptops across all existing pages  
def fetch_all_products(base_url, headers, selector, search_item):
    page = 1
    final_results = []
    while True:
        print(f"Scraping page {page}...")

        # Enclosing the request in a try-except block to handle potential errors
        try:
            # Calling the url within the function
            url = f"{base_url}?page={page}"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html5lib")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching page {page}: {e}")
            break    

        product = fetch_product_from_page(soup, selector, search_item)
        if not product:
            break
        final_results.extend(product)

        next_page = soup.select_one(selector["page_next"])
        if not next_page:
            break   
        page += 1
        time.sleep(5)  # Be polite and avoid overwhelming the server
    
    return final_results
 


# Function to save the laptop details to a CSV file
def save_to_csv(product, filename):

    # For now I will utilize the write(w) functionality, but in future I can implement the append(a)  
    with open("sample.csv", "w", newline="", encoding='utf-8') as file:
        fieldnames = ["Name", "Price", "Ratings", "Description Link"] 
        writer = csv.DictWriter(file, fieldnames=fieldnames) 
        writer.writeheader() 
        writer.writerows(product)
        
    print("Laptop details saved to sample.csv")
   

# Main function to run the script periodically
def main():
    search_item = input("Enter the laptop specification you want to search for: ").lower().strip().split() 
    while True:
        final_outputs = fetch_all_products(base_url, headers, selector, search_item)
        if final_outputs:
            save_to_csv(final_outputs, "sample.csv")
        else:   
            print("No product found matching the specified criteria.")
        time.sleep(300)  # Wait for 5 minutes before the next check
        print("waiting for 5 minutes...")
          
if __name__  == "__main__":
    main()   
