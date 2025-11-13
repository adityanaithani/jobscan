from datetime import datetime, date, timedelta, timezone


def _to_date(val):
    if isinstance(val, datetime):
        if val.tzinfo is None:
            return val.replace(tzinfo=timezone.utc)
        return val
    if isinstance(val, date):
        dt = datetime.combine(val, datetime.min.time())
        return dt.replace(tzinfo=timezone.utc)
    if isinstance(val, str):
        s = val.split(".")[0].replace("Z", "")
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
            try:
                dt = datetime.strptime(s, fmt)
                # Make timezone-aware (assume UTC if not specified)
                return dt.replace(tzinfo=timezone.utc)
            except ValueError:
                continue
        try:
            dt = datetime.fromisoformat(s)
            if dt.tzinfo is None:
                return dt.replace(tzinfo=timezone.utc)
            return dt
        except Exception:
            return None
    return None


def _matches_title(job, includekw, excludekw):
    title = job.get("title", "").lower()

    if includekw:
        has_include = any(k.lower() in title for k in includekw)
        if not has_include:
            return False

    if excludekw:
        has_exclude = any(k.lower() in title for k in excludekw)
        if has_exclude:
            return False

    return True


def _matches_location(job, allowed_countries=None):
    if not allowed_countries:
        return True

    country = job.get("location_country", "").upper()
    if country:
        return any(c.upper() in country for c in allowed_countries)

    location = job.get("location", "").upper()
    if location:
        return any(c.upper() in location for c in allowed_countries)

    return True


def _is_recent(job, hours=24):
    job_date = _to_date(job.get("updated"))
    if not job_date:
        return False

    # Use timezone-aware datetime for comparison
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    return job_date >= cutoff


def filter_jobs(
    jobs,
    keywords=None,
    exclude_keywords=None,
    allowed_countries=None,
    hours=24,
):

    filtered = []

    for job in jobs:
        if not _matches_title(job, keywords, exclude_keywords):
            continue

        if not _matches_location(job, allowed_countries):
            continue

        if hours and not _is_recent(job, hours=hours):
            continue

        filtered.append(job)

    return filtered
