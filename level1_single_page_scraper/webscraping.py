from bs4 import BeautifulSoup
import requests
import html5lib
import csv
import time

jumia_url = "https://www.jumia.com.ng/laptops/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64), AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}

# Define the laptop selectors inorder to prevent hardcoding and follow the DRY principle
Selector = {
     "laptop_card": "article.prd._fb.col.c-prd",
     "name": "h3.name",
     "price": "div.prc",
     "ratings": "div.stars._s"     
}  
         

# Function to fetch laptop details from Jumia
def fetch_laptop_details(search_item):
    try:
        response = requests.get(jumia_url, headers=headers)  
        soup = BeautifulSoup(response.text, "html5lib")
         
        laptop_info = soup.select(Selector["laptop_card"])  
        # List to store the laptop details
        results = []
        
        # Loop through each laptop and extract details
        for laptop in laptop_info: 
            laptop_name = laptop.select_one(Selector["name"]).text
            if any(item in laptop_name.lower() for item in search_item):   
                price = laptop.select_one("div", class_ = "prc").text
                ratings = laptop.select_one("div", class_ = "stars _s").text if laptop.find("div", class_ = "stars _s") else "No ratings"   
                link = laptop.find("a", href=True) 
                link = "https://www.jumia.com.ng" + link['href'] if link else "No link available"
                results.append({"Laptop Name":laptop_name ,"Price": price, "Ratings": ratings,"Description Link": link})  
        
        return results 
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching laptop details: {e}")
        return[] #This returns an empty list if there is an error 

# Function to save the laptop details to a CSV file
def save_to_csv(laptops, filename):
    with open("laptop.csv", "w", newline="", encoding='utf-8') as file:
        fieldnames = ["Laptop Name", "Price", "Ratings", "Description Link"] 
        writer = csv.DictWriter(file, fieldnames=fieldnames) 
        writer.writeheader() 
        writer.writerows(laptops)
    print("Laptop details saved to laptop.csv")
    print("waiting for 5 minutes...")


# Main function to run the script periodically
def main():
    search_item = input("Enter the laptop specification you want to search for: ").lower().strip().split() 
    while True:
        laptops = fetch_laptop_details(search_item)
        if laptops:
            save_to_csv(laptops, "laptop.csv")
        else:   
            print("No laptops found matching the specified criteria.")
        time.sleep(300)  # Wait for 5 minutes before the next check
        print("waiting for 5 minutes...")
          
if __name__  == "__main__":
    main() 