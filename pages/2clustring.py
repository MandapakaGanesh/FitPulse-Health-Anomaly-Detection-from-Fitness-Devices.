# ═══════════════════════════════════════════════════════════════
#  FITPULSE  ·  MILESTONE 2  ·  mile2_ui.py
#  Biomechanical Observatory  ·  Amber / Coral / Gold
#  Horizontal top-nav  ·  Advanced CSS effects
#  Run:  streamlit run mile2_ui.py
# ═══════════════════════════════════════════════════════════════

import os, io, warnings
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
warnings.filterwarnings("ignore")

try:
    from IPython.display import display
except ImportError:
    display = print

# ── page config ─────────────────────────────────────────────
st.set_page_config(
    page_title="FitPulse · M2",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── page list — defined early so sidebar can reference it ────
PAGES     = ["Overview", "TSFresh", "Prophet", "Clustering"]
NAV_ICONS = ["◎", "⬡", "◉", "◆"]
NAV_DESCS = ["Dataset overview & KPIs",
             "Feature extraction",
             "Forecasting",
             "Segmentation"]

# ── sidebar with Home button ─────────────────────────────────
with st.sidebar:
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] * { font-family: 'Bricolage Grotesque', sans-serif !important; }
    /* Hide Streamlit default multipage nav links */
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] { display: none !important; }
    section[data-testid="stSidebarNav"] { display: none !important; }
    div[data-testid="stSidebarNavItems"] { display: none !important; }
    div[data-testid="stSidebarNavSeparator"] { display: none !important; }
    /* Ensure sidebar scrolls instead of overlapping */
    section[data-testid="stSidebar"] { overflow-y: auto !important; }
    section[data-testid="stSidebar"] > div:first-child { padding-bottom: 16px !important; }
    /* Hide keyboard icon / collapse arrow text */
    button[data-testid="collapsedControl"] { display: none !important; }
    div[data-testid="stSidebar"] [data-testid="stButton"] > button {
        background: rgba(245,166,35,0.08) !important;
        border: 1px solid rgba(245,166,35,0.2) !important;
        color: #f5a623 !important; border-radius: 10px !important;
        font-size: 12px !important; font-weight: 600 !important;
        width: 100% !important; padding: 9px 14px !important;
        transition: all 0.2s ease !important;
        font-family: 'Fira Code', monospace !important;
    }
    div[data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
        background: rgba(245,166,35,0.16) !important;
        border-color: #f5a623 !important;
        box-shadow: 0 0 16px rgba(245,166,35,0.2) !important;
    }
    </style>
    <div style="text-align:center;padding:24px 16px 16px;">
        <div style="width:52px;height:52px;border-radius:15px;
            background:linear-gradient(135deg,#1a1208,#2a1e08);
            border:1px solid rgba(245,166,35,0.4);
            display:flex;align-items:center;justify-content:center;
            margin:0 auto 12px;
            box-shadow:0 0 24px rgba(245,166,35,0.25),inset 0 1px 0 rgba(255,255,255,0.06);">
            <svg width="26" height="26" viewBox="0 0 32 32" fill="none">
                <polyline points="2,16 7,16 10,7 16,26 22,9 26,20 29,16 30,16"
                    stroke="url(#sg2)" stroke-width="2.4"
                    stroke-linecap="round" stroke-linejoin="round"/>
                <defs>
                    <linearGradient id="sg2" x1="0" y1="0" x2="32" y2="0">
                        <stop offset="0%" stop-color="#f5a623"/>
                        <stop offset="100%" stop-color="#ff3c82"/>
                    </linearGradient>
                </defs>
            </svg>
        </div>
        <div style="font-size:15px;font-weight:800;color:#e8e4ff;letter-spacing:0.3px;">
            FitPulse
        </div>
        <div style="font-family:'Fira Code',monospace;font-size:9px;
            color:#4a3820;letter-spacing:2px;text-transform:uppercase;margin-top:3px;">
            Intelligence Lab
        </div>
    </div>
    <div style="height:1px;background:linear-gradient(90deg,transparent,
        rgba(245,166,35,0.18),transparent);margin:0 14px 16px;"></div>
    """, unsafe_allow_html=True)

    if st.button("🏠  Back to Home", key="m2_home_btn"):
        st.switch_page("Home.py")

    st.markdown("""
    <div style="margin-top:12px;">
    <div style="font-family:'Fira Code',monospace;font-size:8px;
        letter-spacing:3px;color:#1e1a10;text-transform:uppercase;
        padding:0 16px 8px;">Sections</div>
    </div>
    """, unsafe_allow_html=True)

    # Page indicator — pre-build strings, no nested quotes in f-string
    _cur_pg = PAGES[st.session_state.get("pg", 0)]
    for _p, _ic in zip(PAGES, ["◎", "⬡", "◉", "◆"]):
        _active  = _p == _cur_pg
        _col     = "#f5a623"              if _active else "#4a4030"
        _bg      = "rgba(245,166,35,0.08)" if _active else "transparent"
        _bdr     = "rgba(245,166,35,0.22)" if _active else "rgba(255,255,255,0.04)"
        _fw      = "700"                  if _active else "400"
        _dot     = ("<span style='margin-left:auto;width:5px;height:5px;"
                    "border-radius:50%;background:#f5a623;"
                    "box-shadow:0 0 6px #f5a623;display:inline-block;'></span>")
        _dot_html = _dot if _active else ""
        _html = (
            f"<div style='display:flex;align-items:center;gap:10px;"
            f"padding:8px 16px;margin-bottom:3px;border-radius:8px;"
            f"background:{_bg};border:1px solid {_bdr};'>"
            f"<span style='font-size:10px;color:{_col};'>{_ic}</span>"
            f"<span style='font-size:11px;color:{_col};font-weight:{_fw};'>{_p}</span>"
            f"{_dot_html}"
            f"</div>"
        )
        st.markdown(_html, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:20px;padding:0 16px 20px;">
        <div style="background:rgba(245,166,35,0.05);
            border:1px solid rgba(245,166,35,0.1);
            border-radius:10px;padding:10px 12px;text-align:center;">
            <div style="font-family:'Fira Code',monospace;
                font-size:8px;color:#2a2010;letter-spacing:1px;line-height:1.9;">
                35 Users · 31 Days<br>2016 Fitbit Dataset
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── colour palette ───────────────────────────────────────────
VOID      = "#07060e"
DEEP      = "#0e0c1a"
LAYER     = "#141228"
CARD      = "#1a1730"
EDGE      = "#2a2545"
AMBER     = "#f5a623"
CORAL     = "#ff6b6b"
GOLD      = "#ffd700"
TEAL      = "#00d4aa"
LAVENDER  = "#b388ff"
TEXT      = "#ede8ff"
MUTED     = "#9896bc"
DIM       = "#6b6890"
PAL       = [AMBER, CORAL, TEAL, LAVENDER, GOLD, "#ff9f43", "#54a0ff", "#5f27cd"]

def mpl_fig(fig, axes):
    fig.patch.set_facecolor(LAYER)
    for ax in (np.array(axes).flat if hasattr(axes, '__iter__') else [axes]):
        ax.set_facecolor(CARD)
        ax.tick_params(colors=MUTED, labelsize=8, length=3)
        ax.xaxis.label.set_color(MUTED)
        ax.yaxis.label.set_color(MUTED)
        ax.title.set_color(AMBER)
        ax.title.set_fontsize(11)
        ax.title.set_fontweight("bold")
        for sp in ax.spines.values():
            sp.set_edgecolor(EDGE)
            sp.set_linewidth(0.8)
        ax.grid(True, color=DIM, linewidth=0.5, linestyle="--", alpha=0.5)
    fig.tight_layout(pad=2)

# ════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Clash+Display:wght@400;500;600;700&family=Bricolage+Grotesque:opsz,wght@12..96,300;400;500;600;700;800&family=Fira+Code:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp { font-family: 'Bricolage Grotesque', sans-serif !important; }

.stApp {
    background-color: #07060e;
    background-image:
        radial-gradient(ellipse 120% 60% at 50% -5%,
            rgba(245,166,35,0.12) 0%, transparent 55%),
        radial-gradient(ellipse 80% 80% at -10% 50%,
            rgba(255,107,107,0.07) 0%, transparent 55%),
        radial-gradient(ellipse 60% 50% at 110% 80%,
            rgba(0,212,170,0.06) 0%, transparent 55%),
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='104'%3E%3Cpath d='M30 0 L60 17.3 L60 51.9 L30 69.3 L0 51.9 L0 17.3 Z' fill='none' stroke='rgba(245,166,35,0.04)' stroke-width='0.5'/%3E%3Cpath d='M30 34.6 L60 51.9 L60 86.6 L30 104 L0 86.6 L0 51.9 Z' fill='none' stroke='rgba(245,166,35,0.04)' stroke-width='0.5'/%3E%3C/svg%3E"),
        linear-gradient(160deg, #0a0917 0%, #07060e 50%, #0b0a1a 100%);
    background-size: 100% 100%, 100% 100%, 100% 100%, 120px 104px, 100% 100%;
    color: #ede8ff;
    min-height: 100vh;
}

.stApp::before {
    content: '';
    position: fixed; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg,
        transparent 0%, rgba(245,166,35,0.0) 10%,
        rgba(245,166,35,0.9) 35%, rgba(255,215,0,1) 50%,
        rgba(255,107,107,0.9) 65%, rgba(0,212,170,0.0) 90%, transparent 100%);
    z-index: 99999; pointer-events: none;
    box-shadow: 0 0 30px rgba(245,166,35,0.4), 0 0 80px rgba(245,166,35,0.15);
}

#MainMenu, footer, header { visibility: hidden !important; }
section[data-testid="stSidebar"] {
    background: #07060f !important;
    background-image: radial-gradient(ellipse 140% 30% at 50% 0%,
        rgba(245,166,35,0.12) 0%, transparent 55%),
        linear-gradient(180deg, #09081a 0%, #06050e 100%) !important;
    border-right: 1px solid rgba(245,166,35,0.1) !important;
    box-shadow: 4px 0 40px rgba(0,0,0,0.6) !important;
}
.block-container { padding: 0 2rem 4rem !important; max-width: 1400px !important; }

/* ── TOP NAV ─────────────────────────────── */
.topnav {
    position: sticky; top: 0; z-index: 9000;
    display: flex; align-items: center;
    padding: 0 32px; height: 64px;
    background: rgba(7,6,14,0.88);
    backdrop-filter: blur(24px) saturate(180%);
    border-bottom: 1px solid rgba(245,166,35,0.12);
    box-shadow: 0 4px 32px rgba(0,0,0,0.6), 0 1px 0 rgba(245,166,35,0.06) inset;
    margin: 0 -2rem 0 -2rem;
    width: calc(100% + 4rem);
}
.topnav-brand {
    display: flex; align-items: center; gap: 12px;
    flex-shrink: 0; margin-right: 40px;
}
.topnav-logo {
    width: 36px; height: 36px; border-radius: 10px;
    background: linear-gradient(135deg, #1a1525, #2a2040);
    border: 1px solid rgba(245,166,35,0.3);
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 0 16px rgba(245,166,35,0.2);
}
.topnav-name { font-family:'Clash Display',sans-serif; font-size:17px; font-weight:700; color:#ede8ff; }
.topnav-badge {
    font-family:'Fira Code',monospace; font-size:9px; color:#f5a623;
    background:rgba(245,166,35,0.1); border:1px solid rgba(245,166,35,0.25);
    border-radius:4px; padding:1px 6px; letter-spacing:1px;
}
.topnav-links { display:flex; align-items:center; gap:4px; flex:1; }
.topnav-link {
    display:flex; align-items:center; gap:7px;
    padding:7px 16px; border-radius:8px;
    font-size:13px; font-weight:500; color:#9896bc;
    border:1px solid transparent; transition:all 0.2s ease;
}
.topnav-link.active {
    color:#f5a623; font-weight:600;
    background:rgba(245,166,35,0.08);
    border-color:rgba(245,166,35,0.2);
    box-shadow:0 0 20px rgba(245,166,35,0.08);
}
.nav-dot { width:5px; height:5px; border-radius:50%; background:#f5a623; box-shadow:0 0 6px #f5a623; display:none; }
.topnav-link.active .nav-dot { display:block; }
.topnav-right { display:flex; align-items:center; gap:10px; margin-left:auto; }
.topnav-stat {
    font-family:'Fira Code',monospace; font-size:10px; color:#8b88b8;
    padding:5px 12px; background:rgba(255,255,255,0.02);
    border:1px solid rgba(255,255,255,0.04); border-radius:6px;
}
.topnav-live {
    display:flex; align-items:center; gap:6px;
    font-family:'Fira Code',monospace; font-size:10px; color:#00d4aa;
    padding:5px 10px; background:rgba(0,212,170,0.06);
    border:1px solid rgba(0,212,170,0.15); border-radius:6px;
}
.live-dot { width:6px; height:6px; border-radius:50%; background:#00d4aa;
    animation:livePulse 1.8s ease-in-out infinite; }
@keyframes livePulse { 0%,100%{opacity:1;box-shadow:0 0 4px #00d4aa;} 50%{opacity:0.4;box-shadow:0 0 10px #00d4aa;} }

/* ── HERO ────────────────────────────────── */
.hero {
    position:relative; overflow:hidden;
    border-radius:24px; padding:52px 52px 48px;
    margin:28px 0 32px;
    background:
        radial-gradient(ellipse 80% 100% at 90% 50%, rgba(245,166,35,0.1) 0%, transparent 60%),
        radial-gradient(ellipse 50% 80% at 10% 50%, rgba(255,107,107,0.07) 0%, transparent 60%),
        linear-gradient(135deg, #120f24 0%, #0e0c1a 60%, #131128 100%);
    border:1px solid rgba(245,166,35,0.15);
    box-shadow:0 0 0 1px rgba(255,255,255,0.03) inset, 0 32px 80px rgba(0,0,0,0.6);
}
.hero-ring {
    position:absolute; right:-80px; top:-80px;
    width:400px; height:400px; border-radius:50%;
    border:1px solid rgba(245,166,35,0.08);
    pointer-events:none; animation:slowSpin 40s linear infinite;
}
.hero-ring::before { content:''; position:absolute; inset:30px; border-radius:50%; border:1px solid rgba(255,107,107,0.06); }
.hero-ring::after  { content:''; position:absolute; inset:60px; border-radius:50%; border:1px solid rgba(0,212,170,0.06); }
@keyframes slowSpin { from{transform:rotate(0deg);} to{transform:rotate(360deg);} }
.hero-hex {
    position:absolute; inset:0; border-radius:24px;
    background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='69.3'%3E%3Cpath d='M20 0 L40 11.5 L40 34.6 L20 46.2 L0 34.6 L0 11.5Z' fill='none' stroke='rgba(245,166,35,0.04)' stroke-width='0.5'/%3E%3Cpath d='M20 23.1 L40 34.6 L40 57.7 L20 69.3 L0 57.7 L0 34.6Z' fill='none' stroke='rgba(245,166,35,0.04)' stroke-width='0.5'/%3E%3C/svg%3E");
    background-size:60px 104px; pointer-events:none; opacity:0.7;
}
.hero-kicker {
    font-family:'Fira Code',monospace; font-size:10px; font-weight:500;
    color:#f5a623; letter-spacing:3px; text-transform:uppercase;
    display:inline-flex; align-items:center; gap:8px; margin-bottom:16px;
}
.hero-kicker::before { content:''; display:inline-block; width:24px; height:1px; background:#f5a623; box-shadow:0 0 8px #f5a623; }
.hero-title {
    font-family:'Clash Display',sans-serif !important;
    font-size:56px !important; font-weight:700 !important;
    line-height:1.05 !important; letter-spacing:-1px;
    background:linear-gradient(135deg, #ede8ff 0%, #f5a623 40%, #ff6b6b 70%, #ffd700 100%);
    background-size:200% auto;
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    animation:gradShift 6s linear infinite; margin-bottom:16px !important;
}
@keyframes gradShift { 0%{background-position:0% center;} 100%{background-position:200% center;} }
.hero-sub { font-size:15px; color:#9896bc; line-height:1.75; max-width:520px; margin-bottom:32px; }
.hero-pills { display:flex; flex-wrap:wrap; gap:8px; }
.hero-pill {
    display:inline-flex; align-items:center; gap:6px;
    padding:7px 16px; border-radius:999px; font-size:12px; font-weight:500;
    background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.07); color:#b0aed4;
}

/* ── KPI ORBIT ───────────────────────────── */
.kpi-orbit { display:grid; grid-template-columns:repeat(5,1fr); gap:16px; margin-bottom:32px; }
.kpi-card {
    position:relative; overflow:hidden;
    background:linear-gradient(135deg,#1a1730,#141228);
    border-radius:18px; padding:24px 20px;
    border:1px solid #2a2545;
    transition:transform 0.3s cubic-bezier(0.34,1.56,0.64,1), border-color 0.3s ease, box-shadow 0.3s ease;
}
.kpi-card:hover { transform:translateY(-6px) scale(1.02); box-shadow:0 20px 60px rgba(0,0,0,0.5); }
.kpi-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:1px;
    background:linear-gradient(90deg,transparent,var(--accent),transparent); opacity:0.6;
}
.kpi-card::after {
    content:''; position:absolute; bottom:-30px; right:-30px;
    width:80px; height:80px; border-radius:50%;
    background:radial-gradient(circle,var(--accent-glow) 0%,transparent 70%);
}
.kpi-amber { --accent:#f5a623; --accent-glow:rgba(245,166,35,0.12); border-left:2px solid #f5a623; }
.kpi-coral { --accent:#ff6b6b; --accent-glow:rgba(255,107,107,0.12); border-left:2px solid #ff6b6b; }
.kpi-teal  { --accent:#00d4aa; --accent-glow:rgba(0,212,170,0.12);  border-left:2px solid #00d4aa; }
.kpi-lav   { --accent:#b388ff; --accent-glow:rgba(179,136,255,0.12);border-left:2px solid #b388ff; }
.kpi-gold  { --accent:#ffd700; --accent-glow:rgba(255,215,0,0.12);  border-left:2px solid #ffd700; }
.kpi-card:hover { border-color:var(--accent); }
.kpi-icon  { font-size:20px; margin-bottom:12px; display:block; }
.kpi-label { font-family:'Fira Code',monospace; font-size:9px; letter-spacing:2px; text-transform:uppercase; color:#8b88b8; margin-bottom:6px; }
.kpi-num   { font-family:'Clash Display',sans-serif; font-size:34px; font-weight:700; color:#ede8ff; line-height:1; margin-bottom:4px; }
.kpi-unit  { font-family:'Fira Code',monospace; font-size:10px; color:#8b88b8; }
.kpi-bar   { height:2px; border-radius:2px; margin-top:14px; background:linear-gradient(90deg,var(--accent),transparent); box-shadow:0 0 8px var(--accent); }
.pulse-ring { position:absolute; top:50%; left:50%; transform:translate(-50%,-50%) scale(0); width:100%; height:100%; border-radius:18px; border:1px solid var(--accent); opacity:0; pointer-events:none; }
.kpi-card:hover .pulse-ring { animation:kpiPulse 0.6s ease-out forwards; }
@keyframes kpiPulse { 0%{transform:translate(-50%,-50%) scale(0.85);opacity:0.6;} 100%{transform:translate(-50%,-50%) scale(1.08);opacity:0;} }

/* ── MODULE HEADER ───────────────────────── */
.mod-header {
    display:flex; align-items:flex-start; gap:20px;
    padding:28px 32px; border-radius:20px;
    background:linear-gradient(135deg,rgba(245,166,35,0.07) 0%,rgba(255,107,107,0.04) 100%);
    border:1px solid rgba(245,166,35,0.13);
    margin-bottom:24px; position:relative; overflow:hidden;
}
.mod-header-line {
    position:absolute; top:0; left:0; bottom:0; width:3px;
    background:linear-gradient(180deg,#f5a623,#ff6b6b,#f5a623);
    border-radius:0 2px 2px 0; box-shadow:0 0 12px rgba(245,166,35,0.5);
}
.mod-icon { font-size:32px; flex-shrink:0; }
.mod-code {
    font-family:'Fira Code',monospace; font-size:9px; color:#f5a623;
    background:rgba(245,166,35,0.1); border:1px solid rgba(245,166,35,0.2);
    border-radius:4px; padding:2px 8px; display:inline-block; margin-bottom:6px; letter-spacing:1.5px;
}
.mod-title { font-family:'Clash Display',sans-serif; font-size:22px; font-weight:700; color:#ede8ff; margin-bottom:4px; }
.mod-desc  { font-size:12px; color:#8b88b8; line-height:1.6; }

/* ── GLASS PANEL ─────────────────────────── */
.glass-panel {
    background:rgba(20,18,40,0.7); backdrop-filter:blur(16px);
    border:1px solid rgba(245,166,35,0.1); border-radius:18px; padding:24px;
    margin-bottom:20px;
    box-shadow:0 8px 32px rgba(0,0,0,0.4), 0 1px 0 rgba(255,255,255,0.03) inset;
    position:relative; overflow:hidden;
}
.glass-panel::before {
    content:''; position:absolute; top:0; left:0; right:0; height:1px;
    background:linear-gradient(90deg,transparent,rgba(245,166,35,0.2),rgba(255,107,107,0.15),transparent);
}
.panel-label {
    font-family:'Fira Code',monospace; font-size:9px; letter-spacing:2.5px;
    text-transform:uppercase; color:#8b88b8; margin-bottom:14px;
    display:flex; align-items:center; gap:10px;
}
.panel-label::after { content:''; flex:1; height:1px; background:linear-gradient(90deg,rgba(245,166,35,0.15),transparent); }

/* ── DIVIDER ─────────────────────────────── */
.v-div { height:1px; border:none; margin:32px 0; background:linear-gradient(90deg,transparent,rgba(245,166,35,0.25),rgba(255,107,107,0.15),transparent); }

/* ── TERMINAL ────────────────────────────── */
.term {
    background:#060510; border:1px solid #1a1530; border-radius:12px;
    padding:20px 22px; font-family:'Fira Code',monospace;
    font-size:11px; line-height:2; color:#8b88b8; margin-bottom:16px;
}
.term .ok   { color:#00d4aa; }
.term .hi   { color:#f5a623; }
.term .val  { color:#b388ff; }
.term .warn { color:#ff6b6b; }

/* ── CHIPS ───────────────────────────────── */
.chip { display:inline-flex; align-items:center; gap:5px; padding:5px 14px; border-radius:999px; font-size:11px; font-weight:600; margin:3px; font-family:'Fira Code',monospace; }
.chip-a { background:rgba(245,166,35,0.1); border:1px solid rgba(245,166,35,0.3); color:#f5a623; }
.chip-b { background:rgba(0,212,170,0.1);  border:1px solid rgba(0,212,170,0.3);  color:#00d4aa; }
.chip-c { background:rgba(255,107,107,0.1);border:1px solid rgba(255,107,107,0.3);color:#ff6b6b; }
.chip-d { background:rgba(179,136,255,0.1);border:1px solid rgba(179,136,255,0.3);color:#b388ff; }

/* ── Streamlit overrides ─────────────────── */
[data-testid="metric-container"] { background:#1a1730 !important; border:1px solid #2a2545 !important; border-radius:14px !important; padding:20px !important; }
[data-testid="stDataFrame"] { background:#14122a !important; border:1px solid #2a2545 !important; border-radius:12px !important; }
div[data-testid="stButton"] > button {
    background:linear-gradient(135deg,rgba(245,166,35,0.12),rgba(255,107,107,0.08)) !important;
    border:1px solid rgba(245,166,35,0.3) !important; color:#f5a623 !important;
    border-radius:10px !important; font-family:'Fira Code',monospace !important;
    font-size:12px !important; transition:all 0.2s ease !important;
}
div[data-testid="stButton"] > button:hover {
    background:linear-gradient(135deg,rgba(245,166,35,0.22),rgba(255,107,107,0.15)) !important;
    border-color:#f5a623 !important; box-shadow:0 0 24px rgba(245,166,35,0.3) !important;
    transform:translateY(-2px) !important;
}
div[data-testid="stSelectbox"] > div > div { background:#1a1730 !important; border-color:#2a2545 !important; color:#ede8ff !important; }
h1,h2,h3 { font-family:'Clash Display',sans-serif !important; color:#ede8ff !important; }
.stRadio > label { display:none !important; }

/* ── Animations ──────────────────────────── */
@keyframes fadeUp { from{opacity:0;transform:translateY(20px);} to{opacity:1;transform:translateY(0);} }
.f1{animation:fadeUp 0.5s ease both;} .f2{animation:fadeUp 0.5s ease 0.08s both;}
.f3{animation:fadeUp 0.5s ease 0.16s both;} .f4{animation:fadeUp 0.5s ease 0.24s both;}
.f5{animation:fadeUp 0.5s ease 0.32s both;}

::-webkit-scrollbar{width:5px;height:5px;} ::-webkit-scrollbar-track{background:#07060e;}
::-webkit-scrollbar-thumb{background:#2a2545;border-radius:3px;} ::-webkit-scrollbar-thumb:hover{background:#f5a623;}

/* ── ANIMATED COUNTER ────────────────────── */
@keyframes countUp {
    from { opacity:0; transform:translateY(8px); }
    to   { opacity:1; transform:translateY(0); }
}
.kpi-num { animation: countUp 0.6s cubic-bezier(0.34,1.56,0.64,1) both; }

/* ── TOOLTIP ─────────────────────────────── */
.tooltip-wrap { position:relative; display:inline-block; }
.tooltip-wrap .tooltip-box {
    visibility:hidden; opacity:0;
    position:absolute; bottom:calc(100% + 8px); left:50%;
    transform:translateX(-50%) translateY(4px);
    background:linear-gradient(135deg,#1e1a38,#160f2e);
    border:1px solid rgba(245,166,35,0.25);
    border-radius:10px; padding:10px 14px;
    font-family:'Fira Code',monospace; font-size:10px;
    color:#c8c4e8; line-height:1.7; white-space:nowrap;
    box-shadow:0 8px 32px rgba(0,0,0,0.6);
    transition:all 0.2s ease; pointer-events:none;
    z-index:9999;
}
.tooltip-wrap .tooltip-box::after {
    content:''; position:absolute; top:100%; left:50%;
    transform:translateX(-50%);
    border:5px solid transparent;
    border-top-color:rgba(245,166,35,0.25);
}
.tooltip-wrap:hover .tooltip-box {
    visibility:visible; opacity:1; transform:translateX(-50%) translateY(0);
}

/* ── INSIGHT BADGE ───────────────────────── */
.insight-badge {
    display:inline-flex; align-items:center; gap:6px;
    padding:6px 14px; border-radius:8px;
    font-family:'Fira Code',monospace; font-size:11px;
    font-weight:600; margin:4px 4px 4px 0;
    transition:all 0.2s ease;
}
.badge-up   { background:rgba(0,212,170,0.12); border:1px solid rgba(0,212,170,0.3); color:#00d4aa; }
.badge-down { background:rgba(255,107,107,0.12); border:1px solid rgba(255,107,107,0.3); color:#ff6b6b; }
.badge-neutral { background:rgba(245,166,35,0.12); border:1px solid rgba(245,166,35,0.3); color:#f5a623; }

/* ── COLLAPSIBLE SECTION ─────────────────── */
details.data-expander {
    background:rgba(20,18,40,0.5);
    border:1px solid rgba(245,166,35,0.08);
    border-radius:12px; margin-top:12px; overflow:hidden;
}
details.data-expander summary {
    padding:12px 18px; cursor:pointer;
    font-family:'Fira Code',monospace; font-size:11px;
    color:#8b88b8; letter-spacing:1px;
    list-style:none; display:flex; align-items:center; gap:8px;
    transition:color 0.2s ease;
}
details.data-expander summary:hover { color:#f5a623; }
details.data-expander summary::before {
    content:'▶'; font-size:8px; transition:transform 0.2s ease;
}
details.data-expander[open] summary::before { transform:rotate(90deg); }
details.data-expander[open] summary { color:#f5a623; border-bottom:1px solid rgba(245,166,35,0.08); }

/* ── DOWNLOAD BUTTON STYLE ───────────────── */
.dl-btn {
    display:inline-flex; align-items:center; gap:8px;
    padding:8px 18px; border-radius:8px;
    background:rgba(245,166,35,0.08);
    border:1px solid rgba(245,166,35,0.2);
    color:#f5a623; font-family:'Fira Code',monospace;
    font-size:11px; cursor:pointer; text-decoration:none;
    transition:all 0.2s ease; margin-top:10px;
}
.dl-btn:hover { background:rgba(245,166,35,0.16); border-color:#f5a623; box-shadow:0 0 16px rgba(245,166,35,0.2); }

/* ── STAT COMPARISON ROW ─────────────────── */
.stat-row {
    display:grid; grid-template-columns:repeat(3,1fr);
    gap:10px; margin:12px 0;
}
.stat-cell {
    background:rgba(255,255,255,0.02);
    border:1px solid rgba(255,255,255,0.05);
    border-radius:10px; padding:14px 16px; text-align:center;
}
.stat-cell-val { font-family:'Clash Display',sans-serif; font-size:22px; font-weight:700; color:#ede8ff; }
.stat-cell-lbl { font-family:'Fira Code',monospace; font-size:9px; color:#8b88b8; letter-spacing:1.5px; text-transform:uppercase; margin-top:4px; }
.stat-cell-delta { font-family:'Fira Code',monospace; font-size:10px; margin-top:4px; }
.delta-up   { color:#00d4aa; }
.delta-down { color:#ff6b6b; }

/* ── PROGRESS TRACK ──────────────────────── */
.prog-track {
    background:rgba(255,255,255,0.04);
    border-radius:999px; height:6px; margin:6px 0 14px;
    overflow:hidden; position:relative;
}
.prog-fill {
    height:100%; border-radius:999px;
    background:linear-gradient(90deg,#f5a623,#ff6b6b);
    box-shadow:0 0 10px rgba(245,166,35,0.4);
    transition:width 1s cubic-bezier(0.34,1.56,0.64,1);
}

/* ── CLUSTER CARD ────────────────────────── */
.cluster-int-card {
    border-radius:14px; padding:16px 18px;
    margin-bottom:12px; position:relative; overflow:hidden;
    transition:all 0.25s ease;
}
.cluster-int-card:hover { transform:translateX(4px); }
.cluster-int-card::before {
    content:''; position:absolute; left:0; top:0; bottom:0; width:3px;
    background:var(--c-accent); box-shadow:0 0 10px var(--c-accent);
}
.c-amber { --c-accent:#f5a623; background:rgba(245,166,35,0.06); border:1px solid rgba(245,166,35,0.15); }
.c-teal  { --c-accent:#00d4aa; background:rgba(0,212,170,0.06);  border:1px solid rgba(0,212,170,0.15); }
.c-coral { --c-accent:#ff6b6b; background:rgba(255,107,107,0.06);border:1px solid rgba(255,107,107,0.15); }
.c-lav   { --c-accent:#b388ff; background:rgba(179,136,255,0.06);border:1px solid rgba(179,136,255,0.15); }
.cluster-int-head { display:flex; align-items:center; justify-content:space-between; margin-bottom:10px; }
.cluster-int-name { font-family:'Clash Display',sans-serif; font-size:16px; font-weight:700; color:#ede8ff; }
.cluster-int-tag  { font-family:'Fira Code',monospace; font-size:9px; color:var(--c-accent); letter-spacing:1px; text-transform:uppercase; }
.cluster-int-row  { display:flex; justify-content:space-between; padding:4px 0; border-bottom:1px solid rgba(255,255,255,0.04); font-family:'Fira Code',monospace; font-size:11px; }
.cluster-int-row:last-child { border-bottom:none; }
.cluster-int-key  { color:#8b88b8; }
.cluster-int-val  { color:#ede8ff; font-weight:600; }

/* ── SECTION PROGRESS STEPS ─────────────── */
.steps-track {
    display:flex; align-items:center; gap:0;
    padding:16px 24px; margin:20px 0;
    background:rgba(255,255,255,0.02);
    border:1px solid rgba(255,255,255,0.05);
    border-radius:14px;
}
.step-node {
    display:flex; flex-direction:column; align-items:center;
    gap:6px; flex:1; position:relative;
}
.step-node::after {
    content:''; position:absolute; top:15px; left:60%; right:-40%;
    height:1px; background:rgba(255,255,255,0.08);
}
.step-node:last-child::after { display:none; }
.step-circle {
    width:30px; height:30px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:11px; font-weight:700; font-family:'Fira Code',monospace;
    border:1px solid rgba(255,255,255,0.1);
    background:rgba(255,255,255,0.04); color:#8b88b8; z-index:1;
}
.step-circle.s-done {
    background:rgba(0,212,170,0.15); border-color:#00d4aa;
    color:#00d4aa; box-shadow:0 0 12px rgba(0,212,170,0.2);
}
.step-circle.s-active {
    background:linear-gradient(135deg,rgba(245,166,35,0.2),rgba(255,107,107,0.15));
    border-color:#f5a623; color:#f5a623; box-shadow:0 0 16px rgba(245,166,35,0.3);
}
.step-node::after { top:15px; }
.step-node.s-done-conn::after { background:linear-gradient(90deg,#00d4aa,rgba(255,255,255,0.08)); }
.step-lbl { font-family:'Fira Code',monospace; font-size:9px; color:#8b88b8; letter-spacing:1px; white-space:nowrap; text-align:center; }
.step-lbl.s-active { color:#f5a623; }
.step-lbl.s-done   { color:#00d4aa; }

/* ── SEARCH INPUT ────────────────────────── */
div[data-testid="stTextInput"] input {
    background:#1a1730 !important; border:1px solid #2a2545 !important;
    color:#ede8ff !important; border-radius:10px !important;
    font-family:'Fira Code',monospace !important; font-size:12px !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color:rgba(245,166,35,0.5) !important;
    box-shadow:0 0 16px rgba(245,166,35,0.12) !important;
}
div[data-testid="stTextInput"] label { color:#8b88b8 !important; font-size:11px !important; }

/* ── EXPANDER ────────────────────────────── */
div[data-testid="stExpander"] {
    background:#141228 !important; border:1px solid #2a2545 !important;
    border-radius:12px !important;
}
div[data-testid="stExpander"] summary { color:#8b88b8 !important; }
div[data-testid="stExpander"] summary:hover { color:#f5a623 !important; }
div[data-testid="stExpander"][open] summary { color:#f5a623 !important; }

/* ── INFO STRIP ──────────────────────────── */
.info-strip {
    display:flex; align-items:center; gap:12px;
    padding:10px 16px; border-radius:10px;
    background:rgba(0,212,170,0.06); border:1px solid rgba(0,212,170,0.15);
    font-family:'Fira Code',monospace; font-size:11px; color:#7be8cc;
    margin:10px 0;
}
.warn-strip {
    display:flex; align-items:center; gap:12px;
    padding:10px 16px; border-radius:10px;
    background:rgba(255,184,0,0.06); border:1px solid rgba(255,184,0,0.15);
    font-family:'Fira Code',monospace; font-size:11px; color:#f5d060;
    margin:10px 0;
}

/* ── TOPNAV link hover ───────────────────── */
.topnav-link:hover { color:#c8c4e8 !important; background:rgba(255,255,255,0.04); }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  DATA LOADING  ·  Upload-based (same approach as Milestone 3)
# ════════════════════════════════════════════════════════════════

# ── Session-state defaults ───────────────────────────────────
for _k, _v in [
    ("m2_files_loaded", False),
    ("m2_daily",    None), ("m2_hourly_s", None),
    ("m2_sleep",    None), ("m2_hr_minute",None),
    ("m2_master",   None),
]:
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ── Required-file registry (same as M3, minus hourlyIntensities) ─
M2_REQUIRED_FILES = {
    "dailyActivity_merged.csv":     {"key_cols": ["ActivityDate", "TotalSteps", "Calories"],  "label": "Daily Activity",    "icon": "🏃"},
    "hourlySteps_merged.csv":       {"key_cols": ["ActivityHour", "StepTotal"],               "label": "Hourly Steps",      "icon": "👣"},
    "minuteSleep_merged.csv":       {"key_cols": ["date", "value", "logId"],                  "label": "Minute Sleep",      "icon": "💤"},
    "heartrate_seconds_merged.csv": {"key_cols": ["Time", "Value"],                           "label": "Heart Rate",        "icon": "❤️"},
}

def _score_match(df, req_info):
    return sum(1 for col in req_info["key_cols"] if col in df.columns)

def _build_master_from_dfs(daily_raw, hr_raw, sleep_raw):
    """Build master DataFrame from uploaded raw DataFrames.

    Fast path for HR: floor-truncate timestamps to the minute instead of using
    the slow groupby+resample API.  On 127 K rows this is ~10× faster.
    """
    daily = daily_raw.copy()
    sleep = sleep_raw.copy()

    # ── Parse dates ──────────────────────────────────────────
    daily["ActivityDate"] = pd.to_datetime(
        daily["ActivityDate"], format="mixed", errors="coerce"
    )
    sleep["date"] = pd.to_datetime(
        sleep["date"], format="mixed", errors="coerce"
    )

    # ── Heart-rate: fast minute-level aggregation ─────────────
    # Work only with the columns we need; use a lightweight dtype
    hr = hr_raw[["Id", "Time", "Value"]].copy()
    hr["Id"]    = hr["Id"].astype("int32")
    hr["Value"] = pd.to_numeric(hr["Value"], errors="coerce")
    hr["Time"]  = pd.to_datetime(hr["Time"], format="mixed", errors="coerce")
    hr.dropna(subset=["Time", "Value"], inplace=True)

    # Floor to minute bucket — O(n) vs O(n log n) resample
    hr["MinuteBucket"] = hr["Time"].dt.floor("min")
    hr_minute = (
        hr.groupby(["Id", "MinuteBucket"])["Value"]
          .mean()
          .reset_index()
          .rename(columns={"MinuteBucket": "Time", "Value": "HeartRate"})
    )
    hr_minute["Date"] = hr_minute["Time"].dt.date

    # Daily HR stats straight from minute data
    hr_daily = (
        hr_minute.groupby(["Id", "Date"])["HeartRate"]
                 .agg(["mean", "max", "min", "std"])
                 .reset_index()
                 .rename(columns={"mean": "AvgHR", "max": "MaxHR",
                                  "min": "MinHR",  "std": "StdHR"})
    )

    # ── Sleep daily ───────────────────────────────────────────
    sleep["Date"] = sleep["date"].dt.date
    sleep_daily = (
        sleep.groupby(["Id", "Date"])
             .agg(
                 TotalSleepMinutes=("value", "count"),
                 DominantSleepStage=("value", lambda x: x.mode()[0])
             )
             .reset_index()
    )

    # ── Merge into master ─────────────────────────────────────
    master = daily.copy().rename(columns={"ActivityDate": "Date"})
    master["Date"] = master["Date"].dt.date
    master = master.merge(hr_daily,    on=["Id", "Date"], how="left")
    master = master.merge(sleep_daily, on=["Id", "Date"], how="left")
    master["TotalSleepMinutes"]  = master["TotalSleepMinutes"].fillna(0)
    master["DominantSleepStage"] = master["DominantSleepStage"].fillna(0)
    for c in ["AvgHR", "MaxHR", "MinHR", "StdHR"]:
        master[c] = master.groupby("Id")[c].transform(
            lambda x: x.fillna(x.median())
        )

    return master, hr_minute

# ── File-upload UI (shown until data is loaded) ──────────────
if not st.session_state.m2_files_loaded:
    st.markdown("""
    <div style="margin:28px 0 8px;">
    <div style="font-family:'Fira Code',monospace;font-size:10px;letter-spacing:3px;
        color:#f5a623;text-transform:uppercase;margin-bottom:6px;">📂 Data Loading</div>
    <div style="font-size:22px;font-weight:800;color:#ede8ff;margin-bottom:6px;">
        Upload Fitbit CSV Files</div>
    <div style="font-size:13px;color:#9896bc;">
        Drop all 4 required Fitbit CSV files below. Files are auto-detected by
        column structure — drop them in any order.</div>
    </div>
    """, unsafe_allow_html=True)

    _info_html = (
        '<div style="display:flex;align-items:center;gap:10px;padding:10px 16px;'
        'border-radius:10px;background:rgba(245,166,35,0.06);'
        'border:1px solid rgba(245,166,35,0.18);font-family:Fira Code,monospace;'
        'font-size:11px;color:#f5c97a;margin-bottom:18px;">'
        'ℹ️&nbsp;&nbsp;Same 4 Fitbit CSVs used in Milestone 2 — '
        'dailyActivity, hourlySteps, minuteSleep, heartrate_seconds</div>'
    )
    st.markdown(_info_html, unsafe_allow_html=True)

    _uploaded = st.file_uploader(
        "📁  Drop CSV files here",
        type="csv", accept_multiple_files=True, key="m2_uploader",
        help="Hold Ctrl / Cmd to select multiple files at once"
    )

    # Auto-detect which file is which by column signature
    _detected = {}
    if _uploaded:
        _raw_uploads = []
        for _uf in _uploaded:
            try:
                _raw_uploads.append((_uf.name, pd.read_csv(_uf)))
            except Exception:
                pass
        for _req, _finfo in M2_REQUIRED_FILES.items():
            _best_s, _best_df = 0, None
            for _uname, _udf in _raw_uploads:
                _s = _score_match(_udf, _finfo)
                if _s > _best_s:
                    _best_s, _best_df = _s, _udf
            if _best_s >= 2:
                _detected[_req] = _best_df

    # Status grid
    _grid_html = '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0;">'
    for _req, _finfo in M2_REQUIRED_FILES.items():
        _found = _req in _detected
        _bg    = "rgba(0,212,170,0.07)" if _found else "rgba(255,107,107,0.06)"
        _bdr   = "rgba(0,212,170,0.25)" if _found else "rgba(255,107,107,0.18)"
        _ico   = "✅" if _found else "❌"
        _grid_html += (
            f'<div style="background:{_bg};border:1px solid {_bdr};border-radius:12px;'
            f'padding:14px 16px;text-align:center;">'
            f'<div style="font-size:1.3rem">{_ico} {_finfo["icon"]}</div>'
            f'<div style="font-size:0.78rem;font-weight:600;color:#ede8ff;margin-top:6px">'
            f'{_finfo["label"]}</div>'
            f'<div style="font-family:Fira Code,monospace;font-size:0.65rem;'
            f'color:#9896bc;margin-top:2px">{"Found ✓" if _found else "Missing"}</div>'
            f'</div>'
        )
    _grid_html += '</div>'
    st.markdown(_grid_html, unsafe_allow_html=True)

    _n_up = len(_detected)
    # KPI mini-row
    _kpi_html = '<div style="display:flex;gap:12px;margin-bottom:18px;">'
    for _ic, _lbl, _val, _unit, _ok in [
        ("📁", "Files Detected", str(_n_up),      "/ 4",    True),
        ("❌", "Files Missing",  str(4 - _n_up),  "files",  _n_up == 4),
        ("✅", "Status",         "Ready" if _n_up == 4 else "Waiting", "", _n_up == 4),
    ]:
        _c = "rgba(0,212,170,0.08)" if _ok else "rgba(245,166,35,0.08)"
        _bc = "rgba(0,212,170,0.2)" if _ok else "rgba(245,166,35,0.2)"
        _tc = "#00d4aa" if _ok else "#f5a623"
        _kpi_html += (
            f'<div style="flex:1;background:{_c};border:1px solid {_bc};'
            f'border-radius:12px;padding:14px 18px;text-align:center;">'
            f'<div style="font-size:1.1rem">{_ic}</div>'
            f'<div style="font-family:Fira Code,monospace;font-size:8px;'
            f'color:#9896bc;letter-spacing:1.5px;text-transform:uppercase;margin-top:4px">{_lbl}</div>'
            f'<div style="font-size:1.6rem;font-weight:800;color:{_tc};line-height:1.2">{_val}</div>'
            f'<div style="font-family:Fira Code,monospace;font-size:9px;color:#9896bc">{_unit}</div>'
            f'</div>'
        )
    _kpi_html += '</div>'
    st.markdown(_kpi_html, unsafe_allow_html=True)

    if _n_up < 4:
        _missing_labels = [M2_REQUIRED_FILES[r]["label"] for r in M2_REQUIRED_FILES if r not in _detected]
        st.warning(f"⚠️  Missing: {', '.join(_missing_labels)}")

    if st.button("⚡  Load & Build Master DataFrame", disabled=(_n_up < 4), key="m2_load_btn"):
        with st.spinner("Parsing and merging all datasets… (this may take ~20 seconds for the HR file)"):
            try:
                _master, _hr_min = _build_master_from_dfs(
                    _detected["dailyActivity_merged.csv"],
                    _detected["heartrate_seconds_merged.csv"],
                    _detected["minuteSleep_merged.csv"],
                )
                st.session_state.update({
                    "m2_daily":     _detected["dailyActivity_merged.csv"].copy(),
                    "m2_hourly_s":  _detected["hourlySteps_merged.csv"].copy(),
                    "m2_sleep":     _detected["minuteSleep_merged.csv"].copy(),
                    "m2_hr_minute": _hr_min,   # minute-level, not raw seconds
                    "m2_master":    _master,
                    "m2_files_loaded": True,
                })
                st.rerun()
            except Exception as _e:
                st.error(f"❌  Error building master DataFrame: {_e}")

    st.stop()   # Don't render the rest of the app until data is loaded

# ── Pull loaded data from session state ──────────────────────
daily    = st.session_state.m2_daily
hourly_s = st.session_state.m2_hourly_s
sleep    = st.session_state.m2_sleep
hr       = st.session_state.m2_hr_minute   # minute-level HR
master   = st.session_state.m2_master

# Sidebar reload button
with st.sidebar:
    st.markdown("""
    <div style="height:1px;background:linear-gradient(90deg,transparent,
        rgba(245,166,35,0.18),transparent);margin:8px 14px 12px;"></div>
    """, unsafe_allow_html=True)
    if st.button("🔄  Load Different Files", key="m2_reload_btn"):
        for _k in ["m2_files_loaded","m2_daily","m2_hourly_s","m2_sleep",
                   "m2_hr_minute","m2_master"]:
            st.session_state[_k] = False if _k == "m2_files_loaded" else None
        st.rerun()
    _n_users  = master["Id"].nunique()
    _n_days   = master["Date"].nunique()
    _n_hr_pts = hr.shape[0]
    st.markdown(
        f'<div style="background:rgba(245,166,35,0.05);border:1px solid rgba(245,166,35,0.1);'
        f'border-radius:10px;padding:10px 12px;text-align:center;margin-top:8px;">'
        f'<div style="font-family:Fira Code,monospace;font-size:8px;color:#4a3820;'
        f'letter-spacing:1px;line-height:2;">'
        f'{_n_users} Users · {_n_days} Days<br>{_n_hr_pts:,} HR records</div></div>',
        unsafe_allow_html=True
    )

@st.cache_data(show_spinner=False)
def get_tsfresh(_hr):
    from tsfresh import extract_features
    from tsfresh.feature_extraction import MinimalFCParameters
    ts = (_hr[["Id","Time","HeartRate"]].dropna()
           .sort_values(["Id","Time"])
           .rename(columns={"Id":"id","Time":"time","HeartRate":"value"}))
    f = extract_features(ts, column_id="id", column_sort="time",
                         column_value="value",
                         default_fc_parameters=MinimalFCParameters(),
                         disable_progressbar=True, n_jobs=1)
    return f.dropna(axis=1, how="all")

@st.cache_data(show_spinner=False)
def get_prophet_hr(_hr):
    from prophet import Prophet
    import logging; logging.getLogger("cmdstanpy").setLevel(logging.ERROR)
    tmp = _hr.copy(); tmp["Date"] = tmp["Time"].dt.date
    p = tmp.groupby("Date")["HeartRate"].mean().reset_index()
    p.columns = ["ds","y"]; p["ds"] = pd.to_datetime(p["ds"])
    p = p.dropna().sort_values("ds")
    m = Prophet(weekly_seasonality=True, yearly_seasonality=False,
                daily_seasonality=False, interval_width=0.80, changepoint_prior_scale=0.1)
    m.fit(p); fc = m.predict(m.make_future_dataframe(periods=30))
    return p, fc

@st.cache_data(show_spinner=False)
def get_prophet_metric(_master, metric):
    from prophet import Prophet
    import logging; logging.getLogger("cmdstanpy").setLevel(logging.ERROR)
    p = _master.groupby("Date")[metric].mean().reset_index()
    p.columns = ["ds","y"]; p["ds"] = pd.to_datetime(p["ds"])
    p = p.dropna().sort_values("ds")
    m = Prophet(weekly_seasonality=True, yearly_seasonality=False,
                daily_seasonality=False, interval_width=0.80, changepoint_prior_scale=0.1)
    m.fit(p); fc = m.predict(m.make_future_dataframe(periods=30))
    return p, fc

@st.cache_data(show_spinner=False)
def get_clustering(_master):
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans, DBSCAN
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE
    cols = ["TotalSteps","Calories","VeryActiveMinutes","FairlyActiveMinutes",
            "LightlyActiveMinutes","SedentaryMinutes","TotalSleepMinutes"]
    for c in ["AvgHR","MaxHR","MinHR","StdHR"]:
        if c in _master.columns:
            if _master[c].notna().groupby(_master["Id"]).any().mean() > 0.5:
                cols.append(c)
    cf = _master.groupby("Id")[cols].mean().round(3)
    for c in cf.columns: cf[c] = cf[c].fillna(cf[c].median())
    cf = cf.dropna()
    X  = StandardScaler().fit_transform(cf)
    n  = cf.shape[0]; K = min(3, n)
    km = KMeans(n_clusters=K, random_state=42, n_init=10).fit_predict(X)
    db = DBSCAN(eps=1.8, min_samples=2).fit_predict(X)
    pca  = PCA(n_components=2, random_state=42); Xp = pca.fit_transform(X)
    tsne = TSNE(n_components=2, random_state=42, perplexity=min(30,n-1), max_iter=1000)
    Xt   = tsne.fit_transform(X)
    cf["KMeans_Cluster"] = km; cf["DBSCAN_Cluster"] = db
    nc = len(set(db))-(1 if -1 in db else 0); nn = list(db).count(-1)
    ve = pca.explained_variance_ratio_*100
    return cf, cols, X, km, db, Xp, Xt, K, nc, nn, ve

# ── Page index session state ─────────────────────────────────
if "pg" not in st.session_state:
    st.session_state["pg"] = 0

# ── Resolve page from session state ─────────────────────────
cur  = st.session_state["pg"]
page = PAGES[cur]

# ════════════════════════════════════════════════════════════════
#  TOP NAV  (decorative HTML — mirrors session state)
# ════════════════════════════════════════════════════════════════
links_html = ""
for i, (p, ic) in enumerate(zip(PAGES, NAV_ICONS)):
    cls = "active" if i == cur else ""
    links_html += (
        f'<div class="topnav-link {cls}">'
        f'<span class="nav-dot"></span>'
        f'<span style="font-size:11px;opacity:0.5;">{ic}</span>'
        f'<span>{p}</span></div>'
    )

st.markdown(f"""
<div class="topnav">
    <div class="topnav-brand">
        <div class="topnav-logo">
            <svg width="20" height="20" viewBox="0 0 32 32" fill="none">
                <polyline points="3,16 9,16 12,7 16,25 20,11 24,20 27,16 29,16"
                    stroke="#f5a623" stroke-width="2.2" stroke-linecap="round"
                    stroke-linejoin="round" fill="none"/>
            </svg>
        </div>
        <div class="topnav-name">FitPulse</div>
        <span class="topnav-badge">M2</span>
    </div>
    <div class="topnav-links">{links_html}</div>
    <div class="topnav-right">
        <div class="topnav-stat">35 users · 31 days</div>
        <div class="topnav-live"><span class="live-dot"></span> LIVE</div>
    </div>
