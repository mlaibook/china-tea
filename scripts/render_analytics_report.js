#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const repoRoot = path.resolve(__dirname, '..');
const dataDir = path.join(repoRoot, 'data', 'ga');
const analyticsPath = path.join(repoRoot, 'analytics.html');
const envPath = path.join(repoRoot, '.env.analytics');

function ensureDir(p) { fs.mkdirSync(p, { recursive: true }); }
function readJsonSafe(file) {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); }
  catch { return null; }
}
function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
function parseDotEnv(file) {
  if (!fs.existsSync(file)) return {};
  const out = {};
  for (const line of fs.readFileSync(file, 'utf8').split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const idx = trimmed.indexOf('=');
    if (idx === -1) continue;
    const key = trimmed.slice(0, idx).trim();
    let val = trimmed.slice(idx + 1).trim();
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) val = val.slice(1, -1);
    out[key] = val;
  }
  return out;
}

function buildSampleData() {
  const now = new Date().toISOString();
  return {
    generatedAt: now,
    source: 'sample',
    note: 'GA credentials not configured yet. This placeholder report keeps the page wired and ready.',
    propertyId: process.env.GA4_PROPERTY_ID || '',
    measurementId: process.env.GA4_MEASUREMENT_ID || 'G-4VCYC4P23R',
    summary: {
      last7Days: { activeUsers: 0, sessions: 0, views: 0, avgSessionDurationSeconds: 0, engagementRate: 0 },
      last30Days: { activeUsers: 0, sessions: 0, views: 0, avgSessionDurationSeconds: 0, engagementRate: 0 }
    },
    topPages7d: [],
    topPages30d: [],
    topSections30d: [],
    insights: [
      'GA4 data API not configured yet; page is ready for live report ingestion.',
      'Add GA4_PROPERTY_ID and GOOGLE_APPLICATION_CREDENTIALS before enabling live pulls.',
      'Once credentials are present, this report can rank hot article URLs and section demand automatically.'
    ]
  };
}

function formatInt(v) {
  const num = Number(v || 0);
  return Number.isFinite(num) ? num.toLocaleString('en-US') : '0';
}
function formatPct(v) {
  const num = Number(v || 0);
  return `${(num * 100).toFixed(1)}%`;
}
function formatSeconds(v) {
  const n = Math.round(Number(v || 0));
  const m = Math.floor(n / 60);
  const s = n % 60;
  return `${m}m ${s}s`;
}
function card(title, value, sub='') {
  return `<div class="analytics-card"><div class="analytics-kicker">${escapeHtml(title)}</div><div class="analytics-value">${escapeHtml(value)}</div>${sub ? `<div class="analytics-sub">${escapeHtml(sub)}</div>` : ''}</div>`;
}
function rows(items, columns) {
  if (!items.length) return `<tr><td colspan="${columns}">No data yet.</td></tr>`;
  return items.map(item => `<tr>${item.map(cell => `<td>${cell}</td>`).join('')}</tr>`).join('');
}

