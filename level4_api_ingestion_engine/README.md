# 🔹 Level 4 — API Ingestion Engine
 
**Level 4 — API Ingestion Engine** marks the transition from manual or web-based extraction to **programmatic data ingestion through authenticated APIs**.  
This module establishes the backbone of scalable, secure, and automated data pipelines by integrating API authentication, structured data extraction, and efficient transformation workflows.

It is part of the broader **Data Ingestion Lab**, a multi-phase system design experiment that evolves from simple static scrapers into fully autonomous ingestion engines.

---

## 🧠 Core Objectives

- Implement **authenticated API connections** (API key / token-based).
- Handle **multiple endpoints** with flexible parameters.
- Introduce **automated data refresh logic** and error recovery.
- Normalize **JSON → tabular datasets**.
- Log operations and **maintain ingestion integrity**.

---

## 🧩 System Architecture

```mermaid
graph TD
    A[API Endpoint(s)] -->|HTTP Requests| B[Auth Layer (.env)]
    B --> C[API Ingestion Engine]
    C --> D[Data Normalization (pandas)]
    D --> E[Storage Layer (CSV/JSON)]
    E --> F[Logging & Reports]
```

## 🧱 Directory Structure

📦 level4_api_ingestion_engine/
 ┣ 📜 api_ingestor.py        → Core data fetching & normalization logic
 ┣ 📜 api_auth.py            → Authentication and key management
 ┣ 📜 requirements.txt       → Module dependencies
 ┣ 📂 data/                  → Local storage for extracted datasets
 ┗ 📜 README.md              → Module documentation (you’re reading this)
 

## 🔐 Authentication Layer

- API keys and tokens are securely managed through a .env file.
- The ingestion engine loads credentials using the python-dotenv library.
- This ensures that no sensitive keys are exposed in public repositories.
  

## 🧩 Context in the Roadmap
Level	- Description
Level 1	- Single-page web scraper (static extraction)
Level 2	- Multi-page crawler (pagination & traversal)
Level 3	- Automated ingestion cycles (scheduled data refresh)
👉 Level 4	- API Ingestion Engine (authenticated, programmatic extraction)
Level 5	- Full orchestration (autonomous ingestion system)  


## 📚 Learning Value 
This module demonstrates practical mastery of:
- Real-world API integration
- Authentication management
- Resilient data pipeline design
- Scalable system modularization
It validates readiness for professional data engineering and automation roles.

## 🧠 Author
Charles Onokohwomo : Data Scientist • Technologist • Data System Architect
 
