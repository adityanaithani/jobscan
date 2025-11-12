import requests

def fetch_greenhouse(company: str):
    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
    response = requests.get(url)
    # response.raise_for_status()
    return response.json().get("jobs", [])

# test runner
if __name__ == "__main__":
    company = "stripe"
    jobs = fetch_greenhouse(company)
    for job in jobs:
        if job['title'].lower().startswith("software engineer"):
            print(f"Title: {job['title']}, Location: {job['location']['name']}, ID: {job['id']}")