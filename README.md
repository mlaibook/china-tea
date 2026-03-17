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
- `scripts/openclaw_refresh_analytics.sh` — local OpenClaw cron entrypoint; refreshes, commits, and pushes if data changed
- `data/ga/report.json` — cached analytics snapshot used by the page

### Local GA4 configuration for OpenClaw cron

This repo is now designed for local GA4 fetching through OpenClaw cron rather than GitHub Actions.

Set local environment/config like this:

- `GA4_PROPERTY_ID` — numeric GA4 property id
- `GA4_MEASUREMENT_ID` — optional, current site measurement id like `G-XXXXXXXXXX`
- `GOOGLE_APPLICATION_CREDENTIALS` — path to a local GA read-only credential file stored outside git

You can also place these in a local `.env.analytics` file in the repo root for the scripts to read.

Also make sure the service account email has at least read access to the target GA4 property.

If credentials are missing, the scripts still render a placeholder report so the static analytics page and local cron pipeline stay intact.
