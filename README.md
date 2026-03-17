# China Tea

A bilingual GitHub Pages site introducing Chinese tea culture to international readers.

## Structure

- `index.html` landing page
- `en/` English pages
- `zh/` Chinese pages
- `assets/css/style.css` shared styling

## GitHub Pages

This repository is designed to work with GitHub Pages from the root branch.
Set Pages to deploy from `main` branch `/ (root)`.

## Analytics report

This repo now includes a static `analytics.html` page for internal reporting.

### Files

- `scripts/fetch_ga4_report.js` — fetches GA4 data via the Google Analytics Data API
- `scripts/render_analytics_report.js` — renders `analytics.html` from `data/ga/report.json`
- `scripts/update_analytics_report.sh` — fetch + render wrapper
- `data/ga/report.json` — cached analytics snapshot used by the page
- `.github/workflows/daily-analytics.yml` — daily refresh job

### Required secrets for live GA4 data

Add these GitHub Actions secrets in the repo settings:

- `GA4_PROPERTY_ID` — numeric GA4 property id
- `GA4_MEASUREMENT_ID` — optional, current site measurement id like `G-XXXXXXXXXX`
- `GA4_SERVICE_ACCOUNT_JSON` — full service account JSON with `analytics.readonly` access

Also make sure the service account email has at least read access to the target GA4 property.

If credentials are missing, the workflow still renders a placeholder report so the page and cron wiring stay intact.
