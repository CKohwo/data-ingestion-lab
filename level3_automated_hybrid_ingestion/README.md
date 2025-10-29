## 🧠 Level 3 – Automated Ingestion cycles (Scheduled Scrapper)

This level marks the evolution from a simple HTML crawler into a hybrid, autonomous ingestion system — capable of fetching data from both web sources (HTML scraping) and structured APIs, then intelligently produces a refreshing datasets on a fixed schedule.

The automation pipeline runs every 5 days via GitHub Actions, fetches and delivers data from multiple ingestion layers, and commits updates directly to this repository — creating a continuously self-refreshing data engine.

--------

## ⚙️ Core Concept

Objective:
Design a self-sustaining ingestion pipeline that intelligently blends web scraping (for data without APIs) and API-based retrieval (for structured or rate-limited data) into a two distinct dataset.

At this stage, the system demonstrates true autonomy and resilience — updating itself without manual triggers, managing versioned data persistence, and maintaining a living dataset repository.

This is a key milestone toward a fully orchestrated ingestion engine (Level 4).

----------

## 🧩 Project Structure
``` bash
data-ingestion-lab/
│
├── core/
│   ├── __init__.py
│   ├── scraper_engine.py          # Reusable scraping logic (HTML)
│   ├── api_engine.py              # Reusable API ingestion logic
│
├── sites/
│   ├── categories.json            # Category mapping for scraping endpoints
│   ├── api_sources.json           # List of public or structured API endpoints
│   ├── jumia_config.py            # Site-specific scraping configs (selectors, headers)
│
├── level3_automated_hybrid_ingestion/
│   ├── automated_scraper.py       # Carries out the html webscraping  
│   ├── api_ingestor.py            # API ingestion script 
│   ├── scraper_dataset.csv        # Auto-generated scraper dataset
│   ├── api_dataset.csv            # Auto-saved dataset extracted via Api       
│   └── README.md                  # You are here
│
└── .github/
    └── workflows/
        └── auto_ingest.yml        # Scheduler (GitHub Actions)
```

------------

## 🧠 Workflow Logic
1. Ingestion Engines

scraper_engine.py — Handles HTML-based extraction via BeautifulSoup and requests.

api_engine.py — Pulls structured data from REST APIs, handling pagination and response normalization.

Both engines return standardized DataFrames.  

2. Configuration Layer

categories.json — Defines multiple category endpoints for web scraping.

api_sources.json — Lists active API sources (e.g., exchange rates, products, market data).

config.py — Custom rules for scraping (headers, base URLs, selectors).

3. Automation & Scheduling

API Ingestion: Executes via GitHub Actions every 5 days. Lightweight, predictable, and version-controlled.

HTML Scraper: Hosted on Render, triggered automatically by UptimeRobot pings to maintain dataset freshness without relying on paid background workers.
 
```bash

+-------------------------------+
| 🧠 GitHub Actions Scheduler   |
| Runs every 5 days             |
| Executes api_ingestor.py      |
| Commits api_dataset.csv       |
+---------------+---------------+
                |
                v
+-------------------------------+
| 🕸️ Render + UptimeRobot       |
| Runs periodically or pinged   |
| Executes automated_scraper.py |
| Commits scraper_dataset.csv   |
+-------------------------------+

Both feed separate CSV datasets in the repo:

level3_automated_hybrid_ingestion/
├── api_dataset.csv
├── scraper_dataset.csv
```
---------

## 🛠️ Tech Stack
**Component	Purpose**
- Python 3.x	Core automation language
- Requests	HTTP requests for both API + HTML ingestion
- BeautifulSoup (lxml)	HTML parsing
- Pandas	Data transformation, merging, deduplication
- JSON	Configuration for endpoints and API mappings
- GitHub Actions	CI/CD automation & scheduling

----------

## 🚀 How It Works

- **Configuration** — Define endpoints in categories.json (HTML) and api_sources.json (API).

- **Run Locally (optional)** — python level3_automated_hybrid_ingestion/automated_scraper.py or python level3_automated_hybrid_ingestion/api_ingestor.py
 
- **Automated Mode (default)** — GitHub Actions triggers ingestion every 5 days, executing both engines and committing updates automatically.

--------

## 📈 Expected Output

✅ Unified ingestion pipeline (API + Scraper)
✅ Two different dataset refreshed automatically
✅ Full automation via GitHub Actions
✅ Version-controlled, self-sustaining data pipeline
✅ Scalable architecture for future orchestration (Level 5)

----------

## 🧭 Next Step: Level 4 – Orchestrated Intelligence

The next level transitions from hybrid ingestion to orchestration and insight automation, where the system doesn’t just collect data — it interprets, summarizes, and generates human-readable analytical insights automatically.
-----------

## Author: Charles Onokohwomo 

**Project: Data Ingestion Lab (ADIP Series)**
