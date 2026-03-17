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
  const file = process.env.GOOGLE_APPLICATION_CREDENTIALS || process.env.GA4_LOCAL_GA_CREDENTIALS;
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
  return Number(row?.metricValues?.[idx]?.value || 0);
}
function dimVal(row, idx) {
  return row?.dimensionValues?.[idx]?.value || '';
}
function normalizePath(input) {
  let p = String(input || '').trim();
  if (!p) return '/';
  p = p.replace(/^https?:\/\/[^/]+/i, '');
  if (!p.startsWith('/')) p = '/' + p;
  p = p.replace(/^\/china-tea(?=\/|$)/, '');
  p = p.replace(/\/+/g, '/');
  if (p !== '/' && p.endsWith('/')) p = p.slice(0, -1);
  return p || '/';
}
function detectLang(parts) {
  if (parts[0] === 'en' || parts[0] === 'zh') return parts[0];
  return '';
}
function classifySection(rawPath) {
  const p = normalizePath(rawPath);
  if (p === '/' || p === '/index.html') return { key: 'home', label: '首页' };
  const parts = p.split('/').filter(Boolean);
  const lang = detectLang(parts);
  const start = lang ? 1 : 0;
  const first = parts[start] || '';
  if (!first || first === 'index.html') {
    return { key: lang ? `${lang}-home` : 'home', label: lang === 'zh' ? '中文首页' : lang === 'en' ? '英文首页' : '首页' };
  }
  const map = {
    tea: '茶叶',
    teaware: '茶具',
    history: '茶文化历史',
    drinks: '现制茶饮',
    science: '科学/健康',
    about: '关于页',
    privacy: '隐私页',
    contact: '联系页',
    terms: '条款页',
    'analytics.html': '数据报表'
  };
  return { key: first, label: map[first] || first };
}
function sample(propertyId) {
  return {
    generatedAt: new Date().toISOString(),
    source: 'sample',
    note: '当前机器尚未完成 GA4 本地凭据配置，所以这里展示的是占位静态报表。',
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
      '尚未读取到 live GA4 数据。',
      '需要配置 GA4_PROPERTY_ID 与 GOOGLE_APPLICATION_CREDENTIALS。',
      '配置完成后，本地 OpenClaw cron 会自动拉取 GA 数据并更新静态 analytics 页面。'
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
  const top7raw = await runReport(propertyId, token, 7, ['pagePath'], ['screenPageViews','activeUsers'], 25);
  const top30raw = await runReport(propertyId, token, 30, ['pagePath'], ['screenPageViews','activeUsers'], 25);

  const top7 = (top7raw.rows || []).map(r => ({ path: normalizePath(dimVal(r,0)), views: metricVal(r,0), activeUsers: metricVal(r,1) }));
  const top30 = (top30raw.rows || []).map(r => ({ path: normalizePath(dimVal(r,0)), views: metricVal(r,0), activeUsers: metricVal(r,1) }));

  const sectionMap = new Map();
  for (const row of top30) {
    const sec = classifySection(row.path);
    const cur = sectionMap.get(sec.key) || { section: sec.key, label: sec.label, views: 0, activeUsers: 0 };
    cur.views += row.views;
    cur.activeUsers += row.activeUsers;
    sectionMap.set(sec.key, cur);
  }
  const topSections30d = [...sectionMap.values()]
    .sort((a,b) => b.views - a.views)
    .slice(0,10)
    .map(({section,label,views,activeUsers}) => ({ section, label, views, activeUsers }));

  const s7r = summary7.rows?.[0];
  const s30r = summary30.rows?.[0];
  const data = {
    generatedAt: new Date().toISOString(),
    source: 'ga4-data-api',
    note: '已通过本地 OpenClaw 脚本从 GA4 Data API 拉取数据，并生成静态页面。',
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
      top7[0] ? `近 7 天热门页面：${top7[0].path}（${top7[0].views} 次浏览）。` : '近 7 天暂无热门页面数据。',
      topSections30d[0] ? `近 30 天最强栏目：${topSections30d[0].label}。` : '近 30 天暂无栏目趋势数据。',
      '这些数据可直接用于首页热门模块、栏目推荐与选题优先级判断。'
    ]
  };
  fs.writeFileSync(outFile, JSON.stringify(data, null, 2), 'utf8');
  console.log(`Wrote live ${path.relative(repoRoot, outFile)}`);
})().catch(err => {
  const propertyId = process.env.GA4_PROPERTY_ID || parseDotEnv(envPath).GA4_PROPERTY_ID || '';
  const data = sample(propertyId);
  data.source = 'sample-fallback';
  data.note = `GA4 实时拉取失败，当前展示降级静态报表。${err.message}`;
  data.insights = [
    'GA4 拉取失败，已自动降级为静态占位数据。',
    '请检查 property id、service account 权限与本地凭据路径。',
    '本地 cron 仍会保留页面更新链路。'
  ];
  fs.writeFileSync(outFile, JSON.stringify(data, null, 2), 'utf8');
  console.error(err.stack || err.message);
  process.exitCode = 1;
});
