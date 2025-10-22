import sys
import os
import threading
from pathlib import Path
from flask import Flask, jsonify, request, abort
from datetime import datetime

# === Dynamic Import Setup === #
# (Your path setup is good and explicit)
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))
if str(ROOT_DIR / "level3_automated_ingestion") not in sys.path:
    sys.path.append(str(ROOT_DIR / "level3_automated_ingestion"))
if str(ROOT_DIR / "core") not in sys.path:
    sys.path.append(str(ROOT_DIR / "core"))
if str(ROOT_DIR / "sites") not in sys.path:
    sys.path.append(str(ROOT_DIR / "sites"))

# === Imports from your ingestion system === #
from level3_automated_ingestion.orchestrator import run_ingestion_cycle

# === Flask Setup === #
app = Flask(__name__)

# Get the secret key from Replit Secrets
EXPECTED_SECRET = os.environ.get("SCRAPE_SECRET")

# === Background Worker Function === #
def run_and_commit_in_background():
    """
    This is the wrapper that runs in a separate thread.
    It contains the full, long-running logic.
    """
    try:
        print("\n🚀 [BG_THREAD_START] Automated ingestion triggered...\n")
        
        # We only need to call the one orchestrator function,
        # since it's designed to handle the commit internally.
        run_ingestion_cycle() 

        print("\n✅ [BG_THREAD_SUCCESS] Ingestion + Commit completed.\n")

    except Exception as e:
        print(f"\n❌ [BG_THREAD_ERROR] Ingestion failed: {e}\n", flush=True)


# === Flask Endpoints === #
@app.route("/")
def home():
    """Shows the server is alive."""
    return jsonify({
        "message": "🧠 Data Ingestion Service",
        "status": "running",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }), 200


@app.route("/health")
def health_check():
    """Simple route for UptimeRobot to check that the server is alive."""
    return jsonify({
        "service": "data-ingestion-lab",
        "health": "OK",
    }), 200


@app.route("/run-scrape")
def run_ingestion():
    """
    This is the *secure* endpoint that UptimeRobot will ping.
    It validates a secret and then starts the job in a background thread.
    """
    # 1. Check for Server-Side Configuration
    if not EXPECTED_SECRET:
        print("❌ CONFIG_ERROR: SCRAPE_SECRET is not set in environment.")
        return jsonify({"status": "error", "message": "Server configuration error"}), 500

    # 2. Check for Client-Side Secret
    secret = request.args.get('secret')
    if secret != EXPECTED_SECRET:
        print(f"🔒 AUTH_FAILURE: Invalid secret key provided.")
        return jsonify({"status": "error", "message": "Invalid authentication secret"}), 403

    # 3. Start the job in the background
    try:
        print("✅ [REQUEST_SUCCESS] Auth successful. Starting background thread...")
        
        # Create and start the background thread
        scraper_thread = threading.Thread(target=run_and_commit_in_background)
        scraper_thread.start()

        # 4. Return an immediate "Accepted" response
        return jsonify({
            "status": "accepted",
            "message": "Ingestion job started in background.",
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }), 202

    except Exception as e:
        print(f"❌ [REQUEST_ERROR] Failed to start thread: {e}\n", flush=True)
        return jsonify({"status": "error", "message": f"Failed to start thread: {e}"}), 500


if __name__ == "__main__":
    # Flask will bind to port 8080 on Replit
    port = int(os.environ.get("PORT", 8080))
    print(f"🌍 Server running at http://localhost:{port}")
    app.run(host="0.0.0.0", port=port)