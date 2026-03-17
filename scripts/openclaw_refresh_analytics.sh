#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

bash scripts/update_analytics_report.sh

git add analytics.html data/ga/report.json
if git diff --cached --quiet; then
  echo "No analytics changes to commit"
  exit 0
fi

git commit -m "chore: refresh analytics report"
git push
