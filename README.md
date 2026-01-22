# JobScan

<!--[![Deploy JobScan](https://github.com/adityanaithani/jobscan/actions/workflows/main.yml/badge.svg)](https://github.com/adityanaithani/jobscan/actions/workflows/main.yml)-->

Job board scraper notifying of new positions through Discord.

## Features

- Fetches jobs from Greenhouse, Ashby, SmartRecruiters, Lever
- Customizable filters - title keywords, location, and date
- Posts to Discord via webhook

## Deployment

Self-hosted, using Docker / GitHub Actions for CI/CD.

## Todo

- [x] add Lever scraper
- [ ] add Dover scraper
- [ ] add Workday scraper
- [x] refine / grow list of companies
- [ ] change to async requests to accomodate for scale
- [ ] implement queue to avoid discord api rate limits
