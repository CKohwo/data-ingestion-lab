# orchestrator.py

import argparse
import logging
import json
from datetime import datetime


# --- Import jobs ---
from level4_api_ingestion_engine.api_ingestor import run_api_ingestion  
from level4_api_ingestion_engine.api_auth import run_api_authentication


# --- Register jobs ---
JOBS = {
    "API_Ingestion": run_api_ingestion,
    "API_Auth": run_api_authentication,
}


# --- Logger ---
logging.basicConfig(
    filename="orchestrator.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger()


# --- Simple job runner with retries + JSON report ---
def run_job(job_name, job_fn, retries=1, verbose=False):
    start = datetime.utcnow()
    success = False
    error_message = None

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

    return {
        "job": job_name,
        "success": success,
        "attempts": retries,
        "error": error_message,
        "duration_seconds": (end - start).total_seconds(),
        "timestamp": end.isoformat(),
    }


def save_report(reports):
    """Append run reports to a single JSON file."""
    try:
        existing = json.load(open("orchestrator_report.json"))
    except (FileNotFoundError, json.JSONDecodeError):
        existing = []

    existing.extend(reports)

    with open("orchestrator_report.json", "w") as f:
        json.dump(existing, f, indent=4)


def main():
    parser = argparse.ArgumentParser(description="Clean Orchestrator")
    parser.add_argument("--job", type=str, help="Job to run")
    parser.add_argument("--all", action="true", help="Run all jobs")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--retries", type=int, default=1)
    args = parser.parse_args()

    reports = []

    # run all jobs
    if args.all:
        for name, fn in JOBS.items():
            report = run_job(name, fn, args.retries, args.verbose)
            reports.append(report)

    # run single job
    elif args.job:
        if args.job not in JOBS:
            print(f"Unknown job: {args.job}")
            print(f"Available: {list(JOBS.keys())}")
            return

        report = run_job(args.job, JOBS[args.job], args.retries, args.verbose)
        reports.append(report)

    else:
        print("Specify either: --job <name> OR --all")
        return

    save_report(reports)
    if args.verbose:
        print("\n📁 JSON report updated: orchestrator_report.json\n")


if __name__ == "__main__":
    main()
