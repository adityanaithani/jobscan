# JobScan

Personalized job board scraper updating new positions hourly via Discord (hours before LinkedIn or any of the big job boards!)

## Features

- Fetches jobs from Greenhouse, Ashby, SmartRecruiters, Lever, Dayforce
- Customizable filters - title keywords, location, and date

## Deployment

Self-hosted, using Docker / GitHub Actions for CI/CD.

## Todo

- [ ] change to async requests to accomodate for scale
- [x] implement queue to avoid discord api rate limits
