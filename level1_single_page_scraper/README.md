# Level 1 — Static Web Scraper (Jumia website reference)

This Level 1 phase introduces the foundational layer of **web intelligence ingestion** — a **single-page static web scraper** designed to extract structured information from the Jumia laptops category.

It uses **BeautifulSoup** and **Requests** to capture key product attributes such as:
- Laptop name  
- Price  
- Ratings  
- Product link  

and exports them into a structured **CSV dataset** for downstream processing.

---

## ⚙️ Technical Overview

**Language:** Python  
**Libraries:** `requests`, `bs4`, `html5lib`, `csv`, `time`

**Features:**
- Clean modular functions (`fetch_laptop_details`, `save_to_csv`)
- DRY principle via selector mapping
- Header-based anti-bot detection evasion
- CSV export for structured datasets
- Time-based loop for re-execution every 5 minutes (simulated automation)

---

## 🧭 Execution

```bash
python webscrapper.py

Then enter the laptop specification you want to search for, e.g.:

Enter the laptop specification you want to search for: hp dell

The scraper will extract relevant listings, print them to console, and save the structured results in laptop.csv.

🧱 Output Example
Laptop Name	Price	Ratings	Description Link
HP 250 G8	₦450,000	★★★★☆	https://www.jumia.com.ng/hp-250-g8-
...
Dell Latitude 3420	₦510,000	No ratings	https://www.jumia.com.ng/dell-latitude-
...
```

#🧩 Next Level Preview
Level 2 will extend this foundation into multi-page crawling, traversing paginated content dynamically to capture complete category datasets.
 
