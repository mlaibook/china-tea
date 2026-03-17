#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
node scripts/fetch_ga4_report.js || true
node scripts/render_analytics_report.js