</div>""", unsafe_allow_html=True)

# ── Nav buttons (the ONLY source of truth for navigation) ───
# Style active button differently via injected CSS
active_btn_css = ""
for i, p in enumerate(PAGES):
    if i == cur:
        active_btn_css += f"""
div[data-testid="stButton"]:has(button[kind="secondary"][data-testid*="nav_{p}"]) > button,
div[data-testid="column"]:nth-child({i+2}) div[data-testid="stButton"] > button {{
    background: linear-gradient(135deg, rgba(245,166,35,0.22),
        rgba(255,107,107,0.15)) !important;
    border-color: #f5a623 !important;
    color: #f5a623 !important;
    box-shadow: 0 0 20px rgba(245,166,35,0.25) !important;
}}"""
st.markdown(f"<style>{active_btn_css}</style>", unsafe_allow_html=True)

nb = st.columns(len(PAGES) + 2)
for i, (p, ic, desc) in enumerate(zip(PAGES, NAV_ICONS, NAV_DESCS)):
    with nb[i + 1]:
        if st.button(f"{ic}  {p}", key=f"nav_{p}", use_container_width=True,
                     help=desc):
            st.session_state["pg"] = i
            st.rerun()

st.markdown("<hr class='v-div' style='margin-top:8px;'>", unsafe_allow_html=True)

# ── Progress steps indicator ─────────────────────────────────
_step_nodes = ""
for _i, (_p, _ic) in enumerate(zip(PAGES, NAV_ICONS)):
    _done   = _i < cur
    _active = _i == cur
    _scls   = "s-done" if _done else ("s-active" if _active else "")
    _lcls   = "s-done" if _done else ("s-active" if _active else "")
    _ccls   = "s-done-conn" if _done else ""
    _inner  = "✓" if _done else _ic
    _step_nodes += f'''
    <div class="step-node {_ccls}">
        <div class="step-circle {_scls}">{_inner}</div>
        <div class="step-lbl {_lcls}">{_p}</div>
    </div>'''
st.markdown(f'<div class="steps-track">{_step_nodes}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  PAGE: OVERVIEW
# ════════════════════════════════════════════════════════════════
if page == "Overview":
    st.markdown("""
    <div class="hero f1">
        <div class="hero-hex"></div><div class="hero-ring"></div>
        <div style="position:relative;z-index:2;">
            <div class="hero-kicker">Milestone 2 · Fitbit Analytics Platform</div>
            <div class="hero-title">Biometric<br>Intelligence</div>
            <p class="hero-sub">Deep analysis of real Fitbit sensor data from 35 users across 31 days — from raw seconds to actionable clustering insights.</p>
            <div class="hero-pills">
                <div class="hero-pill"><span>⚡</span> 174K HR records</div>
                <div class="hero-pill"><span>🧬</span> TSFresh features</div>
                <div class="hero-pill"><span>📈</span> Prophet forecasts</div>
                <div class="hero-pill"><span>🔬</span> KMeans + DBSCAN</div>
                <div class="hero-pill"><span>🎯</span> PCA + t-SNE</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    kpis = [
        ("🧑‍🤝‍🧑","TOTAL USERS",    f"{master['Id'].nunique()}",       "users",     "kpi-amber"),
        ("📅",   "DAYS TRACKED",   "31",                               "Mar–Apr 16","kpi-coral"),
        ("💓",   "HR RECORDS",     f"{hr.shape[0]:,}",                 "1-min pts", "kpi-teal"),
        ("😴",   "SLEEP ENTRIES",  f"{sleep.shape[0]:,}",              "rows",      "kpi-lav"),
        ("👟",   "AVG DAILY STEPS",f"{int(master['TotalSteps'].mean()):,}","steps/day","kpi-gold"),
    ]
    kpi_html = '<div class="kpi-orbit">'
    for ic,lbl,num,unit,cls in kpis:
        kpi_html += f'<div class="kpi-card {cls} f2"><div class="pulse-ring"></div><span class="kpi-icon">{ic}</span><div class="kpi-label">{lbl}</div><div class="kpi-num">{num}</div><div class="kpi-unit">{unit}</div><div class="kpi-bar"></div></div>'
    kpi_html += "</div>"
    st.markdown(kpi_html, unsafe_allow_html=True)

    st.markdown("<hr class='v-div'>", unsafe_allow_html=True)
    st.markdown("""<div class="mod-header f3"><div class="mod-header-line"></div>
        <span class="mod-icon">📊</span>
        <div><span class="mod-code">SECTION 01 · OVERVIEW</span>
        <div class="mod-title">Activity & Health Distribution</div>
        <div class="mod-desc">Statistical distribution of steps, calories, sleep and activity intensity across all 35 users</div></div>
    </div>""", unsafe_allow_html=True)

    r1a,r1b,r1c = st.columns(3)
    with r1a:
        st.markdown('<div class="glass-panel f3"><div class="panel-label">Daily Steps Distribution</div>', unsafe_allow_html=True)
        fig,ax = plt.subplots(figsize=(5,3.2))
        data = master["TotalSteps"].dropna()
        ax.hist(data, bins=28, color=AMBER, edgecolor=VOID, linewidth=0.3, alpha=0.85)
        ax.axvline(data.mean(), color=CORAL, linewidth=1.5, linestyle="--", label=f"Mean: {data.mean():.0f}")
        ax.legend(fontsize=7, facecolor=LAYER, edgecolor=EDGE, labelcolor=TEXT)
        ax.set_title("Steps / Day"); ax.set_xlabel("Steps"); ax.set_ylabel("Count")
        mpl_fig(fig,ax); st.pyplot(fig); plt.close(fig)
        st.markdown('</div>', unsafe_allow_html=True)

    with r1b:
        st.markdown('<div class="glass-panel f4"><div class="panel-label">Activity Intensity Breakdown</div>', unsafe_allow_html=True)
        fig2,ax2 = plt.subplots(figsize=(5,3.2))
        cats = ["Very Active","Fairly Active","Lightly Active","Sedentary"]
        means = [master["VeryActiveMinutes"].mean(), master["FairlyActiveMinutes"].mean(),
                 master["LightlyActiveMinutes"].mean(), master["SedentaryMinutes"].mean()]
        wedges,texts,autotexts = ax2.pie(means, labels=cats, autopct="%1.0f%%",
            colors=[AMBER,CORAL,TEAL,MUTED], startangle=140,
            wedgeprops=dict(edgecolor=VOID,linewidth=2), pctdistance=0.78)
        for t in texts: t.set_color(MUTED); t.set_fontsize(8)
        for at in autotexts: at.set_color(TEXT); at.set_fontsize(8); at.set_fontweight("bold")
        ax2.set_facecolor(CARD); fig2.patch.set_facecolor(LAYER)
        ax2.set_title("Activity Split", color=AMBER, fontsize=11, fontweight="bold")
        fig2.tight_layout(); st.pyplot(fig2); plt.close(fig2)
        st.markdown('</div>', unsafe_allow_html=True)

    with r1c:
        st.markdown('<div class="glass-panel f5"><div class="panel-label">Calories vs Steps</div>', unsafe_allow_html=True)
        fig3,ax3 = plt.subplots(figsize=(5,3.2))
        sc = ax3.scatter(master["TotalSteps"], master["Calories"],
            c=master["VeryActiveMinutes"], cmap="YlOrRd", s=12, alpha=0.5, linewidths=0)
        cbar = fig3.colorbar(sc, ax=ax3, shrink=0.8)
        cbar.ax.tick_params(colors=MUTED, labelsize=7)
        cbar.set_label("V.Active Min", color=MUTED, fontsize=8)
        ax3.set_title("Calories vs Steps"); ax3.set_xlabel("Steps"); ax3.set_ylabel("Calories")
        mpl_fig(fig3,ax3); st.pyplot(fig3); plt.close(fig3)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr class='v-div'>", unsafe_allow_html=True)
    st.markdown("""<div class="mod-header f1"><div class="mod-header-line"></div>
        <span class="mod-icon">💓</span>
        <div><span class="mod-code">HEART RATE SENSOR</span>
        <div class="mod-title">1-Minute Resolution · Sample User</div>
        <div class="mod-desc">Resampled from seconds · 13 users with HR sensor data</div></div>
    </div>""", unsafe_allow_html=True)

    r2a,r2b = st.columns([3,1])
    with r2a:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        sid  = hr["Id"].unique()[0]
        shr  = (hr[hr["Id"]==sid].sort_values("Time").set_index("Time")
                  .resample("1h")["HeartRate"].mean().dropna())
        s7   = shr.head(7*24)
        fig4,ax4 = plt.subplots(figsize=(11,3))
        ax4.fill_between(s7.index, s7.values, alpha=0.1, color=CORAL)
        ax4.plot(s7.index, s7.values, color=CORAL, linewidth=1.2, alpha=0.7)
        ma = s7.rolling(6,center=True).mean()
        ax4.plot(s7.index, ma, color=GOLD, linewidth=2.2, linestyle="--", label="6-hr rolling avg")
        ax4.axhline(s7.mean(), color=TEAL, linewidth=1, linestyle=":", alpha=0.7, label=f"Mean: {s7.mean():.1f}")
        ax4.legend(fontsize=8, facecolor=LAYER, edgecolor=EDGE, labelcolor=TEXT)
        ax4.set_title(f"Heart Rate — User …{str(sid)[-5:]}")
        mpl_fig(fig4,ax4); plt.xticks(rotation=25,ha="right")
        st.pyplot(fig4); plt.close(fig4)
        st.markdown('</div>', unsafe_allow_html=True)

    with r2b:
        hr_d = hr["HeartRate"].describe()
        for lbl,val,cls in [("Mean BPM",f"{hr_d['mean']:.1f}","kpi-amber"),
                             ("Peak BPM",f"{hr_d['max']:.0f}","kpi-coral"),
                             ("Min BPM", f"{hr_d['min']:.0f}","kpi-teal")]:
            st.markdown(f'<div class="kpi-card {cls}" style="margin-bottom:14px;padding:18px 16px;"><div class="kpi-label">{lbl}</div><div class="kpi-num" style="font-size:28px;">{val}</div><div class="kpi-bar"></div></div>', unsafe_allow_html=True)

    st.markdown("<hr class='v-div'>", unsafe_allow_html=True)
    st.markdown("""<div class="mod-header"><div class="mod-header-line"></div>
        <span class="mod-icon">🗄️</span>
        <div><span class="mod-code">DATA REGISTRY</span><div class="mod-title">Source File Summary</div></div>
    </div>""", unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        shapes = pd.DataFrame({"File":["dailyActivity","hourlySteps","minuteSleep","heartrate_1min"],
            "Rows":[daily.shape[0],hourly_s.shape[0],sleep.shape[0],hr.shape[0]],
            "Cols":[daily.shape[1],hourly_s.shape[1],sleep.shape[1],hr.shape[1]],
            "Nulls":[daily.isnull().sum().sum(),hourly_s.isnull().sum().sum(),
                     sleep.isnull().sum().sum(),hr.isnull().sum().sum()]})
        st.dataframe(shapes, use_container_width=True, hide_index=True)
    with c2:
        st.dataframe(master[["TotalSteps","Calories","AvgHR","TotalSleepMinutes","VeryActiveMinutes"]].describe().round(2), use_container_width=True)

# ════════════════════════════════════════════════════════════════
#  PAGE: TSFRESH
# ════════════════════════════════════════════════════════════════
elif page == "TSFresh":
    st.markdown("""<div class="mod-header f1"><div class="mod-header-line"></div>
        <span class="mod-icon">⚗️</span>
        <div><span class="mod-code">SECTION 02 · FEATURE ENGINEERING</span>
        <div class="mod-title">TSFresh Extraction</div>
        <div class="mod-desc">Automated statistical feature engineering from 127K minute-level heart rate records · MinimalFCParameters · n_jobs=1</div></div>
    </div>""", unsafe_allow_html=True)

    prog = st.progress(0, text="Extracting features…")
    try:
        prog.progress(40, text="Running TSFresh…")
        features = get_tsfresh(hr)
        prog.progress(100, text="Done!"); prog.empty(); ok = True
    except Exception as e:
        prog.empty(); st.error(f"TSFresh error: {e}"); ok = False

    if ok:
        from sklearn.preprocessing import MinMaxScaler
        ta,tb,tc = st.columns(3)
        for col,lbl,val,cls in [(ta,"USERS PROCESSED",str(features.shape[0]),"kpi-amber"),
                                 (tb,"FEATURES EXTRACTED",str(features.shape[1]),"kpi-teal"),
                                 (tc,"HR SOURCE ROWS",f"{hr.shape[0]:,}","kpi-lav")]:
            with col:
                st.markdown(f'<div class="kpi-card {cls} f2" style="text-align:center;"><div class="kpi-label">{lbl}</div><div class="kpi-num">{val}</div><div class="kpi-bar"></div></div>', unsafe_allow_html=True)

        st.markdown("<hr class='v-div'>", unsafe_allow_html=True)

        fn = pd.DataFrame(MinMaxScaler().fit_transform(features), index=features.index, columns=features.columns)
        st.markdown('<div class="glass-panel f3"><div class="panel-label">Normalised Feature Matrix Heatmap  (0–1 scale)</div>', unsafe_allow_html=True)
        fig_h,ax_h = plt.subplots(figsize=(14, max(4, features.shape[0]*0.65)))
        cmap = sns.diverging_palette(30,250,s=90,l=30,n=256,as_cmap=True)
        sns.heatmap(fn, ax=ax_h, cmap=cmap, annot=True, fmt=".2f",
                    linewidths=0.3, linecolor=VOID, cbar_kws={"shrink":0.55,"pad":0.02})
        ax_h.set_facecolor(CARD); fig_h.patch.set_facecolor(LAYER)
        ax_h.set_title("TSFresh Feature Matrix — Fitbit Heart Rate", color=AMBER, fontsize=12, fontweight="bold")
        ax_h.tick_params(colors=MUTED, labelsize=8)
        ax_h.set_xlabel("Feature", color=MUTED); ax_h.set_ylabel("User ID", color=MUTED)
        plt.xticks(rotation=28, ha="right"); plt.tight_layout()
        st.pyplot(fig_h)
        buf_h = io.BytesIO(); fig_h.savefig(buf_h,format="png",dpi=150,bbox_inches="tight",facecolor=LAYER)
        st.download_button("⬇  Download Heatmap", buf_h.getvalue(), "tsfresh_heatmap.png","image/png")
        plt.close(fig_h)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr class='v-div'>", unsafe_allow_html=True)
        cr1,cr2 = st.columns(2)
        with cr1:
            st.markdown('<div class="glass-panel f4"><div class="panel-label">Mean Value Per Feature (normalised)</div>', unsafe_allow_html=True)
            fig_b,ax_b = plt.subplots(figsize=(6,3.5))
            means = fn.mean(); short = [c.replace("value__","") for c in means.index]
            ax_b.bar(range(len(means)), means.values, color=[PAL[i%len(PAL)] for i in range(len(means))], edgecolor=VOID, linewidth=0, width=0.7)
            ax_b.set_xticks(range(len(means))); ax_b.set_xticklabels(short, rotation=30, ha="right", fontsize=7)
            ax_b.set_title("Feature Mean (norm)")
            mpl_fig(fig_b,ax_b); st.pyplot(fig_b); plt.close(fig_b)
            st.markdown("</div>", unsafe_allow_html=True)

        with cr2:
            st.markdown('<div class="glass-panel f5"><div class="panel-label">Feature Variance Across Users</div>', unsafe_allow_html=True)
            fig_v,ax_v = plt.subplots(figsize=(6,3.5))
            varis = fn.std()
            ax_v.barh(range(len(varis)), varis.values, color=[PAL[i%len(PAL)] for i in range(len(varis))], edgecolor=VOID, linewidth=0, height=0.65)
            ax_v.set_yticks(range(len(varis))); ax_v.set_yticklabels([c.replace("value__","") for c in varis.index], fontsize=7)
            ax_v.set_title("Feature Std Dev"); ax_v.set_xlabel("Std Dev")
            mpl_fig(fig_v,ax_v); st.pyplot(fig_v); plt.close(fig_v)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr class='v-div'>", unsafe_allow_html=True)
        feat_lines = "".join([f'<span class="ok">[{i+1:02d}]</span>  <span class="hi">{c.replace("value__","")}</span><br>' for i,c in enumerate(features.columns)])
        st.markdown(f'<div class="term f3"><span class="hi">$ tsfresh.extract_features(MinimalFCParameters, n_jobs=1)</span><br><span class="ok">completed  {features.shape[0]} users · {features.shape[1]} features</span><br><br>{feat_lines}</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-label" style="margin-top:16px;">RAW FEATURE TABLE</div>', unsafe_allow_html=True)
        st.dataframe(features.round(4), use_container_width=True)

# ════════════════════════════════════════════════════════════════
#  PAGE: PROPHET
# ════════════════════════════════════════════════════════════════
elif page == "Prophet":
    st.markdown("""<div class="mod-header f1"><div class="mod-header-line"></div>
        <span class="mod-icon">🔮</span>
        <div><span class="mod-code">SECTION 03 · FORECASTING</span>
        <div class="mod-title">Prophet Trend Forecast</div>
        <div class="mod-desc">30-day ahead forecasting with 80% confidence intervals · Heart Rate · Steps · Sleep</div></div>
    </div>""", unsafe_allow_html=True)

    if "prophet_metric" not in st.session_state:
        st.session_state["prophet_metric"] = "Heart Rate"

    metrics_map = {"Heart Rate":(CORAL,"bpm","💓"), "Total Steps":(AMBER,"steps","👟"), "Sleep Min":(LAVENDER,"minutes","😴")}
    pm_cols = st.columns(3)
    for col,(label,(color,unit,icon)) in zip(pm_cols, metrics_map.items()):
        with col:
            if st.button(f"{icon}  {label}", key=f"pm_{label}", use_container_width=True):
                st.session_state["prophet_metric"] = label; st.rerun()

    sel_m = st.session_state["prophet_metric"]
    color,unit,icon = metrics_map[sel_m]
    st.markdown("<hr class='v-div' style='margin:16px 0;'>", unsafe_allow_html=True)

    with st.spinner(f"Fitting Prophet on {sel_m}…"):
        try:
            if sel_m=="Heart Rate":
                actual,forecast = get_prophet_hr(hr)
            elif sel_m=="Total Steps":
                actual,forecast = get_prophet_metric(master,"TotalSteps")
            else:
                actual,forecast = get_prophet_metric(master,"TotalSleepMinutes")
            fc_ok = True
        except Exception as e:
            st.error(f"Prophet error: {e}"); fc_ok = False

    if fc_ok:
        split = actual["ds"].max()
        fut   = forecast[forecast["ds"]>split]
        p1,p2,p3,p4 = st.columns(4)
        for col,lbl,val,cls in [(p1,"DATA POINTS",str(actual.shape[0]),"kpi-amber"),
                                 (p2,"FORECAST DAYS","30","kpi-coral"),
                                 (p3,"ACTUAL MEAN",f"{actual['y'].mean():.1f}","kpi-teal"),
                                 (p4,"FORECAST END",f"{fut['yhat'].iloc[-1]:.1f}","kpi-lav")]:
            with col:
                st.markdown(f'<div class="kpi-card {cls} f2" style="padding:18px 16px;text-align:center;"><div class="kpi-label">{lbl}</div><div class="kpi-num" style="font-size:26px;">{val}</div><div class="kpi-unit">{unit}</div><div class="kpi-bar"></div></div>', unsafe_allow_html=True)

        st.markdown("<hr class='v-div'>", unsafe_allow_html=True)
        st.markdown('<div class="glass-panel f3"><div class="panel-label">Forecast Chart · Actual vs Predicted · 80% Confidence Band</div>', unsafe_allow_html=True)
        fig_fc,ax_fc = plt.subplots(figsize=(13,4.5))
        ax_fc.fill_between(forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"], alpha=0.12, color=color, label="80% CI")
        ax_fc.plot(forecast["ds"], forecast["yhat"], color=TEXT, linewidth=2, alpha=0.7, label="Forecast")
        ax_fc.scatter(actual["ds"], actual["y"], color=color, s=20, zorder=5, alpha=0.9, label="Actual")
        ax_fc.axvline(split, color=GOLD, linewidth=1.5, linestyle="--", label="Forecast Start", alpha=0.8)
        ax_fc.axvspan(split, forecast["ds"].max(), alpha=0.04, color=color)
        ax_fc.legend(fontsize=8, facecolor=LAYER, edgecolor=EDGE, labelcolor=TEXT)
        ax_fc.set_title(f"{sel_m} — Prophet 30-Day Forecast"); ax_fc.set_ylabel(unit)
        mpl_fig(fig_fc,ax_fc); plt.xticks(rotation=30,ha="right")
        st.pyplot(fig_fc)
        buf_fc = io.BytesIO(); fig_fc.savefig(buf_fc,format="png",dpi=150,bbox_inches="tight",facecolor=LAYER)
        st.download_button("⬇  Download Chart", buf_fc.getvalue(), f"prophet_{sel_m.replace(' ','_')}.png","image/png")
        plt.close(fig_fc)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr class='v-div'>", unsafe_allow_html=True)
        dc1,dc2 = st.columns(2)
        with dc1:
            st.markdown('<div class="glass-panel f4"><div class="panel-label">Trend Component</div>', unsafe_allow_html=True)
            fig_tr,ax_tr = plt.subplots(figsize=(6,3))
            ax_tr.fill_between(forecast["ds"], forecast["trend"], alpha=0.15, color=AMBER)
            ax_tr.plot(forecast["ds"], forecast["trend"], color=AMBER, linewidth=2)
            ax_tr.set_title("Long-term Trend")
            mpl_fig(fig_tr,ax_tr); plt.xticks(rotation=25,ha="right")
            st.pyplot(fig_tr); plt.close(fig_tr)
            st.markdown("</div>", unsafe_allow_html=True)

        with dc2:
            st.markdown('<div class="glass-panel f5"><div class="panel-label">Weekly Seasonality</div>', unsafe_allow_html=True)
            fig_wk,ax_wk = plt.subplots(figsize=(6,3))
            if "weekly" in forecast.columns:
                wkly = forecast.groupby(forecast["ds"].dt.dayofweek)["weekly"].mean()
                days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
                ax_wk.bar(range(7), wkly.values, color=[AMBER if v>=0 else CORAL for v in wkly.values], edgecolor=VOID, linewidth=0, width=0.6)
                ax_wk.set_xticks(range(7)); ax_wk.set_xticklabels(days, fontsize=8)
                ax_wk.axhline(0, color=EDGE, linewidth=0.8)
                ax_wk.set_title("Day-of-Week Effect")
            else:
                ax_wk.text(0.5,0.5,"Not available",ha="center",va="center",color=MUTED,transform=ax_wk.transAxes)
                ax_wk.set_title("Weekly Seasonality")
            mpl_fig(fig_wk,ax_wk); st.pyplot(fig_wk); plt.close(fig_wk)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr class='v-div'>", unsafe_allow_html=True)
        st.markdown('<div class="panel-label">FORECAST TABLE · LAST 15 ROWS</div>', unsafe_allow_html=True)
        show_cols = ["ds","yhat","yhat_lower","yhat_upper","trend"]
        st.dataframe(forecast[show_cols].tail(15).round(2).reset_index(drop=True), use_container_width=True)

# ════════════════════════════════════════════════════════════════
#  PAGE: CLUSTERING
# ════════════════════════════════════════════════════════════════
elif page == "Clustering":
    st.markdown("""<div class="mod-header f1"><div class="mod-header-line"></div>
        <span class="mod-icon">🔬</span>
        <div><span class="mod-code">SECTION 04 · SEGMENTATION</span>
        <div class="mod-title">User Clustering & Dimensionality Reduction</div>
        <div class="mod-desc">KMeans · DBSCAN · PCA · t-SNE · 35 users segmented by 7 behavioural features</div></div>
    </div>""", unsafe_allow_html=True)

    with st.spinner("Running clustering pipeline…"):
        cf,cols,X,km,db,Xp,Xt,K,nc,nn,ve = get_clustering(master)

    CPAL = [AMBER,TEAL,CORAL,LAVENDER,GOLD]
    ca,cb,cc,cd,ce = st.columns(5)
    for col,lbl,val,cls in [(ca,"USERS",str(cf.shape[0]),"kpi-amber"),(cb,"FEATURES",str(len(cols)),"kpi-teal"),
                             (cc,"KMEANS K",str(K),"kpi-coral"),(cd,"DBSCAN CLUSTERS",str(nc),"kpi-lav"),
                             (ce,"NOISE",str(nn),"kpi-gold")]:
        with col:
            st.markdown(f'<div class="kpi-card {cls} f2" style="text-align:center;padding:18px 14px;"><div class="kpi-label">{lbl}</div><div class="kpi-num" style="font-size:28px;">{val}</div><div class="kpi-bar"></div></div>', unsafe_allow_html=True)

    # ── Insight summary badges ───────────────────────────────────
    _active_pct  = round(len([x for x in km if x == 0]) / len(km) * 100)
    _sedent_pct  = round(len([x for x in km if x == (K-1)]) / len(km) * 100)
    _noise_pct   = round(nn / cf.shape[0] * 100)
    st.markdown(f"""
    <div style="display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 20px;">
        <span class="insight-badge badge-up">↑ {cf.shape[0] - nn} clustered users</span>
        <span class="insight-badge badge-neutral">PC1+PC2 = {sum(ve):.1f}% variance</span>
        <span class="insight-badge badge-down">⚠ {nn} noise users ({_noise_pct}%)</span>
        <span class="insight-badge badge-neutral">K={K} optimal clusters</span>
        <span class="insight-badge badge-up">✓ {K} DBSCAN groups found</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='v-div'>", unsafe_allow_html=True)

    from sklearn.cluster import KMeans as _KM
    col_el,col_pca = st.columns([1,1.4])
    with col_el:
        st.markdown('<div class="glass-panel f3"><div class="panel-label">Elbow Curve — Optimal K</div>', unsafe_allow_html=True)
        inertias,kr = [],range(2,min(10,cf.shape[0]))
        for k in kr: inertias.append(_KM(n_clusters=k,random_state=42,n_init=10).fit(X).inertia_)
        fig_el,ax_el = plt.subplots(figsize=(5.5,3.5))
        ax_el.plot(list(kr),inertias,"o-",color=AMBER,linewidth=2.2,markersize=7,
                   markerfacecolor=LAYER,markeredgecolor=AMBER,markeredgewidth=2)
        ax_el.fill_between(list(kr),inertias,alpha=0.05,color=AMBER)
        ax_el.axvline(K,color=CORAL,linewidth=1.5,linestyle="--",label=f"Chosen K={K}")
        ax_el.legend(fontsize=8,facecolor=LAYER,edgecolor=EDGE,labelcolor=TEXT)
        ax_el.set_title("KMeans Elbow"); ax_el.set_xlabel("K"); ax_el.set_ylabel("Inertia")
        mpl_fig(fig_el,ax_el); st.pyplot(fig_el); plt.close(fig_el)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_pca:
        st.markdown('<div class="glass-panel f4"><div class="panel-label">KMeans · PCA 2D Projection</div>', unsafe_allow_html=True)
        fig_p,ax_p = plt.subplots(figsize=(7.5,4))
        for cid in sorted(set(km)):
            mask = km==cid
            ax_p.scatter(Xp[mask,0],Xp[mask,1],c=CPAL[cid%len(CPAL)],s=100,
                         alpha=0.9,edgecolors=VOID,linewidths=0.8,label=f"Cluster {cid}",zorder=3)
            pts = Xp[mask]
            if len(pts)>=3:
                try:
                    from scipy.spatial import ConvexHull
                    hull = ConvexHull(pts); hp = np.append(hull.vertices,hull.vertices[0])
                    ax_p.plot(pts[hp,0],pts[hp,1],color=CPAL[cid%len(CPAL)],linewidth=1,alpha=0.3,linestyle="--")
                except Exception: pass
            for i,uid in enumerate(np.array(cf.index)[mask]):
                ax_p.annotate(str(uid)[-4:],(Xp[mask][i,0],Xp[mask][i,1]),fontsize=5,color=MUTED,ha="center",fontfamily="monospace")
        ax_p.set_title(f"KMeans PCA (K={K})"); ax_p.set_xlabel(f"PC1 ({ve[0]:.1f}%)"); ax_p.set_ylabel(f"PC2 ({ve[1]:.1f}%)")
        ax_p.legend(fontsize=8,facecolor=LAYER,edgecolor=EDGE,labelcolor=TEXT)
        mpl_fig(fig_p,ax_p); st.pyplot(fig_p); plt.close(fig_p)
        st.markdown("</div>", unsafe_allow_html=True)

    col_ts1,col_ts2 = st.columns(2)
    for col_ts,labels,title,algo in [(col_ts1,km,f"KMeans t-SNE (K={K})","KMeans"),(col_ts2,db,"DBSCAN t-SNE (eps=1.8)","DBSCAN")]:
        with col_ts:
            st.markdown(f'<div class="glass-panel f4"><div class="panel-label">{algo} · t-SNE Projection</div>', unsafe_allow_html=True)
            fig_t,ax_t = plt.subplots(figsize=(6.5,4.5))
            for lbl in sorted(set(labels)):
                mask = labels==lbl
                if lbl==-1:
                    ax_t.scatter(Xt[mask,0],Xt[mask,1],c=MUTED,marker="x",s=80,linewidths=1.5,label="Noise",zorder=5)
                else:
                    ax_t.scatter(Xt[mask,0],Xt[mask,1],c=CPAL[lbl%len(CPAL)],s=90,alpha=0.9,edgecolors=VOID,linewidths=0.7,label=f"Cluster {lbl}",zorder=3)
            ax_t.set_title(title); ax_t.legend(fontsize=8,facecolor=LAYER,edgecolor=EDGE,labelcolor=TEXT)
            mpl_fig(fig_t,ax_t); st.pyplot(fig_t); plt.close(fig_t)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr class='v-div'>", unsafe_allow_html=True)
    st.markdown("""<div class="mod-header f1"><div class="mod-header-line"></div>
        <span class="mod-icon">📊</span>
        <div><span class="mod-code">CLUSTER PROFILES</span>
        <div class="mod-title">Behavioural Segment Analysis</div>
        <div class="mod-desc">Average feature values per cluster — sedentary, moderate and highly active segments</div></div>
    </div>""", unsafe_allow_html=True)

    profile  = cf.groupby("KMeans_Cluster")[cols].mean().round(2)
    plot_c   = ["TotalSteps","Calories","VeryActiveMinutes","SedentaryMinutes","TotalSleepMinutes"]
    col_pr,col_int = st.columns([2,1])

    with col_pr:
        st.markdown('<div class="glass-panel f3"><div class="panel-label">Grouped Bar — Key Features by Cluster</div>', unsafe_allow_html=True)
        fig_pr,ax_pr = plt.subplots(figsize=(9,4))
        x = np.arange(K); w = 0.14
        for j,feat in enumerate(plot_c):
            vals = [profile.loc[i,feat] if i in profile.index else 0 for i in range(K)]
            ax_pr.bar(x+j*w, vals, w, label=feat, color=PAL[j%len(PAL)], edgecolor=VOID, linewidth=0, alpha=0.9)
        ax_pr.set_xticks(x+w*2); ax_pr.set_xticklabels([f"Cluster {i}" for i in range(K)])
        ax_pr.legend(fontsize=7,facecolor=LAYER,edgecolor=EDGE,labelcolor=TEXT,loc="upper right")
        ax_pr.set_title("Cluster Feature Profiles")
        mpl_fig(fig_pr,ax_pr); st.pyplot(fig_pr)
        buf_pr = io.BytesIO(); fig_pr.savefig(buf_pr,format="png",dpi=150,bbox_inches="tight",facecolor=LAYER)
        st.download_button("⬇  Download Profile Chart", buf_pr.getvalue(),"cluster_profiles.png","image/png")
        plt.close(fig_pr)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_int:
        st.markdown('<div class="glass-panel f4"><div class="panel-label">Cluster Interpretation</div>', unsafe_allow_html=True)
        for i in range(K):
            if i in profile.index:
                steps = profile.loc[i,"TotalSteps"]; sed = profile.loc[i,"SedentaryMinutes"]; active = profile.loc[i,"VeryActiveMinutes"]
                if steps>10000: tag,cls = "🏃 HIGHLY ACTIVE","chip-a"
                elif steps>5000: tag,cls = "🚶 MODERATELY ACTIVE","chip-b"
                else: tag,cls = "🛋️ SEDENTARY","chip-c"
                st.markdown(f'<div style="margin-bottom:14px;padding:14px 16px;background:rgba(255,255,255,0.02);border:1px solid #2a2545;border-radius:12px;"><span class="chip {cls}">Cluster {i}</span><div style="font-size:11px;color:#9896bc;margin-top:8px;font-family:Fira Code,monospace;line-height:1.9;">Steps: <span style="color:#ede8ff;">{steps:,.0f}</span><br>Sedentary: <span style="color:#ede8ff;">{sed:.0f} min</span><br>V.Active: <span style="color:#ede8ff;">{active:.0f} min</span><br><strong style="color:#f5a623;">{tag}</strong></div></div>', unsafe_allow_html=True)
        if nn:
            st.markdown(f'<span class="chip chip-d">⚠️ {nn} noise users ({nn/cf.shape[0]*100:.0f}%)</span>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr class='v-div'>", unsafe_allow_html=True)
    with st.expander("📋  Full Cluster Profile Table", expanded=False):
        search_q = st.text_input("🔍  Filter columns", placeholder="e.g. Steps, Calories…", key="cluster_search")
        _show_cols = [c for c in profile.columns if not search_q or search_q.lower() in c.lower()]
        st.dataframe(profile[_show_cols].round(2), use_container_width=True)
        _csv = profile.round(2).to_csv().encode()
        st.download_button("⬇  Export cluster profiles CSV", _csv, "cluster_profiles.csv", "text/csv", key="dl_profile_csv")

    with st.expander("👤  Full User Feature Matrix", expanded=False):
        _disp_cf = cf[[c for c in cf.columns if c not in ["KMeans_Cluster","DBSCAN_Cluster"]]].round(3)
        st.dataframe(_disp_cf, use_container_width=True)
        st.download_button("⬇  Export user features CSV", _disp_cf.to_csv().encode(), "user_features.csv", "text/csv", key="dl_feat_csv")

    st.markdown("<hr class='v-div'>", unsafe_allow_html=True)
    dist = cf["KMeans_Cluster"].value_counts().sort_index().to_dict()
    st.markdown(f"""<div class="term f3">
        <span class="hi">╔══════════════════════════════════════════╗</span><br>
        <span class="hi">║  FITPULSE · MILESTONE 2 · COMPLETE      ║</span><br>
        <span class="hi">╚══════════════════════════════════════════╝</span><br><br>
        <span class="ok">✓</span>  <span class="hi">Dataset</span>   35 users · 31 days · <span class="val">March–April 2016</span><br>
        <span class="ok">✓</span>  <span class="hi">TSFresh</span>   10 features · <span class="val">127,404</span> HR records<br>
        <span class="ok">✓</span>  <span class="hi">Prophet</span>   HR / Steps / Sleep · 30-day · 80% CI<br>
        <span class="ok">✓</span>  <span class="hi">KMeans</span>    K=<span class="val">{K}</span> · {dict(dist)}<br>
        <span class="ok">✓</span>  <span class="hi">DBSCAN</span>    <span class="val">{nc}</span> clusters · <span class="warn">{nn}</span> noise ({nn/cf.shape[0]*100:.1f}%)<br>
        <span class="ok">✓</span>  <span class="hi">PCA</span>       PC1=<span class="val">{ve[0]:.1f}%</span> PC2=<span class="val">{ve[1]:.1f}%</span> total=<span class="val">{sum(ve):.1f}%</span><br><br>
        <span class="ok">STATUS: ALL SECTIONS PASSED ✓</span>
    </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  FOOTER
# ════════════════════════════════════════════════════════════════
st.markdown("""
<div style="margin-top:64px;padding:20px 0 12px;border-top:1px solid rgba(245,166,35,0.08);display:flex;align-items:center;justify-content:space-between;">
    <span style="font-family:'Fira Code',monospace;font-size:10px;color:#5a5680;">FitPulse · Milestone 2 · Streamlit</span>
    <span style="font-family:'Fira Code',monospace;font-size:10px;color:#5a5680;">35 users · 2016 Fitbit Dataset</span>
</div>""", unsafe_allow_html=True)