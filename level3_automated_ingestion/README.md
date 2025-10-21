
# 🧠 Level 3 – Automated Ingestion cycles (Scheduled Data Refresh)

This level marks the **evolution from a simple crawler to an intelligent ingestion system** that autonomously collects, merges, and refreshes data at scheduled intervals.  
The automation pipeline runs every **5 days**, fetches data, then merges them into a single dataset, and committs updates directly to this repository.

---

## ⚙️ Core Concept

> **Objective:** Build a self-updating data pipeline that automatically scrapes, merges, and commits data on a schedule.

At this stage, I’ve introduced **automation** and **data persistence** — the system now lives independently, updating itself without human intervention.  
It’s a critical step toward a **fully orchestrated ingestion engine** (Level 5).

---

## 🧩 Project Structure

```bash
data-ingestion-lab/
│
├── core/
│   ├── __init__.py
│   └── scraper_engine.py          # Reusable scraping logic
│
├── sites/
    ├── categories.json            # JSON mapping for multiple category URLs
│   ├── jumia_config.py            # Site-specific settings: selectors, headers, base URL
│
├── level3_automated_ingestion/
│   ├── orchestrator.py            # Controls the full ingestion cycle
│   ├── ecommerce_data.csv         # Auto-generated dataset saved in csv format (merged results)
│   └── README.md                  # You are here
│
└── .github/
    └── workflows/
        └── auto_ingest.yml        # GitHub Action for scheduled runs

```

## 🧠 Workflow Logic

Scraper Engine (core/)

Contains reusable scraping and pagination logic.

Designed to be modular and portable for future site additions.

Site Configuration (sites/)

jumia_config.py → defines base URL, headers, and CSS selectors.

categories.json → lists each data endpoint to crawl automatically.
Example:

{
  "laptops": "https://www.jumia.com.ng/laptops/",
  "gaming": "https://www.jumia.com.ng/gaming/",
  "accessories": "https://www.jumia.com.ng/computing-accessories/"
}

---

## Orchestrator (orchestrator.py)

- Reads all category URLs from categories.json.

- Iterates through each category and scrapes data using scraper_engine.py.

- Merges all results into a unified DataFrame.

- Checks if a previous dataset exists:

- If no file or empty file → creates a new dataset.

- If file exists → merges, removes duplicates, and updates.

- Saves everything to ecommerce_data.csv.

- Automation Layer (GitHub Actions)

- Runs every 5 days automatically.

- Executes the orchestrator.

- Commits and pushes new data back to the repo.

-------------
## 🛠️ Tech Stack
Component	Purpose
Python 3.x	Core automation language
Requests	HTTP requests
BeautifulSoup (lxml)	HTML parsing
Pandas	Data merging & deduplication
JSON	Category configuration mapping
GitHub Actions	CI/CD automation & scheduling
🚀 How It Works

**Category Configuration:**
Add or remove the data you want to scrape inside sites/categories.json.

**Run Locally (optional):** 
python level3_automated_ingestion/orchestrator.py
 
**Automated Mode (default):**
GitHub Actions executes the ingestion every 5 days automatically and commits the latest data to your repo.

--------------

## 📈 Expected Output

✅ Multi-category scraping (laptops, gaming, accessories, etc.)

✅ Unified dataset (ecommerce_data.csv) refreshed every 5 days

✅ Full automation via GitHub Actions

✅ Demonstrates modular, scalable, and professional data pipeline design

-------------

## 🧭 Next Step: Level 4 – Hybrid Ingestion

Transition from HTML-based scraping to a hybrid ingestion model that combines both API endpoints and web scraping, intelligently switching between them for efficiency, reliability, and fault tolerance.

---------

## Author: Charles Onokohwomo 
## Phase: Level 3 – Automated Ingestion 
## Project: Data Ingestion Lab (ADIP Series) 
