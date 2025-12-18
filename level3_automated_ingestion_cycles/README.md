## 🧠 Level 3 – Automated Ingestion cycles (scheduled data refresh)

This level marks the evolution from a simple HTML crawler into a autonomous ingestion system — capable of fetching data from different web sources (HTML scraping) and then intelligently produces a refreshing datasets on a fixed schedule.

The automation pipeline runs every 5 days via GitHub Actions & Render, it fetches and delivers data from multiple ingestion layers, and commits updates directly to this repository — creating a continuously self-refreshing data engine.

--------

## ⚙️ Core Concept

Objective:
Design a self-sustaining ingestion pipeline intelligently fetches data via web scraping (without APIs) into a distinct dataset.

At this stage, the system demonstrates true autonomy and resilience — updating itself without manual triggers, managing versioned data persistence, and maintaining a living dataset repository.

This is a key milestone toward a fully orchestrated ingestion engine (Level 5).

----------

## 🧩 Project Structure
``` bash
data-ingestion-lab/
│
├── core/
│   ├── __init__.py
│   ├── scraper_engine.py          # Reusable scraping logic (HTML)
│    
│
├── sites/
│   ├── categories.json            # Category mapping for scraping endpoints
│   ├── jumia_config.py            # Site-specific scraping configs (selectors, headers)
│
├── level3_automated_ingestion_cycles/
│   ├── __init__.py        
│   ├── automated_scraper.py       # Carries out the html webscraping
│   └── README.md                  # You are here
│
└── render_app.py 
      
```

------------

## 🧠 Workflow Logic
1. Ingestion Engines

scraper_engine.py — Handles HTML-based extraction via BeautifulSoup and requests.

This returns a standardized DataFrames.  

2. Configuration Layer

categories.json — Defines multiple category endpoints for web scraping.
 
config.py — Custom rules for scraping (headers, base URLs, selectors).

3. Automation & Scheduling

HTML Scraper: Hosted on Render, triggered automatically by UptimeRobot pings to maintain dataset freshness without relying on paid background workers.
 
```bash 
                |
                v
+-------------------------------+
| 🕸️ Render + UptimeRobot       |
| Runs periodically or pinged   |
| Executes automated_scraper.py |
| Commits scraper_dataset.csv   |
+-------------------------------+

This produces a CSV dataset in the repo:

level3_automated_ingestiion_cycles/
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
- render
- flask

----------

## 🚀 How It Works

- **Configuration** — Define endpoints in categories.json (HTML)  

- **Run Locally (optional)** — python level3_automated_ingestion_cycles/automated_scraper.py    
 
- **Automated Mode (default)** — The Render cloud (render_app.py) triggers every 24hrs, which then carries out the execution, uptime robot pings the render webservice every 5mins to prevent downtime, after successful process run the commits are then automatically saved.

--------

## 📈 Expected Output

✅ Unified ingestion pipeline   
✅ Full automation via Render & Uptime Robot
✅ Version-controlled, self-sustaining data pipeline
✅ Scalable architecture for future orchestration (Level 5)

---------- 

## Author: Charles Onokohwomo 

**Project: Data Ingestion Lab (ADIP Series)**
