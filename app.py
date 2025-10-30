from flask import Flask
import threading
import os
from level3_automated_ingestion_cycles.automated_scraper import run_ingestion_cycle, commit_data_to_git

app = Flask(__name__)

@app.route('/')
def home():
    return "🧠 Scraper service is live."

@app.route('/run')
def trigger_scraper():
    def background_job():
        run_ingestion_cycle()
        commit_data_to_git()
    threading.Thread(target=background_job).start()
    return "🚀 Scraper job started in background."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port) 