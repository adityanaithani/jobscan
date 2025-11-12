from greenhouse import fetch_greenhouse
from filter import filter_jobs
from discord import post_to_discord

companies = ["open-ai", "stripe ", "github"]
keywords = ["software engineer", "engineer", "developer", "backend", "fullstack"]

if __name__ == "__main__":
    for company in companies:
        jobs = fetch_greenhouse(company)
        filtered = filter_jobs(jobs, keywords)
        for job in filtered:
            post_to_discord(job)