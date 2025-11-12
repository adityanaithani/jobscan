import requests
import os
from dotenv import load_dotenv

load_dotenv()


def post_to_discord(job):
    url = os.getenv("DISCORD_WEBHOOK_URL")

    data = {"content": "", "username": "JobScan"}

    data["embeds"] = [
        {
            "description": job["posting_url"],
            "title": f"{job['title']}, {job['company_name']}",
        }
    ]

    result = requests.post(url, json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print(f"Code {result.status_code} successful delivery.")
