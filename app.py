import sys
import os
import json
import threading
from pathlib import Path
from flask import Flask, jsonify, request
from datetime import datetime, timedelta

# === PATH SETUP === #
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))
if str(ROOT_DIR / "level3_automated_hybrid_ingestion") not in sys.path:
    sys.path.append(str(ROOT_DIR / "level3_automated_hybrid_ingestion"))
if str(ROOT_DIR / "core") not in sys.path:
    sys.path.append(str(ROOT_DIR / "core"))
if str(ROOT_DIR / "sites") not in sys.path:
    sys.path.append(str(ROOT_DIR / "sites"))

# === IMPORTS === #
from level3_automated_ingestion(Scraper + APIs).automated_scraper import run_ingestion_cycle

# === FLASK SETUP === #
app = Flask(__name__)

EXPECTED_SECRET = os.environ.get("SCRAPE_SECRET")  # set this in Replit Secrets
LAST_RUN_FILE = ROOT_DIR / "level3_automated_hybrid_ingestion"/ "last_run.json"
RUN_INTERVAL_DAYS = 5  # minimum gap between scrapes

thread_lock = threading.Lock()
is_running = False


# === TIMESTAMP MANAGEMENT === #
def get_last_run():
    """Retrieve last ingestion timestamp."""
    if not LAST_RUN_FILE.exists():
        return None
    try:
        data = json.loads(LAST_RUN_FILE.read_text())
        return datetime.fromisoformat(data["last_run"])
    except Exception:
        return None


def update_last_run():
    """Update the timestamp after successful ingestion."""
    LAST_RUN_FILE.parent.mkdir(parents=True, exist_ok=True)
    LAST_RUN_FILE.write_text(json.dumps({"last_run": datetime.utcnow().isoformat()}))


# === BACKGROUND THREAD FUNCTION === #
def run_and_commit_in_background():
    global is_running
    with thread_lock:
        if is_running:
            print("⚠️ Previous ingestion still running. Skipping new trigger.")
            return
        is_running = True

    try:
        print("\n🚀 [BG_THREAD_START] Automated ingestion triggered...\n")
        run_ingestion_cycle()
        update_last_run()
        print("\n✅ [BG_THREAD_SUCCESS] Ingestion + Commit completed.\n")
    except Exception as e:
        print(f"\n❌ [BG_THREAD_ERROR] Ingestion failed: {e}\n", flush=True)
    finally:
        with thread_lock:
            is_running = False


# === ROUTES === #
@app.route("/")
def home():
    """Shows the server is alive."""
    return jsonify({
        "message": "🧠 Data Ingestion Service Active",
        "status": "running",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }), 200


@app.route("/health")
def health_check():
    """Simple route for UptimeRobot to check server availability."""
    return jsonify({
        "service": "data-ingestion-lab",
        "health": "OK",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }), 200


@app.route("/run-scrape", methods=["POST", "GET"])
def run_ingestion():
    """
    Secure endpoint for triggering ingestion.
    Use a header: X-INGEST-TOKEN: <your-secret>
    """

    # 1. Verify secret
    if not EXPECTED_SECRET:
        print("❌ CONFIG_ERROR: SCRAPE_SECRET is not set.")
        return jsonify({"status": "error", "message": "Server misconfigured"}), 500

    secret = request.headers.get("X-INGEST-TOKEN")
    if secret != EXPECTED_SECRET:
        print("🔒 AUTH_FAILURE: Invalid secret.")
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    # 2. Check if last run was too recent
    last_run = get_last_run()
    if last_run:
        elapsed = datetime.utcnow() - last_run
        if elapsed < timedelta(days=RUN_INTERVAL_DAYS):
            msg = f"⏳ Skipped: Last run {elapsed.days} days ago (needs {RUN_INTERVAL_DAYS}-day gap)"
            print(msg)
            return jsonify({"status": "skipped", "message": msg}), 200

    # 3. Launch background thread
    try:
        print("✅ [REQUEST_SUCCESS] Starting background ingestion...")
        scraper_thread = threading.Thread(target=run_and_commit_in_background)
        scraper_thread.start()

        return jsonify({
            "status": "accepted",
            "message": "Ingestion started in background.",
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }), 202

    except Exception as e:
        print(f"❌ [REQUEST_ERROR] Failed to start thread: {e}\n", flush=True)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🌍 Server running at http://localhost:{port}")
    app.run(host="0.0.0.0", port=port)
