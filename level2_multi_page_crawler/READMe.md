# ⚡ Level 2 — Multi-Page Crawling System  
**Repository:** `data-ingestion-lab`  
**Version:** `v2.0.0`  
**Status:** ✅ Completed  

---

## 🚀 Overview  
This level upgrades the **Level 1 Single-Page Crawler** into a **fully functional multi-page scraping system**.  
It automatically navigates through paginated results on **Jumia Nigeria**, collecting laptop product data across all available pages.

The system demonstrates:  
- ✅ Pagination awareness  
- ✅ Clean modular function structure  
- ✅ Resilient error handling  
- ✅ Polite crawling with timed delays  
- ✅ Automated CSV export  

This marks a critical step in transitioning from static scraping to a continuous, scalable ingestion workflow.

---

## ⚙️ Core Workflow  

| Stage | Description |
|:------|:-------------|
| **1 — Input Specification** | User inputs desired laptop specs (e.g., “hp core i5”). |
| **2 — HTML Retrieval** | Script sends HTTP requests to the Jumia laptops category, page by page. |
| **3 — Data Extraction** | For each product card: name, price, ratings, and product link are captured. |
| **4 — Pagination Loop** | The crawler checks for the “Next Page” button and continues until exhausted. |
| **5 — CSV Export** | All results are stored in `sample.csv`. |
| **6 — Auto-Refresh Loop** | Every 5 minutes, the script re-runs and refreshes data (demonstrating periodic ingestion). |

---

## 🧩 File Structure  

```bash
data-ingestion-lab/
└── level2_multi_page_crawler/
    ├── multi_page_scraper.py
    ├── sample.csv
    └── README.md
```

## 🧠 Key Functions
|Function | Purpose
|:------|:-------------|
|fetch_laptop_from_page(soup, selector, search_item) | Extracts laptops from a single HTML page.|
|fetch_all_laptops(base_url, headers, selector, search_item) | Loops through all pages and aggregates data.|
|save_to_csv(laptops, filename) | Saves structured output into a CSV file.|
|main() | Orchestrates the entire flow, manages timing and user input.|

##🧪 Usage
▶ Run Script
python multi_page_scraper.py

💬 Example Prompt
Enter the laptop specification you want to search for: hp core i7

📄 Output

sample.csv — containing structured columns:

Laptop Name

Price

Ratings

Description Link

🧱 Core Technologies
Library	Purpose
requests	For HTTP requests
BeautifulSoup4 + html5lib	For HTML parsing
csv	For structured data export
time	For crawl delays

## ⚖️ Error Handling & Crawl Ethics

- Automatic retries and graceful error handling

- 10-second delay between pages to reduce load

- 5-minute interval between full runs for sustainability

- Configurable headers and base URL for portability

 
## 🌱 Next Milestone — Level 3: Modularization

Level 3 will transform this crawler into a modular scraping architecture, introducing:

- core/ → reusable scraping engine

- sites/ → domain-specific configs (selectors, URLs, headers)

- Multi-site ingestion capabilities

- CLI & automation-ready interface

## 🧭 Version History
Version	Update	Description
v1.0.0	Initial Crawler	Single-page extraction working
v2.0.0	Pagination Upgrade	Multi-page support + CSV integration 


## ✍️ Author

Charles Onokohwomo - Technologist • Data Scientist • AI & Systems Engineer 
