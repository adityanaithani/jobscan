import requests
import os
from dotenv import load_dotenv
load_dotenv()

def post_to_discord(job):
    url = os.getenv("DISCORD_WEBHOOK_URL")
    message = f"**{job['title']}** at {job['company']['name']}\n{job['absolute_url']}"

    data = {
        "content": "",
        "username": "JobScan"
    }

    data["embeds"] = [
        {
            "description": job['absolute_url'],
            "title": f"{job['title']}, {job['company']['name']}"
        }
    ]

    result = requests.post(url, json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print(f"Code {result.status_code} successful delivery.")


if __name__ == "__main__":
    sample_job = {
        "title": "Software Engineer",
        "company": {"name": "OpenAI"},
        "absolute_url": "https://boards.greenhouse.io/openai/jobs/1234567"
    }
    post_to_discord(sample_job)