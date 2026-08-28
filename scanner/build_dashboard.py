#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 skills_catalog.json 内嵌进 dashboard 模板，生成自包含 dashboard.html"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "skills_catalog.json"
OUT = ROOT / "dashboard.html"

data = json.loads(DATA.read_text(encoding="utf-8"))
# 精简字段，减小体积
for r in data["records"]:
    r.pop("path", None)
    r.pop("icon", None)
    r.pop("installed_at", None)
    r.pop("size_kb", None)
payload = json.dumps(data, ensure_ascii=False)

HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WorkBuddy Skill 全景调研</title>
<style>
:root {
  --pa-orange: #F26B21;
  --pa-orange-deep: #D95A10;
  --pa-orange-light: #FDEEE3;
  --pa-blue: #2D4869;
  --pa-blue-light: #EAF0F7;
  --bg: #F7F5F2;
  --card: #FFFFFF;
  --ink: #2A2622;
  --ink-2: #6B625A;
  --ink-3: #9A9088;
  --line: #E8E2DA;
  --star: #E8A23D;
  --ok: #3E8E5A;
  --shadow: 0 1px 3px rgba(42,38,34,.06);
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
  background: var(--bg); color: var(--ink); font-size: 14px; line-height: 1.6;
}
.header {
  background: linear-gradient(135deg, #F26B21 0%, #D95A10 60%, #B84A08 100%);
  color:#fff; padding: 22px 32px 18px;
  display:flex; align-items:flex-end; justify-content:space-between; flex-wrap:wrap; gap:12px;
}
.header h1 { font-size:22px; font-weight:600; letter-spacing:1px; }
.header .sub { font-size:12.5px; opacity:.92; margin-top:4px; }
.header .meta { font-size:12px; opacity:.85; text-align:right; }
.wrap { max-width:1320px; margin:0 auto; padding:20px 28px 60px; }
body { overflow-x:hidden; }

/* KPI */
.kpis { display:grid; grid-template-columns:repeat(auto-fit, minmax(150px,1fr)); gap:12px; margin-bottom:18px; }
.kpi { background:var(--card); border-radius:10px; padding:14px 16px; box-shadow:var(--shadow); border-top:3px solid var(--pa-orange); }
.kpi b { font-size:26px; font-weight:700; color:var(--pa-orange-deep); display:block; line-height:1.2; }
.kpi span { font-size:12px; color:var(--ink-2); }
.kpi.blue { border-top-color:var(--pa-blue); } .kpi.blue b { color:var(--pa-blue); }

/* 布局 */
.cols { display:grid; grid-template-columns: 250px 1fr; gap:16px; align-items:start; }
@media (max-width: 900px){ .cols { grid-template-columns:1fr; } }

/* 图表卡 */
.card { background:var(--card); border-radius:12px; padding:16px 18px; box-shadow:var(--shadow); margin-bottom:16px; }
.card h3 { font-size:14px; font-weight:600; color:var(--pa-blue); margin-bottom:10px; display:flex; justify-content:space-between; align-items:center; }
.card h3 .hint { font-size:11px; color:var(--ink-3); font-weight:400; }

/* 分布条 */
.bar-row { display:flex; align-items:center; gap:8px; margin-bottom:7px; font-size:12.5px; }
.bar-row .lbl { width:72px; text-align:right; color:var(--ink-2); flex-shrink:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.bar-row .track { flex:1; height:16px; background:#F1ECE5; border-radius:4px; overflow:hidden; }
.bar-row .fill { height:100%; background:linear-gradient(90deg,var(--pa-orange),#F58B4B); border-radius:4px; min-width:2px; }
.bar-row .val { width:36px; color:var(--ink-2); font-variant-numeric:tabular-nums; flex-shrink:0; }

/* 筛选器 */
.filters { position:sticky; top:12px; max-height:calc(100vh - 24px); overflow-y:auto; }
.fgroup { margin-bottom:14px; }
.fgroup h4 { font-size:12px; color:var(--ink-2); margin-bottom:6px; font-weight:600; }
.chips { display:flex; flex-wrap:wrap; gap:6px; }
.chip {
  font-size:12px; padding:3px 10px; border-radius:999px; border:1px solid var(--line);
  background:#fff; color:var(--ink-2); cursor:pointer; transition:all .15s; user-select:none;
}
.chip:hover { border-color:var(--pa-orange); color:var(--pa-orange-deep); }
.chip.on { background:var(--pa-orange); border-color:var(--pa-orange); color:#fff; }
.searchbox input {
  width:100%; padding:8px 12px; border:1px solid var(--line); border-radius:8px; font-size:13px; outline:none;
}
.searchbox input:focus { border-color:var(--pa-orange); box-shadow:0 0 0 3px rgba(242,107,33,.12); }
.score-filter { display:flex; gap:4px; }
.score-filter .chip { padding:3px 8px; }
.selectall { font-size:11px; color:var(--pa-orange-deep); cursor:pointer; margin-top:4px; display:inline-block; }

/* 工具栏 */
.toolbar { display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:12px; }
.toolbar .count { font-size:13px; color:var(--ink-2); }
.toolbar .count b { color:var(--pa-orange-deep); font-size:16px; }
.btn {
  font-size:12.5px; padding:6px 14px; border-radius:8px; border:1px solid var(--line);
  background:#fff; color:var(--ink-2); cursor:pointer; transition:all .15s;
}
.btn:hover { border-color:var(--pa-orange); color:var(--pa-orange-deep); }
.btn.primary { background:var(--pa-orange); color:#fff; border-color:var(--pa-orange); }
.btn.primary:hover { background:var(--pa-orange-deep); }

/* 技能卡墙 */
.grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(min(300px,100%),1fr)); gap:12px; }
.scard {
  background:var(--card); border-radius:10px; padding:14px 16px; box-shadow:var(--shadow);
  border:1px solid transparent; cursor:pointer; transition:all .15s; position:relative;
  display:flex; flex-direction:column; gap:6px;
}
.scard:hover { border-color:var(--pa-orange); transform:translateY(-2px); box-shadow:0 4px 14px rgba(242,107,33,.13); }
.scard .top { display:flex; justify-content:space-between; align-items:flex-start; gap:8px; }
.scard .name { font-size:14px; font-weight:600; color:var(--ink); line-height:1.35; }
.scard .stars { color:var(--star); font-size:12px; letter-spacing:1px; white-space:nowrap; flex-shrink:0; }
.scard .envstars { display:flex; flex-direction:column; gap:2px; align-items:flex-end; flex-shrink:0; font-style:normal; }
.scard .eb { font-size:10.5px; letter-spacing:0; white-space:nowrap; font-style:normal; }
.scard .eb.h { color:#B84A08; }
.scard .eb.k { color:#2D4869; letter-spacing:0; }
.scard .desc { font-size:12px; color:var(--ink-2); display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
.scard .tags { display:flex; flex-wrap:wrap; gap:5px; margin-top:2px; }
.tag { font-size:10.5px; padding:1px 8px; border-radius:999px; }
.tag.cat { background:var(--pa-blue-light); color:var(--pa-blue); }
.tag.src { background:#F1ECE5; color:var(--ink-2); }
.tag.role { background:var(--pa-orange-light); color:var(--pa-orange-deep); }
.scard .mark {
  position:absolute; top:10px; right:12px; font-size:11px; display:none;
}
.scard.starred .mark { display:block; color:var(--pa-orange); }

/* 抽屉 */
.overlay { display:none; position:fixed; inset:0; background:rgba(42,38,34,.4); z-index:50; }
.drawer {
  display:none; position:fixed; top:0; right:-560px; width:540px; max-width:92vw; height:100vh;
  background:#fff; z-index:60; box-shadow:-6px 0 24px rgba(0,0,0,.12);
  transition:right .25s ease; overflow-y:auto; padding:24px 26px;
}
.drawer.open { right:0; display:block; }
.overlay.open { display:block; }
.drawer h2 { font-size:18px; color:var(--pa-blue); margin-bottom:4px; padding-right:60px; }
.drawer .dpath { font-size:11.5px; color:var(--ink-3); font-family:Menlo,monospace; word-break:break-all; margin-bottom:12px; }
.drawer .sec { margin-bottom:14px; }
.drawer .sec h5 { font-size:12px; color:var(--pa-orange-deep); margin-bottom:4px; font-weight:600; }
.drawer .sec p { font-size:13px; color:var(--ink-2); white-space:pre-wrap; }
.drawer .close {
  position:absolute; top:16px; right:18px; font-size:22px; color:var(--ink-3); cursor:pointer; line-height:1;
}
.drawer .close:hover { color:var(--pa-orange); }
.markbtns { display:flex; gap:8px; margin:14px 0; flex-wrap:wrap; }
.mbtn {
  flex:1; min-width:110px; padding:10px 8px; border-radius:10px; border:1.5px solid var(--line);
  background:#fff; cursor:pointer; text-align:center; font-size:13px; color:var(--ink-2); transition:all .15s;
}
.mbtn:hover { border-color:var(--pa-orange); }
.mbtn.on-1 { background:var(--pa-orange); border-color:var(--pa-orange); color:#fff; }
.mbtn.on-2 { background:var(--pa-blue); border-color:var(--pa-blue); color:#fff; }
.mbtn.on-3 { background:var(--ok); border-color:var(--ok); color:#fff; }
.legend { font-size:11px; color:var(--ink-3); margin-top:8px; }

/* toast */
.toast {
  position:fixed; bottom:24px; left:50%; transform:translateX(-50%); background:var(--ink);
  color:#fff; padding:10px 22px; border-radius:8px; font-size:13px; opacity:0;
  transition:opacity .3s; pointer-events:none; z-index:100;
}
.toast.show { opacity:.92; }
.empty { text-align:center; color:var(--ink-3); padding:60px 0; font-size:13px; }
.footer { text-align:center; color:var(--ink-3); font-size:11.5px; padding:18px 0 6px; }

/* ---------- 移动端适配 ---------- */
.mtoggle {
  display:none; width:100%; padding:10px; border-radius:10px; border:1.5px dashed var(--line);
  background:#fff; color:var(--pa-orange-deep); font-size:13px; text-align:center; cursor:pointer;
  margin-bottom:12px; user-select:none;
}
.mtoggle::before { content:"▼ 打开筛选器"; }
.mtoggle.open::before { content:"▲ 收起筛选器"; }
@media (max-width: 760px) {
  .header { padding:16px 18px 14px; }
  .header h1 { font-size:18px; }
  .header .meta { display:none; }
  .wrap { padding:14px 12px 40px; width:100%; max-width:100vw; }
  .cols { grid-template-columns:minmax(0,1fr); }
  .filters, .filters .card, .grid, .toolbar, .card, .mtoggle { max-width:100%; min-width:0; }
  .bar-row .track { min-width:0; }
  .filters { position:static; }
  .filters .card { display:none; }
  .filters.show .card { display:block; }
  .mtoggle { display:block; }
  .grid { grid-template-columns:minmax(0,1fr); gap:10px; }
  .scard { min-width:0; max-width:100%; }
  .kpis { grid-template-columns:repeat(2,1fr); gap:8px; }
  .kpi { padding:10px 12px; }
  .kpi b { font-size:20px; }
  .toolbar { gap:6px; }
  .toolbar .count { width:100%; }
  .btn { padding:8px 12px; font-size:13px; }
  .drawer { width:100vw; right:-100vw; padding:18px 16px 40px; }
  .drawer h2 { font-size:17px; padding-right:44px; }
  .mbtn { padding:12px 8px; font-size:13.5px; }
  .bar-row .lbl { width:60px; font-size:11.5px; }
  .scard:hover { transform:none; }
  .card { padding:14px; }
}
@media (hover:none) {
  .scard:hover { transform:none; box-shadow:var(--shadow); }
}
</style>
</head>
<body>
<div class="header">
  <div>
    <h1>WorkBuddy Skill 全景调研</h1>
    <div class="sub">技能 · 专家 · 连接器 —— 分类 / 岗位匹配 / 内网适配 一站式筛选</div>
  </div>
  <div class="meta">
    <div id="genTime"></div>
    <div id="totalCount"></div>
  </div>
</div>

<div class="wrap">
  <div class="kpis" id="kpis"></div>

  <div class="cols">
    <aside class="filters">
      <div class="mtoggle" id="mToggle" onclick="document.querySelector('.filters').classList.toggle('show');this.classList.toggle('open')"></div>
      <div class="card">
        <div class="fgroup searchbox">
          <h4>搜索</h4>
          <input id="q" type="text" placeholder="名称 / 描述 / 触发条件…">
        </div>
        <div class="fgroup">
          <h4>来源 <span class="selectall" data-scope="source">全选</span></h4>
          <div class="chips" id="fSource"></div>
        </div>
        <div class="fgroup">
          <h4>分类 <span class="selectall" data-scope="category">全选</span></h4>
          <div class="chips" id="fCategory"></div>
        </div>
        <div class="fgroup">
          <h4>岗位角色</h4>
          <div class="chips" id="fRole"></div>
        </div>
        <div class="fgroup">
          <h4>内网环境</h4>
          <div class="chips" id="fEnv"></div>
          <div style="font-size:10.5px;color:var(--ink-3);margin-top:4px;line-height:1.5">Honeycomb=内网CLI+DeepSeek可跑本地脚本<br>鲲鹏Max=云端Agent平台+千问纯提示词</div>
        </div>
        <div class="fgroup">
          <h4>该环境适配（最低分）</h4>
          <div class="score-filter chips" id="fScore"></div>
        </div>
        <div class="fgroup">
          <h4>标记状态</h4>
          <div class="chips" id="fMark"></div>
        </div>
      </div>
    </aside>

    <main>
      <div class="card" id="distCard">
        <h3>分布总览 <span class="hint">点击分类条可快速过滤</span></h3>
        <div id="distBars"></div>
      </div>

      <div class="toolbar">
        <div class="count" id="resultCount"></div>
        <span style="flex:1"></span>
        <select id="sortBy" class="btn" style="padding:6px 10px;">
          <option value="default">默认排序</option>
          <option value="score-desc">环境适配 高→低</option>
          <option value="score-asc">环境适配 低→高</option>
          <option value="name">名称 A→Z</option>
        </select>
        <button class="btn" id="btnStarred">只看已收藏</button>
        <button class="btn" id="btnExport">导出标记清单 CSV</button>
        <button class="btn" id="btnReset">重置</button>
      </div>

      <div class="grid" id="cards"></div>
      <div class="empty" id="empty" style="display:none;">没有匹配的条目，试试放宽筛选条件</div>
      <div class="footer" id="footer"></div>
    </main>
  </div>
</div>

<div class="overlay" id="overlay"></div>
<div class="drawer" id="drawer">
  <div class="close" onclick="closeDrawer()">×</div>
  <div id="drawerBody"></div>
</div>
<div class="toast" id="toast"></div>

<script>
const RAW = __PAYLOAD__;

const CAT_COLORS = {"金融投研":"#8E3E71","文档创作":"#2D4869","研究调研":"#3E8E7A","数据分析":"#4A6FA5","网络自动化":"#C07A2D","开发工程":"#5B5B66","多模态创作":"#B85C38","办公协同":"#4E7A5A","法律合规":"#7A4E2D","金融数据":"#8E3E71","技术研发":"#5B5B66","设计创作":"#B85C38","电商零售":"#C07A2D","内容资讯":"#3E8E7A","企业信息":"#4A6FA5","通用服务":"#9A9088","其他":"#9A9088"};
const ROLE_LIST = ["数据岗","产品经理岗","运营岗","管理者","保险业务研究"];
const MARKS = {1:"深入研究",2:"内网移植",3:"外网保留"};
const MARKS_COLOR = {1:"#F26B21",2:"#2D4869",3:"#3E8E5A"};
const SCORE_LABEL = {5:"★★★★★ 可直接用",4:"★★★★ 基本可用",3:"★★★ 部分受限",2:"★★ 强依赖外部",1:"★ 跑不了"};
const ENV_LABEL = {h:"Honeycomb", k:"鲲鹏Max", x:"综合(两者较低值)"};
const ENV_DESC = "Honeycomb：内网CLI+DeepSeek，可跑本地脚本/读文件 · 鲲鹏Max：内网云端Agent平台+千问，纯提示词沙箱";

let records = RAW.records;
let marks = JSON.parse(localStorage.getItem("wb_marks") || "{}");
let filters = {
  q: "", source: new Set(), category: new Set(), role: new Set(),
  scoreMin: 0, mark: "all", starredOnly: false, env: "h",
};

const $ = s => document.querySelector(s);
const esc = s => (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");

function toast(msg) {
  const t = $("#toast"); t.textContent = msg; t.classList.add("show");
  setTimeout(()=>t.classList.remove("show"), 1800);
}
function saveMarks() { localStorage.setItem("wb_marks", JSON.stringify(marks)); }

/* ---------- KPI ---------- */
function renderKPIs() {
  const c = RAW.counts;
  const kpis = [
    [RAW.total, "全部条目"],
    [c.installed, "已安装技能"],
    [c.builtin, "内置能力"],
    [c.official_market, "官方市场可装"],
    [(c.expert||0), "专家包"],
    [(c.connector||0), "连接器"],
    [records.filter(r=>r.intranet_score>=4).length, "可内网适配(≥4分)"],
    [Object.keys(marks).length, "已标记"],
  ];
  $("#kpis").innerHTML = kpis.map(([v,l],i)=>
    `<div class="kpi ${i>=6?'blue':''}"><b>${v}</b><span>${l}</span></div>`).join("");
  $("#genTime").textContent = "生成时间: " + (RAW.generated_at||"").replace("T"," ");
  $("#totalCount").textContent = "Skills · Experts · Connectors";
}

/* ---------- 筛选器 ---------- */
function buildFilters() {
  const sources = [...new Set(records.map(r=>r.source_name))].sort();
  $("#fSource").innerHTML = sources.map(s=>
    `<span class="chip" data-k="${esc(s)}">${esc(s)}</span>`).join("");
  const cats = [...new Set(records.map(r=>r.category))].sort((a,b)=>{
    const ca = records.filter(r=>r.category===a).length, cb = records.filter(r=>r.category===b).length;
    return cb - ca;
  });
  $("#fCategory").innerHTML = cats.map(c=>{
    const n = records.filter(r=>r.category===c).length;
    return `<span class="chip" data-k="${esc(c)}">${esc(c)} <i style="font-style:normal;opacity:.6">${n}</i></span>`;
  }).join("");
  $("#fRole").innerHTML = ROLE_LIST.map(r=>
    `<span class="chip" data-k="${r}">${r}</span>`).join("");
  $("#fEnv").innerHTML = `<span class="chip on" data-k="h">Honeycomb</span><span class="chip" data-k="k">鲲鹏Max</span><span class="chip" data-k="x">综合</span>`;
  $("#fScore").innerHTML = [0,2,3,4,5].map(s=>
    `<span class="chip" data-k="${s}">${s===0?"全部":s+"★+"}</span>`).join("");
  $("#fMark").innerHTML = `<span class="chip on" data-k="all">全部</span>` +
    Object.entries(MARKS).map(([k,v])=>`<span class="chip" data-k="m${k}">${v}</span>`).join("") +
    `<span class="chip" data-k="none">未标记</span>`;

  document.querySelectorAll(".chips .chip").forEach(ch=>{
    ch.onclick = () => {
      const g = ch.parentElement.id;
      const k = ch.dataset.k;
      if (g==="fSource") toggleSet(filters.source, k, ch);
      else if (g==="fCategory") toggleSet(filters.category, k, ch);
      else if (g==="fRole") toggleSet(filters.role, k, ch);
      else if (g==="fEnv") {
        filters.env = k;
        ch.parentElement.querySelectorAll(".chip").forEach(c=>c.classList.remove("on"));
        ch.classList.add("on");
      }
      else if (g==="fScore") {
        filters.scoreMin = +k;
        ch.parentElement.querySelectorAll(".chip").forEach(c=>c.classList.remove("on"));
        ch.classList.add("on");
      } else if (g==="fMark") {
        filters.mark = k;
        ch.parentElement.querySelectorAll(".chip").forEach(c=>c.classList.remove("on"));
        ch.classList.add("on");
      }
      render();
    };
  });
  document.querySelectorAll(".selectall").forEach(sa=>{
    sa.onclick = () => {
      const scope = sa.dataset.scope;
      if (scope==="source") { filters.source.clear(); }
      if (scope==="category") { filters.category.clear(); }
      document.querySelectorAll(`#f${scope[0].toUpperCase()+scope.slice(1)} .chip`).forEach(c=>c.classList.remove("on"));
      render();
    };
  });
}
function toggleSet(set, key, chip) {
  if (set.has(key)) { set.delete(key); chip.classList.remove("on"); }
  else { set.add(key); chip.classList.add("on"); }
}

/* ---------- 分布图 ---------- */
function renderDist() {
  const stats = {};
  records.forEach(r=>{
    stats[r.category] = (stats[r.category]||0)+1;
  });
  const sorted = Object.entries(stats).sort((a,b)=>b[1]-a[1]);
  const max = sorted[0]?.[1] || 1;
  $("#distBars").innerHTML = sorted.map(([cat,n])=>`
    <div class="bar-row" data-cat="${esc(cat)}" style="cursor:pointer" title="点击过滤「${esc(cat)}」">
      <span class="lbl">${esc(cat)}</span>
      <div class="track"><div class="fill" style="width:${(n/max*100).toFixed(1)}%;background:${CAT_COLORS[cat]||'var(--pa-orange)'}"></div></div>
      <span class="val">${n}</span>
    </div>`).join("");
  $("#distBars").querySelectorAll(".bar-row").forEach(row=>{
    row.onclick = () => {
      const cat = row.dataset.cat;
      filters.category = new Set([cat]);
      buildFilters();
      document.querySelectorAll("#fCategory .chip").forEach(c=>{
        c.classList.toggle("on", c.dataset.k===cat);
      });
      render();
      window.scrollTo({top: document.querySelector(".toolbar").offsetTop - 80, behavior:"smooth"});
    };
  });
}

/* ---------- 过滤与渲染 ---------- */
function applyFilters() {
  let list = records.filter(r=>{
    if (filters.q) {
      const q = filters.q.toLowerCase();
      const hay = `${r.name} ${r.description} ${r.when_to_use} ${r.category} ${r.dir_name}`.toLowerCase();
      if (!hay.includes(q)) return false;
    }
    if (filters.source.size && !filters.source.has(r.source_name)) return false;
    if (filters.category.size && !filters.category.has(r.category)) return false;
    if (filters.role.size && !filters.role.some(x=>r.roles.includes(x))) return false;
    const envScore = filters.env==="k" ? (r.kunpeng_score ?? r.intranet_score) : (r.honeycomb_score ?? r.intranet_score);
    if (filters.scoreMin && envScore < filters.scoreMin) return false;
    const m = marks[r.id];
    if (filters.mark==="all") {}
    else if (filters.mark==="none") { if (m) return false; }
    else if (filters.mark.startsWith("m")) { if (m !== +filters.mark[1]) return false; }
    if (filters.starredOnly && !m) return false;
    return true;
  });
  const sort = $("#sortBy").value;
  const es = r => filters.env==="k" ? (r.kunpeng_score ?? r.intranet_score) : (r.honeycomb_score ?? r.intranet_score);
  if (sort==="score-desc") list.sort((a,b)=>es(b)-es(a) || a.name.localeCompare(b.name,"zh"));
  else if (sort==="score-asc") list.sort((a,b)=>es(a)-es(b) || a.name.localeCompare(b.name,"zh"));
  else if (sort==="name") list.sort((a,b)=>a.name.localeCompare(b.name,"zh"));
  return list;
}

function renderCards(list) {
  $("#resultCount").innerHTML = `共 <b>${list.length}</b> 条结果`;
  const frag = [];
  const CHUNK = 120;
  for (let i=0; i<Math.min(list.length, 1000); i++) {
    const r = list[i];
    const m = marks[r.id];
    const hs = r.honeycomb_score ?? r.intranet_score, ks = r.kunpeng_score ?? r.intranet_score;
    frag.push(`
    <div class="scard ${m?'starred':''}" data-id="${esc(r.id)}">
      <div class="top">
        <span class="name">${esc(r.name)}</span>
        <span class="envstars"><i class="eb h" title="Honeycomb：${SCORE_LABEL[hs]}">H${"★".repeat(hs)}</i><i class="eb k" title="鲲鹏Max：${SCORE_LABEL[ks]}">K${"★".repeat(ks)}</i></span>
      </div>
      <div class="desc">${esc(r.description || r.when_to_use || "（无描述）")}</div>
      <div class="tags">
        <span class="tag cat">${esc(r.category)}</span>
        <span class="tag src">${esc(r.source_name)}</span>
        ${(r.roles||[]).map(x=>`<span class="tag role">${esc(x)}</span>`).join("")}
        ${m?`<span class="tag role" style="background:${MARKS_COLOR[m]};color:#fff">${MARKS[m]}</span>`:""}
      </div>
    </div>`);
  }
  if (list.length > 1000) {
    frag.push(`<div class="empty" style="grid-column:1/-1">仅显示前 1000 条，共 ${list.length} 条，请用筛选缩小范围</div>`);
  }
  $("#cards").innerHTML = frag.join("") || "";
  $("#empty").style.display = list.length ? "none" : "block";
  document.querySelectorAll(".scard").forEach(c=>{
    c.onclick = () => openDrawer(c.dataset.id);
  });
}

function render() {
  const list = applyFilters();
  renderCards(list);
  renderKPIs();
}

/* ---------- 抽屉 ---------- */
let curId = null;
function openDrawer(id) {
  curId = id;
  const r = records.find(x=>x.id===id);
  if (!r) return;
  const m = marks[id];
  $("#drawerBody").innerHTML = `
    <h2>${esc(r.name)}</h2>
    <div class="dpath">${esc(r.id)}</div>
    <div class="markbtns">
      ${Object.entries(MARKS).map(([k,v])=>
        `<div class="mbtn ${m===+k?'on-'+k:''}" data-m="${k}">${v}</div>`).join("")
      }
      <div class="mbtn ${!m?'on-3':''}" data-m="0" style="${m?'':'border-color:#bbb'}">清除标记</div>
    </div>
    <div class="sec"><h5>分类</h5><p>${esc(r.category)}${r.category_secondary&&r.category_secondary.length?" · 兼："+r.category_secondary.join("/"):""}</p></div>
    <div class="sec"><h5>来源</h5><p>${esc(r.source_name)}${r.plugin?"（插件："+esc(r.plugin)+"）":""} · 状态：${esc(r.status)}</p></div>
    <div class="sec"><h5>内网环境适配（${ENV_DESC}）</h5>
      <p style="font-size:14px"><b style="color:#B84A08">Honeycomb（CLI+DeepSeek，可跑本地脚本）：</b>${"★".repeat(r.honeycomb_score ?? r.intranet_score)} — ${SCORE_LABEL[r.honeycomb_score ?? r.intranet_score]}</p>
      <p style="font-size:14px"><b style="color:#2D4869">鲲鹏Max（云端Agent平台+千问，纯提示词沙箱）：</b>${"★".repeat(r.kunpeng_score ?? r.intranet_score)} — ${SCORE_LABEL[r.kunpeng_score ?? r.intranet_score]}</p>
    </div>
    ${r.roles&&r.roles.length?`<div class="sec"><h5>岗位匹配</h5><p>${r.roles.map(esc).join(" · ")}</p></div>`:""}
    <div class="sec"><h5>描述</h5><p>${esc(r.description)||"（无）"}</p></div>
    ${r.when_to_use?`<div class="sec"><h5>触发条件</h5><p>${esc(r.when_to_use)}</p></div>`:""}
    <div class="legend">提示：原始文件位于本机 WorkBuddy 目录，可在终端用 open 命令打开。</div>
  `;
  $("#drawer").classList.add("open");
  $("#overlay").classList.add("open");
  document.querySelectorAll(".mbtn").forEach(b=>{
    b.onclick = (e) => {
      e.stopPropagation();
      const mk = +b.dataset.m;
      if (mk===0) delete marks[curId];
      else marks[curId] = mk;
      saveMarks(); render(); openDrawer(curId);
    };
  });
}
function closeDrawer() {
  $("#drawer").classList.remove("open");
  $("#overlay").classList.remove("open");
}
$("#overlay").onclick = closeDrawer;
document.addEventListener("keydown", e=>{ if(e.key==="Escape") closeDrawer(); });

/* ---------- 导出 ---------- */
$("#btnExport").onclick = () => {
  const rows = Object.entries(marks).map(([id,m])=>{
    const r = records.find(x=>x.id===id);
    if (!r) return null;
    return {
      "标记": MARKS[m]||"", "名称": r.name, "分类": r.category,
      "来源": r.source_name, "内网适配分": r.intranet_score,
      "ID": r.id, "描述": (r.description||"").slice(0,120),
    };
  }).filter(Boolean);
  if (!rows.length) { toast("还没有标记任何条目"); return; }
  const head = Object.keys(rows[0]);
  const csv = "\uFEFF" + [head.join(","),
    ...rows.map(r=>head.map(h=>`"${(r[h]+"").replace(/"/g,'""')}"`).join(","))].join("\n");
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([csv],{type:"text/csv"}));
  a.download = "workbuddy_skill_标记清单.csv";
  a.click();
  toast(`已导出 ${rows.length} 条标记`);
};
$("#btnStarred").onclick = () => {
  filters.starredOnly = !filters.starredOnly;
  $("#btnStarred").textContent = filters.starredOnly ? "显示全部" : "只看已收藏";
  $("#btnStarred").classList.toggle("primary", filters.starredOnly);
  render();
};
$("#btnReset").onclick = () => {
  filters = { q:"", source:new Set(), category:new Set(), role:new Set(), scoreMin:0, mark:"all", starredOnly:false };
  $("#q").value = ""; $("#sortBy").value = "default";
  $("#btnStarred").textContent = "只看已收藏"; $("#btnStarred").classList.remove("primary");
  buildFilters();
  $("#fScore .chip[data-k='0']").classList.add("on");
  render();
};
$("#q").oninput = e => { filters.q = e.target.value.trim(); render(); };
$("#sortBy").onchange = render;

$("#footer").textContent = `数据来源：~/.workbuddy 本地扫描 · 共 ${RAW.total} 条 · 标记保存在浏览器 localStorage · 重新生成：python3 scanner/scan_skills.py && python3 scanner/build_dashboard.py`;

/* ---------- init ---------- */
buildFilters();
$("#fScore .chip[data-k='0']").classList.add("on");
renderDist();
render();
</script>
</body>
</html>'''

html = HTML.replace("__PAYLOAD__", payload)
OUT.write_text(html, encoding="utf-8")
print(f"[OK] {OUT} ({OUT.stat().st_size/1024:.0f} KB, {len(data['records'])} records)")

# 同步输出部署目录（CloudStudio 静态部署用）
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)
(DIST / "index.html").write_text(html, encoding="utf-8")
print(f"[OK] {DIST/'index.html'}")
