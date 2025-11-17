from flask import Flask, request
import threading
import os
from level5_full_orchestration.orchestrator import run_job, JOBS

app = Flask(__name__)

@app.route("/")
def home():
    return "🧠 Orchestrator Service Live. Use /run?job=JOB_NAME"

def background_runner(job_name):
    try:
        print(f"[RUNNER] Starting job: {job_name}")

        job_fn = JOBS.get(job_name)
        if job_fn is None:
            print(f"Error, unknown job {job_name}")
            return
            
        run_job(job_name,job_fn, retries=1, verbose=True) 
        print(f"[RUNNER] Completed job: {job_name}")

    except Exception as e:
        print(f"[ERROR] Job {job_name} failed: {e}")

@app.route("/run")
def run_any_job():
    job = request.args.get("job")

    if not job:
        return "❌ No job specified. Use /run?job=JOB_N AME", 400

    # Start background execution
    threading.Thread(target=background_runner, args=(job,)).start()

    return f"🚀 Job '{job}' started in background."

@app.route("/run/all")
def run_all_jobs():
    jobs = list(JOBS.keys())  # modify as needed

    def run_all():
        for job in jobs:
            print(f"[ALL] Running job: {job}")
            run_job(job, JOBS[job], retries=1, verbose=True)

    threading.Thread(target=run_all).start()

    return "🚀 Running all jobs in background."

 

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
