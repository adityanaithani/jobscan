import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


CACHE_DIR = (
    Path("/app/data")
    if Path("/app/data").exists()
    else Path(__file__).parent.parent / "data"
)
CACHE_FILE = CACHE_DIR / "posted_jobs.json"


def _ensure_cache_dir():
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_cache():
    _ensure_cache_dir()

    if not CACHE_FILE.exists():
        return {"posted_jobs": {}}

    try:
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)

        cutoff = datetime.now(timezone.utc) - timedelta(hours=48)
        posted_jobs = cache.get("posted_jobs", {})

        cleaned = {
            job_id: timestamp
            for job_id, timestamp in posted_jobs.items()
            if datetime.fromisoformat(timestamp) > cutoff
        }

        return {"posted_jobs": cleaned}
    except (json.JSONDecodeError, KeyError, ValueError):
        return {"posted_jobs": {}}


def save_cache(cache):
    _ensure_cache_dir()
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def is_posted(job_id, hours=24):
    cache = load_cache()
    posted_jobs = cache.get("posted_jobs", {})

    if job_id not in posted_jobs:
        return False

    # Check if it was posted within the time window
    posted_time = datetime.fromisoformat(posted_jobs[job_id])
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)

    return posted_time > cutoff


def mark_posted(job_id):
    cache = load_cache()
    posted_jobs = cache.get("posted_jobs", {})

    # Store with ISO format timestamp
    posted_jobs[job_id] = datetime.now(timezone.utc).isoformat()

    cache["posted_jobs"] = posted_jobs
    save_cache(cache)
