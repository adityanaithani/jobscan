from datetime import datetime, date


def _to_date(val):
    """Convert various date formats to date object"""
    if isinstance(val, date) and not isinstance(val, datetime):
        return val
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, str):
        # try ISO / common datetime formats
        s = val.split(".")[0]
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(s, fmt).date()
            except ValueError:
                continue
        try:
            return datetime.fromisoformat(val).date()
        except Exception:
            return None
    return None


def _matches_title(job, keywords):
    """Check if job title contains any of the keywords"""
    if not keywords:
        return True
    title = job.get("title", "").lower()
    return any(k.lower() in title for k in keywords)


def _matches_location(job, allowed_countries=None):
    """Check if job location is in allowed countries"""
    if not allowed_countries:
        return True

    # Check location_country field (from Ashby, SmartRecruiters)
    country = job.get("location_country", "").upper()
    if country:
        return any(c.upper() in country for c in allowed_countries)

    # Fallback: check location string (from Greenhouse)
    location = job.get("location", "").upper()
    if location:
        return any(c.upper() in location for c in allowed_countries)

    # If no location data, include it (don't filter out)
    return True


def _matches_date(job, target_date=None):
    """Check if job was updated on target date"""
    if target_date is None:
        target_date = date.today()

    job_date = _to_date(job.get("updated"))
    return job_date == target_date if job_date else False


def filter_jobs(jobs, keywords=None, allowed_countries=None, updated_today=True):
    """
    Filter jobs based on title keywords, location, and update date.

    Args:
        jobs: List of normalized job dicts
        keywords: List of keywords to match in job title (e.g., ["software engineer", "developer"])
        allowed_countries: List of country codes/names (e.g., ["USA", "US", "Canada", "CA"])
        updated_today: If True, only return jobs updated today

    Returns:
        List of filtered jobs
    """
    filtered = []

    for job in jobs:
        if not _matches_title(job, keywords):
            continue

        if not _matches_location(job, allowed_countries):
            continue

        if updated_today and not _matches_date(job):
            continue

        filtered.append(job)

    return filtered
