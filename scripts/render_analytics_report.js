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
    note: '当前机器尚未完成 GA4 本地凭据配置，所以这里展示的是占位静态报表。',
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
      '尚未读取到 live GA4 数据。',
      '需要配置 GA4_PROPERTY_ID 与 GOOGLE_APPLICATION_CREDENTIALS。',
      '配置完成后，本地 OpenClaw cron 会自动拉取 GA 数据并更新静态 analytics 页面。'
    ]
  };
}

function formatInt(v) {
  const num = Number(v || 0);
  return Number.isFinite(num) ? num.toLocaleString('zh-CN') : '0';
}
function formatPct(v) {
  const num = Number(v || 0);
  return `${(num * 100).toFixed(1)}%`;
}
function formatSeconds(v) {
  const n = Math.round(Number(v || 0));
  const m = Math.floor(n / 60);
  const s = n % 60;
  return `${m}分 ${s}秒`;
}
function card(title, value, sub='') {
  return `<div class="analytics-card"><div class="analytics-kicker">${escapeHtml(title)}</div><div class="analytics-value">${escapeHtml(value)}</div>${sub ? `<div class="analytics-sub">${escapeHtml(sub)}</div>` : ''}</div>`;
}
function rows(items, columns) {
  if (!items.length) return `<tr><td colspan="${columns}">暂无数据</td></tr>`;
  return items.map(item => `<tr>${item.map(cell => `<td>${cell}</td>`).join('')}</tr>`).join('');
}
function zhSectionLabel(section) {
  const map = {
    en: '英文首页/目录',
    zh: '中文首页/目录',
    tea: '茶叶',
    teaware: '茶具',
    history: '茶文化历史',
    drinks: '现制茶饮',
    science: '科学/健康'
  };
  return map[section] || section || '未分类';
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

  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>网站数据报表 | 茶库</title>
  <meta name="description" content="茶库站点的静态 Analytics 数据报表页面。" />
  <meta name="robots" content="noindex,follow" />
  <link rel="stylesheet" href="assets/css/style.css" />
</head>
<body>
  <header class="site-header wrap">
    <div class="nav">
      <a class="brand" href="zh/index.html">茶库数据页</a>
      <nav>
        <a href="zh/index.html">网站首页</a>
        <a href="analytics.html">数据报表</a>
      </nav>
    </div>
  </header>
  <main class="page analytics-page">
    <article>
      <p class="eyebrow">数据报表</p>
      <h1>网站静态 Analytics 页面</h1>
      <p class="lede">这个页面只用于呈现已经拉取并生成好的静态数据，不在前端实时请求 Google Analytics。</p>
      <p class="meta">生成时间：<time datetime="${escapeHtml(generatedAt)}">${escapeHtml(generatedAt)}</time> · 数据来源：${escapeHtml(source)}</p>
      ${note ? `<p class="note">${escapeHtml(note)}</p>` : ''}

      <section class="analytics-grid">
        ${card('近 7 天活跃用户', formatInt(s7.activeUsers), '最近 7 天访问用户数')}
        ${card('近 7 天会话数', formatInt(s7.sessions), '最近 7 天访问会话')}
        ${card('近 7 天浏览量', formatInt(s7.views), '最近 7 天页面浏览')}
        ${card('近 7 天平均会话时长', formatSeconds(s7.avgSessionDurationSeconds), '平均访问停留时间')}
        ${card('近 30 天活跃用户', formatInt(s30.activeUsers), '最近 30 天访问用户数')}
        ${card('近 30 天互动率', formatPct(s30.engagementRate), '最近 30 天 engagement rate')}
      </section>

      <section class="feature-card analytics-section">
        <h2>近 7 天热门页面</h2>
        <table class="analytics-table">
          <thead><tr><th>页面路径</th><th>浏览量</th><th>活跃用户</th></tr></thead>
          <tbody>${rows(top7.map(p => [escapeHtml(p.path || ''), formatInt(p.views), formatInt(p.activeUsers)]), 3)}</tbody>
        </table>
      </section>

      <section class="feature-card analytics-section">
        <h2>近 30 天热门页面</h2>
        <table class="analytics-table">
          <thead><tr><th>页面路径</th><th>浏览量</th><th>活跃用户</th></tr></thead>
          <tbody>${rows(top30.map(p => [escapeHtml(p.path || ''), formatInt(p.views), formatInt(p.activeUsers)]), 3)}</tbody>
        </table>
      </section>

      <section class="feature-card analytics-section">
        <h2>近 30 天热门栏目</h2>
        <table class="analytics-table">
          <thead><tr><th>栏目</th><th>浏览量</th><th>活跃用户</th></tr></thead>
          <tbody>${rows(sections.map(p => [escapeHtml(zhSectionLabel(p.section)), formatInt(p.views), formatInt(p.activeUsers)]), 3)}</tbody>
        </table>
      </section>

      <section class="feature-card analytics-section">
        <h2>运营备注</h2>
        <ul class="analytics-notes">
          ${(insights.length ? insights : ['暂无备注。']).map(item => `<li>${escapeHtml(item)}</li>`).join('')}
        </ul>
      </section>
    </article>
  </main>
  <footer class="site-footer wrap">
    <a href="zh/about.html">关于</a>
    <a href="zh/privacy.html">隐私</a>
    <a href="zh/contact.html">联系</a>
    <a href="zh/terms.html">条款</a>
    <a href="analytics.html">数据报表</a>
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
