import requests


# normalizers
def _normalize_greenhouse(job):
    return {
        "title": job.get("title", ""),
        "company_name": job.get("company_name", ""),
        "location": job.get("location", {}).get("name", ""),
        "posting_url": job.get("absolute_url", ""),
        "updated": job.get("updated_at", ""),
        "id": job.get("id", ""),
    }


def _normalize_ashby(job):
    address = job.get("address") or {}
    postal_address = address.get("postalAddress") or {}

    return {
        "title": job.get("title", ""),
        "company_name": job.get("company_name", ""),
        "location": job.get("location", ""),
        "location_country": postal_address.get("addressCountry", ""),
        "posting_url": job.get("applyUrl", ""),
        "updated": job.get("publishedAt", ""),
        "id": job.get("id", ""),
    }


def _normalize_smartrecruiters(job):
    return {
        "title": job.get("name", ""),
        "company_name": job.get("company", {}).get("name", ""),
        "location": job.get("location", {}).get("city", ""),
        "location_country": job.get("location", {}).get("country", ""),
        "posting_url": job.get("applyUrl", "") or job.get("ref", ""),
        "updated": job.get("releasedDate", ""),
        "id": job.get("id", ""),
    }


def _normalize_lever(job):
    categories = job.get("categories", {})
    location = categories.get("location", "")

    return {
        "title": job.get("text", ""),
        "company_name": categories.get("team", ""),
        "location": location,
        "location_country": job.get("country", ""),
        "posting_url": job.get("hostedUrl", "") or job.get("applyUrl", ""),
        "updated": job.get("createdAt", ""),
        "id": job.get("id", ""),
    }


# generic fetch
def _fetch_(company: str, url: str, jobs_key: str, normalizer, platform_name: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        jobs = response.json().get(jobs_key, [])
        return [normalizer(job) for job in jobs]
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"404: '{company}' not found on {platform_name}.")
        else:
            print(f"HTTP error occurred fetching {company} from {platform_name}: {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error occurred fetching {company} from {platform_name}: {e}")
        return []
    except (ValueError, KeyError) as e:
        print(f"Error parsing JSON for {company} from {platform_name}: {e}")
        return []


# specialized fetch
def fetch_greenhouse(company: str):
    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
    return _fetch_(company, url, "jobs", _normalize_greenhouse, "Greenhouse")


def fetch_ashby(company: str):
    url = f"https://api.ashbyhq.com/posting-api/job-board/{company}?includeCompensation=true"
    return _fetch_(company, url, "jobs", _normalize_ashby, "Ashby")


def fetch_smartrecruiters(company: str):
    url = f"https://api.smartrecruiters.com/v1/companies/{company}/postings"
    return _fetch_(
        company, url, "content", _normalize_smartrecruiters, "SmartRecruiters"
    )


def fetch_lever(company: str):
    url = f"https://api.lever.co/v0/postings/{company}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        jobs = response.json()

        if isinstance(jobs, list):
            return [_normalize_lever(job) for job in jobs]
        else:
            print(f"Unexpected Lever response format for {company}")
            return []

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"404: '{company}' not found on Lever.")
        else:
            print(f"HTTP error occurred fetching {company} from Lever: {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error occurred fetching {company} from Lever: {e}")
        return []
    except (ValueError, KeyError) as e:
        print(f"Error parsing JSON for {company} from Lever: {e}")
        return []
