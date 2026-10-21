# WxCareers

Every meteorology job in one place (TV, federal, private, aviation, military, academic) with posted salaries only. Live at https://wxcareers.com

- `site/` static site (jobs list with sector/state filters, salaries, post-a-job, newsletter placeholder). `site/CNAME` = wxcareers.com
- `data/jobs.json` current listings; `data/manual.json` hand-added employer postings
- `scripts/update.py` refreshes listings from public sources (iHireBroadcasting, USAJOBS, employer Greenhouse boards, manual list), dedupes, drops dead links, applies curation (EXCLUDE_TITLES, SECTOR_OVERRIDES). Run: `python3 scripts/update.py`
- `.github/workflows/update-and-deploy.yml` runs daily ~6am ET and on manual trigger, commits changed data, deploys to GitHub Pages.

Local preview: `python3 -m http.server 8080 -d site`