function render(data) {
  const s7 = data.summary?.last7Days || {};
  const s30 = data.summary?.last30Days || {};
  const top7 = Array.isArray(data.topPages7d) ? data.topPages7d : [];
  const top30 = Array.isArray(data.topPages30d) ? data.topPages30d : [];
  const sections = Array.isArray(data.topSections30d) ? data.topSections30d : [];
  const insights = Array.isArray(data.insights) ? data.insights : [];
  const generatedAt = data.generatedAt || new Date().toISOString();
  const source = data.source || 'unknown';
  const note = data.note || '';
  const measurementId = data.measurementId || 'G-4VCYC4P23R';
  const propertyId = data.propertyId || '';

  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>China Tea Analytics Report</title>
  <meta name="description" content="Daily analytics report for the China Tea Library content site." />
  <meta name="robots" content="noindex,follow" />
  <link rel="stylesheet" href="assets/css/style.css" />
</head>
<body>
  <header class="site-header wrap">
    <div class="nav">
      <a class="brand" href="en/index.html">China Tea Library</a>
      <nav>
        <a href="en/index.html">English</a>
        <a href="zh/index.html">中文</a>
        <a href="analytics.html">Analytics</a>
      </nav>
    </div>
  </header>
  <main class="page analytics-page">
    <article>
      <p class="eyebrow">Analytics</p>
      <h1>Daily GA4 content report</h1>
      <p class="lede">This page stores the site’s internal analytics snapshot for editorial decisions, homepage tuning, and future automation.</p>
      <p class="meta">Generated: <time datetime="${escapeHtml(generatedAt)}">${escapeHtml(generatedAt)}</time> · Source: ${escapeHtml(source)} · Measurement ID: ${escapeHtml(measurementId)}${propertyId ? ` · Property ID: ${escapeHtml(propertyId)}` : ''}</p>
      ${note ? `<p class="note">${escapeHtml(note)}</p>` : ''}

      <section class="analytics-grid">
        ${card('7d active users', formatInt(s7.activeUsers), 'Recent audience size')}
        ${card('7d sessions', formatInt(s7.sessions), 'Visits in last 7 days')}
        ${card('7d views', formatInt(s7.views), 'Page views in last 7 days')}
        ${card('7d avg session', formatSeconds(s7.avgSessionDurationSeconds), 'Average engaged visit length')}
        ${card('30d active users', formatInt(s30.activeUsers), 'Broader monthly audience')}
        ${card('30d engagement', formatPct(s30.engagementRate), 'Engagement rate')}
      </section>

      <section class="feature-card analytics-section">
        <h2>Top pages · last 7 days</h2>
        <table class="analytics-table">
          <thead><tr><th>Path</th><th>Views</th><th>Active users</th></tr></thead>
          <tbody>${rows(top7.map(p => [escapeHtml(p.path || ''), formatInt(p.views), formatInt(p.activeUsers)]), 3)}</tbody>
        </table>
      </section>

      <section class="feature-card analytics-section">
        <h2>Top pages · last 30 days</h2>
        <table class="analytics-table">
          <thead><tr><th>Path</th><th>Views</th><th>Active users</th></tr></thead>
          <tbody>${rows(top30.map(p => [escapeHtml(p.path || ''), formatInt(p.views), formatInt(p.activeUsers)]), 3)}</tbody>
        </table>
      </section>

      <section class="feature-card analytics-section">
        <h2>Top sections · last 30 days</h2>
        <table class="analytics-table">
          <thead><tr><th>Section</th><th>Views</th><th>Active users</th></tr></thead>
          <tbody>${rows(sections.map(p => [escapeHtml(p.section || ''), formatInt(p.views), formatInt(p.activeUsers)]), 3)}</tbody>
        </table>
      </section>

      <section class="feature-card analytics-section">
        <h2>Editorial notes</h2>
        <ul class="analytics-notes">
          ${(insights.length ? insights : ['No editorial notes yet.']).map(item => `<li>${escapeHtml(item)}</li>`).join('')}
        </ul>
      </section>
    </article>
  </main>
  <footer class="site-footer wrap">
    <a href="en/about.html">About</a>
    <a href="en/privacy.html">Privacy</a>
    <a href="en/contact.html">Contact</a>
    <a href="en/terms.html">Terms</a>
    <a href="analytics.html">Analytics</a>
  </footer>
</body>
</html>`;
}

ensureDir(dataDir);
const env = parseDotEnv(envPath);
for (const [k,v] of Object.entries(env)) if (!(k in process.env)) process.env[k] = v;
const dataFile = path.join(dataDir, 'report.json');
const data = readJsonSafe(dataFile) || buildSampleData();
fs.writeFileSync(analyticsPath, render(data), 'utf8');
console.log(`Wrote ${path.relative(repoRoot, analyticsPath)}`);
