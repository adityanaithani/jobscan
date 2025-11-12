def filter_jobs(jobs, keywords=None, min_exp=None):
    keywords = [k.lower() for k in (keywords or [])]
    filtered = []
    for job in jobs:
        title = job.get('title', '').lower()
        if any(k in title for k in keywords):
               filtered.append(job)
    return filtered