from fetch import fetch_greenhouse, fetch_ashby, fetch_smartrecruiters
from filter import filter_jobs
from discord import post_to_discord
from cache import is_posted, mark_posted

companies = [
    "stripe",
    "cohere",
    "confluent",
    "openai",
    "snowflake",
    "acorns",
    "homebase",
    "sentry",
    "decagon",
    "figma",
    "base",
    "ramp",
    "faire",
    "andurilindustries",
    "notion",
    "brex",
    "gusto",
    "rubrik",
    "doordashusa",
    "doordashcanada",
    "instacart",
    "robinhood",
    "chime",
    "coinbase",
    "affirm",
    "databricks",
    "asana",
    "calendly",
    "lever",
    "PaloAltoNetworks2",
    "sandisk",
    "wix2",
    "boschgroup",
    "westerndigital",
    "aecom2",
    "aristanetworks",
    "splunk",
    "cloudera",
    "qualtrics",
    "medallia",
]


# Filter configuration
TITLE_KEYWORDS = [
    "software engineer",
    "developer",
    "backend",
    "frontend",
    "fullstack",
    "full stack",
    "swe",
]

ALLOWED_COUNTRIES = [
    "USA",
    "US",
    "United States",
    "Canada",
    "CA",
]

fetchers = [fetch_greenhouse, fetch_ashby, fetch_smartrecruiters]


if __name__ == "__main__":
    total_posted = 0

    for company in companies:
        for fetcher in fetchers:
            jobs = fetcher(company)
            if jobs:
                break

        print(f"Fetched {len(jobs)} jobs from {company}")
        filtered = filter_jobs(
            jobs,
            keywords=TITLE_KEYWORDS,
            allowed_countries=ALLOWED_COUNTRIES,
            updated_today=True,
        )

        print(f"Filtered down to {len(filtered)} jobs for {company}")

        for job in filtered:
            job_id = f"{company}_{job['id']}"  # Create unique ID

            if is_posted(job_id):
                print(f"Already posted: {job['title']} (skipping)")
                continue

            print(f"Posting: {job['title']}")
            post_to_discord(job)
            mark_posted(job_id)
            total_posted += 1

    print(f"\n✅ Posted {total_posted} new jobs to Discord")
