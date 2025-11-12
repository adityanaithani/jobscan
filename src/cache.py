import json
import os
from datetime import date
from pathlib import Path


CACHE_FILE = Path(__file__).parent.parent / "data" / "posted_jobs.json"


def _ensure_cache_dir():
    """Create cache directory if it doesn't exist"""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_cache():
    """Load cache of posted job IDs, reset if it's a new day"""
    _ensure_cache_dir()

    if not CACHE_FILE.exists():
        return {"date": str(date.today()), "posted_ids": []}

    try:
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)

        # Reset cache if it's a new day
        if cache.get("date") != str(date.today()):
            return {"date": str(date.today()), "posted_ids": []}

        return cache
    except (json.JSONDecodeError, KeyError):
        return {"date": str(date.today()), "posted_ids": []}


def save_cache(cache):
    """Save cache to disk"""
    _ensure_cache_dir()
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def is_posted(job_id):
    """Check if a job has already been posted today"""
    cache = load_cache()
    return job_id in cache["posted_ids"]


def mark_posted(job_id):
    """Mark a job as posted"""
    cache = load_cache()
    if job_id not in cache["posted_ids"]:
        cache["posted_ids"].append(job_id)
        save_cache(cache)
