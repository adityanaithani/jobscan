import yaml
from pathlib import Path
from fetch import fetch_greenhouse, fetch_ashby, fetch_smartrecruiters
from filter import filter_jobs
from discord import post_to_discord
from cache import is_posted, mark_posted


def load_config():
    """Load configuration from config.yml"""
    config_path = Path(__file__).parent.parent / "config.yml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


fetchers = [fetch_greenhouse, fetch_ashby, fetch_smartrecruiters]


if __name__ == "__main__":
    # Load configuration
    config = load_config()
    companies = config["companies"]
    filters_config = config["filters"]

    print("🔍 Scanning for jobs posted in the last 24 hours...\n")
    total_posted = 0

    for company in companies:
        for fetcher in fetchers:
            jobs = fetcher(company)
            if jobs:
                break

        print(f"Fetched {len(jobs)} jobs from {company}")

        filtered = filter_jobs(
            jobs,
            keywords=filters_config["title_keywords"],
            exclude_keywords=filters_config["exclude_keywords"],
            allowed_countries=filters_config["allowed_countries"],
            hours=filters_config["hours"],
        )

        print(f"Filtered down to {len(filtered)} jobs for {company}")

        for job in filtered:
            job_id = f"{company}_{job['id']}"

            if is_posted(job_id):
                print(f"Already posted: {job['title']} (skipping)")
                continue

            print(f"Posting: {job['title']}")
            post_to_discord(job)
            mark_posted(job_id)
            total_posted += 1

    print(f"\n🟩 Posted {total_posted} new jobs to Discord")
