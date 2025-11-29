# JobScan

<!--[![Deploy JobScan](https://github.com/adityanaithani/jobscan/actions/workflows/main.yml/badge.svg)](https://github.com/adityanaithani/jobscan/actions/workflows/main.yml)-->

Job board scraper notifying of new positions through Discord.

## Features

- Fetches jobs from Greenhouse, Ashby, SmartRecruiters
- Customizable filters - title keywords, location, and date
- Posts to Discord via webhook

## Deployment

Self-hosted, using Docker / GitHub Actions for CI/CD.

## Todo

- [ ] add additional job board scrapers (Dover, Workday, Lever)
- [ ] refine / grow list of companies
- [ ] change to async requests to accomodate for scale
- [ ] implement queue to avoid discord api rate limits
