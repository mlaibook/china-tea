#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const https = require('https');

const repoRoot = path.resolve(__dirname, '..');
const dataDir = path.join(repoRoot, 'data', 'ga');
const outFile = path.join(dataDir, 'report.json');
const envPath = path.join(repoRoot, '.env.analytics');

function ensureDir(p) { fs.mkdirSync(p, { recursive: true }); }
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
function base64url(input) {
  return Buffer.from(JSON.stringify(input)).toString('base64').replace(/=/g,'').replace(/\+/g,'-').replace(/\//g,'_');
}
function readCredentials() {
  const env = parseDotEnv(envPath);
  for (const [k,v] of Object.entries(env)) if (!(k in process.env)) process.env[k] = v;
  const file = process.env.GOOGLE_APPLICATION_CREDENTIALS || process.env.GA4_CREDENTIALS_JSON;
  if (!file || !fs.existsSync(file)) return null;
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}
function httpRequest(url, { method='GET', headers={}, body } = {}) {
  return new Promise((resolve, reject) => {
    const req = https.request(url, { method, headers }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) resolve({ status: res.statusCode, body: data });
        else reject(new Error(`HTTP ${res.statusCode}: ${data.slice(0, 1000)}`));
      });
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}
async function getAccessToken(creds) {
  const now = Math.floor(Date.now()/1000);
  const header = { alg: 'RS256', typ: 'JWT' };
  const claim = {
    iss: creds.client_email,
    scope: 'https://www.googleapis.com/auth/analytics.readonly',
    aud: creds.token_uri || 'https://oauth2.googleapis.com/token',
    exp: now + 3600,
    iat: now
  };
  const unsigned = `${base64url(header)}.${base64url(claim)}`;
  const signer = require('crypto').createSign('RSA-SHA256');
  signer.update(unsigned);
  signer.end();
  const sig = signer.sign(creds.private_key, 'base64').replace(/=/g,'').replace(/\+/g,'-').replace(/\//g,'_');
  const assertion = `${unsigned}.${sig}`;
  const body = new URLSearchParams({
    grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
    assertion
  }).toString();
  const res = await httpRequest(creds.token_uri || 'https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body
  });
  return JSON.parse(res.body).access_token;
}
async function runReport(propertyId, token, days, dimensions, metrics, limit=10) {
  const body = {
    dateRanges: [{ startDate: `${days}daysAgo`, endDate: 'today' }],
    dimensions: dimensions.map(name => ({ name })),
    metrics: metrics.map(name => ({ name })),
    limit,
    orderBys: [{ metric: { metricName: metrics[0] }, desc: true }]
  };
  const url = `https://analyticsdata.googleapis.com/v1beta/properties/${propertyId}:runReport`;
  const res = await httpRequest(url, {
    method: 'POST',
    headers: { authorization: `Bearer ${token}`, 'content-type': 'application/json' },
    body: JSON.stringify(body)
  });
  return JSON.parse(res.body);
}
function metricVal(row, idx) {
  return Number(row.metricValues?.[idx]?.value || 0);
}
function dimVal(row, idx) {
  return row.dimensionValues?.[idx]?.value || '';
}
function sectionFromPath(p) {
  const parts = String(p || '').split('/').filter(Boolean);
  if (parts.length >= 2 && (parts[0] === 'en' || parts[0] === 'zh')) return parts[1];
  if (parts.length >= 1) return parts[0];
  return 'home';
}
function sample(propertyId) {
  return {
    generatedAt: new Date().toISOString(),
    source: 'sample',
    note: 'Live GA4 fetch skipped because credentials or property id are not configured.',
    propertyId: propertyId || '',
    measurementId: process.env.GA4_MEASUREMENT_ID || 'G-4VCYC4P23R',
    summary: {
      last7Days: { activeUsers: 0, sessions: 0, views: 0, avgSessionDurationSeconds: 0, engagementRate: 0 },
      last30Days: { activeUsers: 0, sessions: 0, views: 0, avgSessionDurationSeconds: 0, engagementRate: 0 }
    },
    topPages7d: [],
    topPages30d: [],
    topSections30d: [],
    insights: [
      'Set GA4_PROPERTY_ID to the numeric property id, not the G- measurement id.',
      'Set GOOGLE_APPLICATION_CREDENTIALS to a service-account JSON file with Analytics Data API access.',
      'Grant the service account read access to the target GA4 property before enabling cron automation.'
    ]
  };
}

(async () => {
  ensureDir(dataDir);
  const propertyId = process.env.GA4_PROPERTY_ID || parseDotEnv(envPath).GA4_PROPERTY_ID;
  const creds = readCredentials();
  if (!propertyId || !creds) {
    const data = sample(propertyId);
    fs.writeFileSync(outFile, JSON.stringify(data, null, 2), 'utf8');
    console.log(`Wrote sample ${path.relative(repoRoot, outFile)}`);
    return;
  }
  const token = await getAccessToken(creds);
  const summary7 = await runReport(propertyId, token, 7, [], ['activeUsers','sessions','screenPageViews','averageSessionDuration','engagementRate'], 1);
  const summary30 = await runReport(propertyId, token, 30, [], ['activeUsers','sessions','screenPageViews','averageSessionDuration','engagementRate'], 1);
  const top7raw = await runReport(propertyId, token, 7, ['pagePath'], ['screenPageViews','activeUsers'], 10);
  const top30raw = await runReport(propertyId, token, 30, ['pagePath'], ['screenPageViews','activeUsers'], 10);

  const top7 = (top7raw.rows || []).map(r => ({ path: dimVal(r,0), views: metricVal(r,0), activeUsers: metricVal(r,1) }));
  const top30 = (top30raw.rows || []).map(r => ({ path: dimVal(r,0), views: metricVal(r,0), activeUsers: metricVal(r,1) }));
  const sectionMap = new Map();
  for (const row of top30) {
    const key = sectionFromPath(row.path);
    const cur = sectionMap.get(key) || { section: key, views: 0, activeUsers: 0 };
    cur.views += row.views;
    cur.activeUsers += row.activeUsers;
    sectionMap.set(key, cur);
  }
  const topSections30d = [...sectionMap.values()].sort((a,b) => b.views - a.views).slice(0,10);

  const s7r = summary7.rows?.[0];
  const s30r = summary30.rows?.[0];
  const data = {
    generatedAt: new Date().toISOString(),
    source: 'ga4-data-api',
    note: 'Live GA4 report generated from the Analytics Data API.',
    propertyId,
    measurementId: process.env.GA4_MEASUREMENT_ID || 'G-4VCYC4P23R',
    summary: {
      last7Days: {
        activeUsers: metricVal(s7r,0), sessions: metricVal(s7r,1), views: metricVal(s7r,2),
        avgSessionDurationSeconds: metricVal(s7r,3), engagementRate: Number(s7r?.metricValues?.[4]?.value || 0)
      },
      last30Days: {
        activeUsers: metricVal(s30r,0), sessions: metricVal(s30r,1), views: metricVal(s30r,2),
        avgSessionDurationSeconds: metricVal(s30r,3), engagementRate: Number(s30r?.metricValues?.[4]?.value || 0)
      }
    },
    topPages7d: top7,
    topPages30d: top30,
    topSections30d,
    insights: [
      top7[0] ? `Top page over the last 7 days: ${top7[0].path} (${top7[0].views} views).` : 'No top-page data returned for the last 7 days.',
      topSections30d[0] ? `Strongest section over the last 30 days: ${topSections30d[0].section}.` : 'No section trend data returned for the last 30 days.',
      'Use this report to refresh homepage hot links, section highlights, and editorial priorities.'
    ]
  };
  fs.writeFileSync(outFile, JSON.stringify(data, null, 2), 'utf8');
  console.log(`Wrote live ${path.relative(repoRoot, outFile)}`);
})().catch(err => {
  const propertyId = process.env.GA4_PROPERTY_ID || parseDotEnv(envPath).GA4_PROPERTY_ID || '';
  const data = sample(propertyId);
  data.source = 'sample-fallback';
  data.note = `Live GA4 fetch failed; fallback report generated. ${err.message}`;
  fs.writeFileSync(outFile, JSON.stringify(data, null, 2), 'utf8');
  console.error(err.stack || err.message);
  process.exitCode = 1;
});
