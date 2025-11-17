# orchestrator.py
import sys
import argparse
import logging
import json
from pathlib import Path
from datetime import datetime

# Determine the root directory of the project and add it to sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

  
# --- Import jobs ---
from level3_automated_ingestion_cycles.automated_scraper import run_automated_scraper
from level4_api_ingestion_engine.api_ingestor import run_api_ingestion
from level4_api_ingestion_engine.api_auth import run_api_authentication

 
# --- Register jobs ---
JOBS = {
    "Auto_Scraper": run_automated_scraper,
    "API_Ingest": run_api_ingestion,
    "API_Auth": run_api_authentication,
}


# --- Logger ---
logging.basicConfig(
    filename="orchestrator.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger()


# --- Append Single Report (Unified Writer) ---
def append_report(report):
    """Automatically append a single job report to orchestrator_report.json."""
    try:
        with open("orchestrator_report.json") as f:
            existing = json.load(f)
    except:
        existing = []

    existing.append(report)

    with open("orchestrator_report.json", "w") as f:
        json.dump(existing, f, indent=4)


# --- Core Job Runner ---
def run_job(job_name, job_fn=None, retries=1, verbose=False):
    """
    This is the Central job executor.
    Called by:
    - CLI
    - GitHub Actions
    - Flask/Render
    """
    start = datetime.utcnow()
    success = False
    error_message = None

    #This allows Flask to pass only job_name
    if job_fn is None:
        if job_name not in JOBS:
            raise ValueError(f"Unknown job: {job_name}")
        job_fn = JOBS[job_name]

    if verbose:
        print(f"\n▶ Running job: {job_name} (retries={retries})")

    for attempt in range(1, retries + 1):
        try:
            job_fn()
            success = True
            logger.info(f"Job succeeded: {job_name} on attempt {attempt}")
            if verbose:
                print(f"✔ Success on attempt {attempt}")
            break

        except Exception as e:
            error_message = str(e)
            logger.error(f"Attempt {attempt} failed for {job_name}: {e}")
            if verbose:
                print(f"✘ Attempt {attempt} failed: {e}")

    end = datetime.utcnow()

    # Structured JSON report
    report = {
        "job": job_name,
        "success": success,
        "attempts": retries,
        "error": error_message,
        "duration_seconds": (end - start).total_seconds(),
        "timestamp": end.isoformat(),
    }

    # This writes report immediately.
    append_report(report)

    return report


# --- CLI Orchestrator ---
def main():
    parser = argparse.ArgumentParser(description="Clean Orchestrator")
    parser.add_argument("-job", type=str, help="Job to run")
    parser.add_argument("-all", action="store_true", help="Run all jobs")
    parser.add_argument("-verbose", action="store_true")
    parser.add_argument("-retries", type=int, default=1)
    args = parser.parse_args()

    # Run all jobs
    if args.all:
        for name, fn in JOBS.items():
            run_job(name, fn, args.retries, args.verbose)

    # Run one job
    elif args.job:
        if args.job not in JOBS:
            print(f"Unknown job: {args.job}")
            print(f"Available: {list(JOBS.keys())}")
            return

        run_job(args.job, JOBS[args.job], args.retries, args.verbose)

    else:
        print("Specify either -job <name> OR -all")
        return

    if args.verbose:
        print("\n📁 JSON report updated: orchestrator_report.json\n")


if __name__ == "__main__":
    main()
