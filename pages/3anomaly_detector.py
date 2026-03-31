# ═══════════════════════════════════════════════════════════════════════════════
#  FITPULSE  ·  MILESTONE 3  ·  3anomaly_detector.py
#  Anomaly Detection Observatory  ·  Crimson / Rose / Dark Theme
#  Horizontal top-nav  ·  M2-inspired advanced CSS  ·  Full Plotly charts
#  Run:  streamlit run Home.py  (place in pages/ folder)
# ═══════════════════════════════════════════════════════════════════════════════

import os, warnings
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
warnings.filterwarnings("ignore")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FitPulse · Anomaly Detector",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Pages / Sections (top-nav) ────────────────────────────────────────────────
PAGES     = ["Overview", "Heart Rate", "Sleep", "Steps", "DBSCAN", "Accuracy"]
NAV_ICONS = ["◎", "❤️", "💤", "🚶", "🔍", "🎯"]
NAV_DESCS = ["Data loading & KPIs",
             "HR anomaly detection",
             "Sleep anomaly detection",
             "Step count anomaly detection",
             "Structural outlier detection",
             "Simulated 90%+ accuracy validation"]

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [
    ("files_loaded",     False),
    ("anomaly_done",     False),
    ("simulation_done",  False),
    ("pg3",              0),
    ("daily",    None), ("hourly_s", None), ("hourly_i", None),
    ("sleep",    None), ("hr",       None), ("hr_minute", None),
    ("master",   None),
    ("anom_hr",  None), ("anom_steps", None), ("anom_sleep", None),
    ("sim_results", None),
]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Colour palette (crimson / rose / deep dark) ───────────────────────────────
VOID      = "#07060e"
DEEP      = "#0e0a14"
LAYER     = "#140d1e"
CARD      = "#1c1228"
EDGE      = "#2e1e3a"
CRIMSON   = "#fc8181"
ROSE      = "#f687b3"
GOLD      = "#fbbf24"
TEAL      = "#34d399"
LAVENDER  = "#c084fc"
CYAN      = "#67e8f9"
TEXT      = "#f0e6ff"
MUTED     = "#a89cc4"
DIM       = "#5a4d70"

# Plotly theme
PLOT_BG   = "#0e0a14"
PAPER_BG  = "#07060e"
GRID_CLR  = "rgba(255,255,255,0.05)"
PAL       = [CRIMSON, ROSE, TEAL, LAVENDER, GOLD, CYAN, "#fb923c", "#a5b4fc"]

def apply_theme(fig, title="", height=460):
    fig.update_layout(
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=TEXT, family="Clash Display, Inter, sans-serif"),
        height=height,
        xaxis=dict(gridcolor=GRID_CLR, showgrid=True, zeroline=False,
                   linecolor=EDGE, tickfont=dict(color=MUTED, size=10)),
        yaxis=dict(gridcolor=GRID_CLR, showgrid=True, zeroline=False,
                   linecolor=EDGE, tickfont=dict(color=MUTED, size=10)),
        legend=dict(bgcolor="rgba(20,13,30,0.85)", bordercolor=EDGE,
                    borderwidth=1, font=dict(color=TEXT, size=11)),
        margin=dict(l=55, r=30, t=60, b=50),
        hoverlabel=dict(bgcolor=CARD, bordercolor=EDGE, font=dict(color=TEXT)),
    )
    if title:
        fig.update_layout(title=dict(
            text=title,
            font=dict(color=TEXT, size=14, family="Clash Display, sans-serif")
        ))
    return fig

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] * { font-family: 'Inter', sans-serif !important; }
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"],
    div[data-testid="stSidebarNavItems"],
    div[data-testid="stSidebarNavSeparator"] { display: none !important; }
    /* Ensure sidebar scrolls instead of overlapping */
    section[data-testid="stSidebar"] { overflow-y: auto !important; }
    section[data-testid="stSidebar"] > div:first-child { padding-bottom: 16px !important; }
    div[data-testid="stSidebar"] [data-testid="stButton"] > button {
        background: rgba(252,129,129,0.08) !important;
        border: 1px solid rgba(252,129,129,0.2) !important;
        color: #fc8181 !important; border-radius: 10px !important;
        font-size: 12px !important; font-weight: 600 !important;
        width: 100% !important; padding: 9px 14px !important;
        transition: all 0.2s ease !important;
        font-family: 'Fira Code', monospace !important;
    }
    div[data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
        background: rgba(252,129,129,0.16) !important;
        border-color: #fc8181 !important;
        box-shadow: 0 0 16px rgba(252,129,129,0.2) !important;
    }
    </style>

    <div style="text-align:center;padding:24px 16px 16px;">
        <div style="width:52px;height:52px;border-radius:15px;
            background:linear-gradient(135deg,#1f0a14,#2e0d1e);
            border:1px solid rgba(252,129,129,0.4);
            display:flex;align-items:center;justify-content:center;
            margin:0 auto 12px;
            box-shadow:0 0 24px rgba(252,129,129,0.25),inset 0 1px 0 rgba(255,255,255,0.06);">
            <svg width="26" height="26" viewBox="0 0 32 32" fill="none">
                <polyline points="2,16 7,16 10,7 16,26 22,9 26,20 29,16 30,16"
                    stroke="url(#sg3)" stroke-width="2.4"
                    stroke-linecap="round" stroke-linejoin="round"/>
                <defs>
                    <linearGradient id="sg3" x1="0" y1="0" x2="32" y2="0">
                        <stop offset="0%" stop-color="#fc8181"/>
                        <stop offset="100%" stop-color="#f687b3"/>
                    </linearGradient>
                </defs>
            </svg>
        </div>
        <div style="font-size:15px;font-weight:800;color:#f0e6ff;letter-spacing:0.3px;">
            FitPulse
        </div>
        <div style="font-family:'Fira Code',monospace;font-size:9px;
            color:#4a2a3a;letter-spacing:2px;text-transform:uppercase;margin-top:3px;">
            Anomaly Detector
        </div>
    </div>
    <div style="height:1px;background:linear-gradient(90deg,transparent,
        rgba(252,129,129,0.18),transparent);margin:0 14px 16px;"></div>
    """, unsafe_allow_html=True)

    if st.button("🏠  Back to Home", key="m3_home_btn"):
        st.switch_page("Home.py")

    st.markdown("""
    <div style="margin-top:12px;">
    <div style="font-family:'Fira Code',monospace;font-size:8px;
        letter-spacing:3px;color:#2e1e2e;text-transform:uppercase;
        padding:0 16px 8px;">Pipeline Status</div>
    </div>
    """, unsafe_allow_html=True)

    steps_done = sum([st.session_state.files_loaded,
                      st.session_state.anomaly_done,
                      st.session_state.simulation_done])
    pct = int(steps_done / 3 * 100)

    st.markdown(f"""
    <div style="padding:0 16px;margin-bottom:12px;">
      <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
        <span style="font-family:'Fira Code',monospace;font-size:9px;color:#6a4a5a;">PROGRESS</span>
        <span style="font-family:'Fira Code',monospace;font-size:9px;color:#fc8181;">{pct}%</span>
      </div>
      <div style="background:rgba(255,255,255,0.04);border-radius:999px;height:5px;overflow:hidden;">
        <div style="width:{pct}%;height:100%;border-radius:999px;
          background:linear-gradient(90deg,#fc8181,#f687b3);
          box-shadow:0 0 8px rgba(252,129,129,0.4);transition:width 0.5s ease;"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    for done, icon, label in [
        (st.session_state.files_loaded,    "📂", "Data Loaded"),
        (st.session_state.anomaly_done,    "🚨", "Anomalies Detected"),
        (st.session_state.simulation_done, "🎯", "Accuracy Validated"),
    ]:
        col = "#34d399" if done else "#4a3a5a"
        dot = "●" if done else "○"
        st.markdown(
            f'<div style="font-size:0.8rem;padding:5px 16px;color:{col};'
            f'font-family:Fira Code,monospace;">{dot} {icon} {label}</div>',
            unsafe_allow_html=True
        )

    st.markdown("""
    <div style="height:1px;background:linear-gradient(90deg,transparent,
        rgba(252,129,129,0.12),transparent);margin:14px 16px;"></div>
    <div style="padding:0 16px 8px;">
    <div style="font-family:'Fira Code',monospace;font-size:8px;
        letter-spacing:2px;color:#2e1e2e;text-transform:uppercase;
        margin-bottom:10px;">Thresholds</div>
    """, unsafe_allow_html=True)

    hr_high = st.number_input("HR High (bpm)",    value=100, min_value=80,  max_value=180)
    hr_low  = st.number_input("HR Low (bpm)",     value=50,  min_value=30,  max_value=70)
    st_low  = st.number_input("Steps Low",        value=500, min_value=0,   max_value=2000)
    sl_low  = st.number_input("Sleep Low (min)",  value=60,  min_value=0,   max_value=120)
    sl_high = st.number_input("Sleep High (min)", value=600, min_value=300, max_value=900)
    sigma   = st.slider("Residual σ threshold",   1.0, 4.0, 2.0, 0.5, key="sigma_slider")

    st.markdown("</div>", unsafe_allow_html=True)

    # Section page indicator
    st.markdown("""
    <div style="height:1px;background:linear-gradient(90deg,transparent,
        rgba(252,129,129,0.12),transparent);margin:4px 16px 12px;"></div>
    <div style="font-family:'Fira Code',monospace;font-size:8px;
        letter-spacing:3px;color:#2e1e2e;text-transform:uppercase;
        padding:0 16px 8px;">Sections</div>
    """, unsafe_allow_html=True)

    _cur = PAGES[st.session_state.pg3]
    for _p, _ic in zip(PAGES, NAV_ICONS):
        _active = _p == _cur
        _col  = "#fc8181" if _active else "#4a3a5a"
        _bg   = "rgba(252,129,129,0.08)" if _active else "transparent"
        _bdr  = "rgba(252,129,129,0.22)" if _active else "rgba(255,255,255,0.04)"
        _fw   = "700" if _active else "400"
        _dot  = ("<span style='margin-left:auto;width:5px;height:5px;border-radius:50%;"
                 "background:#fc8181;box-shadow:0 0 6px #fc8181;display:inline-block;'></span>"
                 if _active else "")
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:10px;"
            f"padding:7px 16px;margin-bottom:3px;border-radius:8px;"
            f"background:{_bg};border:1px solid {_bdr};'>"
            f"<span style='font-size:10px;color:{_col};'>{_ic}</span>"
            f"<span style='font-size:11px;color:{_col};font-weight:{_fw};'>{_p}</span>"
            f"{_dot}</div>",
            unsafe_allow_html=True
        )

    st.markdown("""
    <div style="margin-top:20px;padding:0 16px 20px;">
        <div style="background:rgba(252,129,129,0.05);
            border:1px solid rgba(252,129,129,0.1);
            border-radius:10px;padding:10px 12px;text-align:center;">
            <div style="font-family:'Fira Code',monospace;
                font-size:8px;color:#2e1e2e;letter-spacing:1px;line-height:1.9;">
                35 Users · 31 Days<br>2016 Fitbit Dataset
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Clash+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&family=Fira+Code:wght@300;400;500;600&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}
html, body, .stApp {{ font-family: 'Inter', sans-serif !important; }}

.stApp {{
    background-color: {VOID};
    background-image:
        radial-gradient(ellipse 120% 60% at 50% -5%,
            rgba(252,129,129,0.12) 0%, transparent 55%),
        radial-gradient(ellipse 80% 80% at -10% 50%,
            rgba(246,135,179,0.07) 0%, transparent 55%),
        radial-gradient(ellipse 60% 50% at 110% 80%,
            rgba(52,211,153,0.05) 0%, transparent 55%),
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='104'%3E%3Cpath d='M30 0 L60 17.3 L60 51.9 L30 69.3 L0 51.9 L0 17.3 Z' fill='none' stroke='rgba(252,129,129,0.04)' stroke-width='0.5'/%3E%3Cpath d='M30 34.6 L60 51.9 L60 86.6 L30 104 L0 86.6 L0 51.9 Z' fill='none' stroke='rgba(252,129,129,0.04)' stroke-width='0.5'/%3E%3C/svg%3E"),
        linear-gradient(160deg, #0e0814 0%, {VOID} 50%, #100a18 100%);
    background-size: 100% 100%, 100% 100%, 100% 100%, 120px 104px, 100% 100%;
    color: {TEXT}; min-height: 100vh;
}}

.stApp::before {{
    content: '';
    position: fixed; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg,
        transparent 0%, rgba(252,129,129,0) 10%,
        rgba(252,129,129,0.9) 35%, rgba(246,135,179,1) 50%,
        rgba(252,129,129,0.9) 65%, rgba(52,211,153,0) 90%, transparent 100%);
    z-index: 99999; pointer-events: none;
    box-shadow: 0 0 30px rgba(252,129,129,0.4), 0 0 80px rgba(252,129,129,0.15);
}}

#MainMenu, footer, header {{ visibility: hidden !important; }}
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
[data-testid="stSidebarNavSeparator"] {{ display: none !important; }}

section[data-testid="stSidebar"] {{
    background: #07060f !important;
    background-image: radial-gradient(ellipse 140% 30% at 50% 0%,
        rgba(252,129,129,0.12) 0%, transparent 55%),
        linear-gradient(180deg, #0a0812 0%, {VOID} 100%) !important;
    border-right: 1px solid rgba(252,129,129,0.1) !important;
    box-shadow: 4px 0 40px rgba(0,0,0,0.6) !important;
}}

.block-container {{ padding: 0 2rem 4rem !important; max-width: 1400px !important; }}
p, div, span {{ color: {TEXT}; }}

/* ── TOP NAV ─────────────────────────── */
.topnav {{
    position: sticky; top: 0; z-index: 9000;
    display: flex; align-items: center;
    padding: 0 32px; height: 64px;
    background: rgba(7,6,14,0.90);
    backdrop-filter: blur(24px) saturate(180%);
    border-bottom: 1px solid rgba(252,129,129,0.12);
    box-shadow: 0 4px 32px rgba(0,0,0,0.6);
    margin: 0 -2rem 0 -2rem;
    width: calc(100% + 4rem);
}}
.topnav-brand {{
    display: flex; align-items: center; gap: 12px;
    flex-shrink: 0; margin-right: 40px;
}}
.topnav-logo {{
    width: 36px; height: 36px; border-radius: 10px;
    background: linear-gradient(135deg, #1f0a14, #2e0d1e);
    border: 1px solid rgba(252,129,129,0.3);
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 0 16px rgba(252,129,129,0.2);
}}
.topnav-name {{ font-family:'Clash Display',sans-serif; font-size:17px; font-weight:700; color:{TEXT}; }}
.topnav-badge {{
    font-family:'Fira Code',monospace; font-size:9px; color:{CRIMSON};
    background:rgba(252,129,129,0.1); border:1px solid rgba(252,129,129,0.25);
    border-radius:4px; padding:1px 6px; letter-spacing:1px;
}}
.topnav-links {{ display:flex; align-items:center; gap:4px; flex:1; }}
.topnav-link {{
    display:flex; align-items:center; gap:7px;
    padding:7px 14px; border-radius:8px;
    font-size:12px; font-weight:500; color:{MUTED};
    border:1px solid transparent; transition:all 0.2s ease; white-space:nowrap;
}}
.topnav-link.active {{
    color:{CRIMSON}; font-weight:600;
    background:rgba(252,129,129,0.08);
    border-color:rgba(252,129,129,0.2);
    box-shadow:0 0 20px rgba(252,129,129,0.08);
}}
.topnav-link:hover {{ color:#c8c0e4; background:rgba(255,255,255,0.04); }}
.nav-dot {{ width:5px; height:5px; border-radius:50%; background:{CRIMSON}; box-shadow:0 0 6px {CRIMSON}; display:none; }}
.topnav-link.active .nav-dot {{ display:block; }}
.topnav-right {{ display:flex; align-items:center; gap:10px; margin-left:auto; }}
.topnav-stat {{
    font-family:'Fira Code',monospace; font-size:10px; color:#7a6898;
    padding:5px 12px; background:rgba(255,255,255,0.02);
    border:1px solid rgba(255,255,255,0.04); border-radius:6px;
}}
.topnav-live {{
    display:flex; align-items:center; gap:6px;
    font-family:'Fira Code',monospace; font-size:10px; color:{CRIMSON};
    padding:5px 10px; background:rgba(252,129,129,0.06);
    border:1px solid rgba(252,129,129,0.15); border-radius:6px;
}}
.live-dot {{ width:6px; height:6px; border-radius:50%; background:{CRIMSON};
    animation:livePulse 1.8s ease-in-out infinite; }}
@keyframes livePulse {{ 0%,100%{{opacity:1;box-shadow:0 0 4px {CRIMSON};}} 50%{{opacity:0.4;box-shadow:0 0 10px {CRIMSON};}} }}

/* ── HERO ────────────────────────────── */
.m3-hero {{
    position:relative; overflow:hidden;
    border-radius:24px; padding:52px 52px 48px;
    margin:28px 0 32px;
    background:
        radial-gradient(ellipse 80% 100% at 90% 50%, rgba(252,129,129,0.1) 0%, transparent 60%),
        radial-gradient(ellipse 50% 80% at 10% 50%, rgba(246,135,179,0.07) 0%, transparent 60%),
        linear-gradient(135deg, #1a0d22 0%, #130b1c 60%, #170d20 100%);
    border:1px solid rgba(252,129,129,0.15);
    box-shadow:0 0 0 1px rgba(255,255,255,0.03) inset, 0 32px 80px rgba(0,0,0,0.6);
}}
.hero-ring {{
    position:absolute; right:-80px; top:-80px;
    width:400px; height:400px; border-radius:50%;
    border:1px solid rgba(252,129,129,0.08);
    pointer-events:none; animation:slowSpin 40s linear infinite;
}}
.hero-ring::before {{ content:''; position:absolute; inset:30px; border-radius:50%; border:1px solid rgba(246,135,179,0.06); }}
.hero-ring::after  {{ content:''; position:absolute; inset:60px; border-radius:50%; border:1px solid rgba(52,211,153,0.05); }}
@keyframes slowSpin {{ from{{transform:rotate(0deg);}} to{{transform:rotate(360deg);}} }}
.hero-kicker {{
    font-family:'Fira Code',monospace; font-size:10px; font-weight:500;
    color:{CRIMSON}; letter-spacing:3px; text-transform:uppercase;
    display:inline-flex; align-items:center; gap:8px; margin-bottom:16px;
}}
.hero-kicker::before {{ content:''; display:inline-block; width:24px; height:1px; background:{CRIMSON}; box-shadow:0 0 8px {CRIMSON}; }}
.hero-title {{
    font-family:'Clash Display',sans-serif !important;
    font-size:56px !important; font-weight:700 !important;
    line-height:1.05 !important; letter-spacing:-1px;
    background:linear-gradient(135deg, {TEXT} 0%, {CRIMSON} 40%, {ROSE} 70%, {GOLD} 100%);
    background-size:200% auto;
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    animation:gradShift 6s linear infinite; margin-bottom:16px !important;
}}
@keyframes gradShift {{ 0%{{background-position:0% center;}} 100%{{background-position:200% center;}} }}
.hero-sub {{ font-size:15px; color:{MUTED}; line-height:1.75; max-width:520px; margin-bottom:32px; }}
.hero-pills {{ display:flex; flex-wrap:wrap; gap:8px; }}
.hero-pill {{
    display:inline-flex; align-items:center; gap:6px;
    padding:7px 16px; border-radius:999px; font-size:12px; font-weight:500;
    background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.07); color:{MUTED};
}}

/* ── KPI ORBIT ───────────────────────── */
.kpi-orbit {{ display:grid; grid-template-columns:repeat(5,1fr); gap:14px; margin-bottom:28px; }}
.kpi-card {{
    position:relative; overflow:hidden;
    background:linear-gradient(135deg,{LAYER},{DEEP});
    border-radius:18px; padding:22px 18px;
    border:1px solid {EDGE};
    transition:transform 0.3s cubic-bezier(0.34,1.56,0.64,1), border-color 0.3s, box-shadow 0.3s;
}}
.kpi-card:hover {{ transform:translateY(-6px) scale(1.02); box-shadow:0 20px 60px rgba(0,0,0,0.5); }}
.kpi-card::before {{
    content:''; position:absolute; top:0; left:0; right:0; height:1px;
    background:linear-gradient(90deg,transparent,var(--accent),transparent); opacity:0.6;
}}
.kpi-card::after {{
    content:''; position:absolute; bottom:-30px; right:-30px;
    width:80px; height:80px; border-radius:50%;
    background:radial-gradient(circle,var(--accent-glow) 0%,transparent 70%);
}}
.kpi-red  {{ --accent:{CRIMSON}; --accent-glow:rgba(252,129,129,0.12); border-left:2px solid {CRIMSON}; }}
.kpi-rose {{ --accent:{ROSE}; --accent-glow:rgba(246,135,179,0.12); border-left:2px solid {ROSE}; }}
.kpi-teal {{ --accent:{TEAL}; --accent-glow:rgba(52,211,153,0.12);  border-left:2px solid {TEAL}; }}
.kpi-lav  {{ --accent:{LAVENDER}; --accent-glow:rgba(192,132,252,0.12);border-left:2px solid {LAVENDER}; }}
.kpi-gold {{ --accent:{GOLD}; --accent-glow:rgba(251,191,36,0.12);  border-left:2px solid {GOLD}; }}
.kpi-card:hover {{ border-color:var(--accent); }}
.kpi-icon  {{ font-size:20px; margin-bottom:10px; display:block; }}
.kpi-label {{ font-family:'Fira Code',monospace; font-size:9px; letter-spacing:2px; text-transform:uppercase; color:{DIM}; margin-bottom:5px; }}
.kpi-num   {{ font-family:'Clash Display',sans-serif; font-size:30px; font-weight:700; color:{TEXT}; line-height:1; margin-bottom:3px; }}
.kpi-unit  {{ font-family:'Fira Code',monospace; font-size:10px; color:{DIM}; }}
.kpi-bar   {{ height:2px; border-radius:2px; margin-top:12px; background:linear-gradient(90deg,var(--accent),transparent); box-shadow:0 0 8px var(--accent); }}
.pulse-ring {{ position:absolute; top:50%; left:50%; transform:translate(-50%,-50%) scale(0); width:100%; height:100%; border-radius:18px; border:1px solid var(--accent); opacity:0; pointer-events:none; }}
.kpi-card:hover .pulse-ring {{ animation:kpiPulse 0.6s ease-out forwards; }}
@keyframes kpiPulse {{ 0%{{transform:translate(-50%,-50%) scale(0.85);opacity:0.6;}} 100%{{transform:translate(-50%,-50%) scale(1.08);opacity:0;}} }}

/* ── MODULE HEADER ───────────────────── */
.mod-header {{
    display:flex; align-items:flex-start; gap:20px;
    padding:26px 30px; border-radius:20px;
    background:linear-gradient(135deg,rgba(252,129,129,0.07) 0%,rgba(246,135,179,0.04) 100%);
    border:1px solid rgba(252,129,129,0.13);
    margin-bottom:22px; position:relative; overflow:hidden;
}}
.mod-header-line {{
    position:absolute; top:0; left:0; bottom:0; width:3px;
    background:linear-gradient(180deg,{CRIMSON},{ROSE},{CRIMSON});
    border-radius:0 2px 2px 0; box-shadow:0 0 12px rgba(252,129,129,0.5);
}}
.mod-icon {{ font-size:30px; flex-shrink:0; }}
.mod-code {{
    font-family:'Fira Code',monospace; font-size:9px; color:{CRIMSON};
    background:rgba(252,129,129,0.1); border:1px solid rgba(252,129,129,0.2);
    border-radius:4px; padding:2px 8px; display:inline-block; margin-bottom:6px; letter-spacing:1.5px;
}}
.mod-title {{ font-family:'Clash Display',sans-serif; font-size:22px; font-weight:700; color:{TEXT}; margin-bottom:4px; }}
.mod-desc  {{ font-size:12px; color:{MUTED}; line-height:1.6; }}

/* ── GLASS PANEL ─────────────────────── */
.glass-panel {{
    background:rgba(20,13,30,0.7); backdrop-filter:blur(16px);
    border:1px solid rgba(252,129,129,0.1); border-radius:18px; padding:22px;
    margin-bottom:18px;
    box-shadow:0 8px 32px rgba(0,0,0,0.4), 0 1px 0 rgba(255,255,255,0.03) inset;
    position:relative; overflow:hidden;
}}
.glass-panel::before {{
    content:''; position:absolute; top:0; left:0; right:0; height:1px;
    background:linear-gradient(90deg,transparent,rgba(252,129,129,0.2),rgba(246,135,179,0.15),transparent);
}}
.panel-label {{
    font-family:'Fira Code',monospace; font-size:9px; letter-spacing:2.5px;
    text-transform:uppercase; color:{DIM}; margin-bottom:14px;
    display:flex; align-items:center; gap:10px;
}}
.panel-label::after {{ content:''; flex:1; height:1px; background:linear-gradient(90deg,rgba(252,129,129,0.15),transparent); }}

/* ── STATUS GRID ─────────────────────── */
.file-grid {{ display:grid; grid-template-columns:repeat(5,1fr); gap:10px; margin:12px 0 20px; }}
.file-card {{
    border-radius:12px; padding:14px 14px 12px;
    display:flex; flex-direction:column; gap:4px;
    transition:all 0.2s ease;
}}
.file-ok  {{ background:rgba(52,211,153,0.06); border:1px solid rgba(52,211,153,0.2); }}
.file-miss{{ background:rgba(252,129,129,0.06); border:1px solid rgba(252,129,129,0.2); }}
.file-card:hover {{ transform:translateY(-2px); }}

/* ── ALERT BARS ──────────────────────── */
.alert-success {{
    background:rgba(52,211,153,0.08); border-left:3px solid {TEAL};
    border-radius:0 10px 10px 0; padding:0.8rem 1rem; margin:0.6rem 0;
    font-size:0.85rem; color:#9ae6b4;
}}
.alert-warn {{
    background:rgba(251,191,36,0.08); border-left:3px solid {GOLD};
    border-radius:0 10px 10px 0; padding:0.8rem 1rem; margin:0.6rem 0;
    font-size:0.85rem; color:#fcd34d;
}}
.alert-info {{
    background:rgba(103,232,249,0.08); border-left:3px solid {CYAN};
    border-radius:0 10px 10px 0; padding:0.8rem 1rem; margin:0.6rem 0;
    font-size:0.85rem; color:#a5f3fc;
}}
.alert-danger {{
    background:rgba(252,129,129,0.08); border-left:3px solid {CRIMSON};
    border-radius:0 10px 10px 0; padding:0.8rem 1rem; margin:0.6rem 0;
    font-size:0.85rem; color:#fca5a5;
}}

/* ── DIVIDER ─────────────────────────── */
.v-div {{ height:1px; border:none; margin:28px 0;
    background:linear-gradient(90deg,transparent,rgba(252,129,129,0.25),rgba(246,135,179,0.15),transparent); }}

/* ── TERMINAL ────────────────────────── */
.term {{
    background:#060412; border:1px solid #1a0d22; border-radius:12px;
    padding:20px 22px; font-family:'Fira Code',monospace;
    font-size:11px; line-height:2; color:{DIM}; margin-bottom:16px;
}}
.term .ok   {{ color:{TEAL}; }}
.term .hi   {{ color:{CRIMSON}; }}
.term .val  {{ color:{LAVENDER}; }}
.term .warn {{ color:{GOLD}; }}

/* ── CHIPS ───────────────────────────── */
.chip {{ display:inline-flex; align-items:center; gap:5px; padding:5px 14px; border-radius:999px; font-size:11px; font-weight:600; margin:3px; font-family:'Fira Code',monospace; }}
.chip-red  {{ background:rgba(252,129,129,0.1); border:1px solid rgba(252,129,129,0.3); color:{CRIMSON}; }}
.chip-rose {{ background:rgba(246,135,179,0.1); border:1px solid rgba(246,135,179,0.3); color:{ROSE}; }}
.chip-teal {{ background:rgba(52,211,153,0.1);  border:1px solid rgba(52,211,153,0.3);  color:{TEAL}; }}
.chip-lav  {{ background:rgba(192,132,252,0.1); border:1px solid rgba(192,132,252,0.3); color:{LAVENDER}; }}
.chip-gold {{ background:rgba(251,191,36,0.1);  border:1px solid rgba(251,191,36,0.3);  color:{GOLD}; }}

/* ── DETECTION METHOD CARDS ──────────── */
.method-card {{
    border-radius:14px; padding:18px 20px; position:relative; overflow:hidden;
    transition:all 0.25s ease;
}}
.method-card:hover {{ transform:translateY(-3px); }}
.method-card::before {{
    content:''; position:absolute; left:0; top:0; bottom:0; width:3px;
    background:var(--mc); box-shadow:0 0 10px var(--mc);
}}
.mc-red  {{ --mc:{CRIMSON}; background:rgba(252,129,129,0.05); border:1px solid rgba(252,129,129,0.14); }}
.mc-rose {{ --mc:{ROSE};    background:rgba(246,135,179,0.05); border:1px solid rgba(246,135,179,0.14); }}
.mc-teal {{ --mc:{TEAL};    background:rgba(52,211,153,0.05);  border:1px solid rgba(52,211,153,0.14); }}

/* ── STEP TRACK ──────────────────────── */
.steps-track {{
    display:flex; align-items:center; gap:0;
    padding:14px 22px; margin:18px 0;
    background:rgba(255,255,255,0.02);
    border:1px solid rgba(255,255,255,0.05); border-radius:14px;
}}
.step-node {{
    display:flex; flex-direction:column; align-items:center;
    gap:6px; flex:1; position:relative;
}}
.step-node::after {{
    content:''; position:absolute; top:13px; left:60%; right:-40%;
    height:1px; background:rgba(255,255,255,0.07);
}}
.step-node:last-child::after {{ display:none; }}
.step-circle {{
    width:28px; height:28px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:11px; font-weight:700; font-family:'Fira Code',monospace;
    border:1px solid rgba(255,255,255,0.1);
    background:rgba(255,255,255,0.04); color:{DIM}; z-index:1;
}}
.step-circle.s-done {{ background:rgba(52,211,153,0.15); border-color:{TEAL}; color:{TEAL}; box-shadow:0 0 12px rgba(52,211,153,0.2); }}
.step-circle.s-active {{ background:linear-gradient(135deg,rgba(252,129,129,0.2),rgba(246,135,179,0.15)); border-color:{CRIMSON}; color:{CRIMSON}; box-shadow:0 0 16px rgba(252,129,129,0.3); }}
.step-node.s-done-conn::after {{ background:linear-gradient(90deg,{TEAL},rgba(255,255,255,0.07)); }}
.step-lbl {{ font-family:'Fira Code',monospace; font-size:9px; color:{DIM}; letter-spacing:1px; white-space:nowrap; text-align:center; }}
.step-lbl.s-active {{ color:{CRIMSON}; }} .step-lbl.s-done {{ color:{TEAL}; }}

/* ── INSIGHT BADGE ───────────────────── */
.insight-badge {{
    display:inline-flex; align-items:center; gap:6px;
    padding:5px 13px; border-radius:8px;
    font-family:'Fira Code',monospace; font-size:11px; font-weight:600; margin:3px 3px 3px 0;
}}
.badge-up   {{ background:rgba(52,211,153,0.1);  border:1px solid rgba(52,211,153,0.3);  color:{TEAL}; }}
.badge-down {{ background:rgba(252,129,129,0.1); border:1px solid rgba(252,129,129,0.3); color:{CRIMSON}; }}
.badge-warn {{ background:rgba(251,191,36,0.1);  border:1px solid rgba(251,191,36,0.3);  color:{GOLD}; }}

/* ── ACCURACY CARD ───────────────────── */
.acc-card {{
    border-radius:16px; padding:20px 18px; text-align:center;
    position:relative; overflow:hidden; flex:1; min-width:140px;
    transition:all 0.25s ease;
}}
.acc-card:hover {{ transform:translateY(-4px); }}
.acc-pass {{ background:rgba(52,211,153,0.08); border:1px solid rgba(52,211,153,0.25); }}
.acc-fail {{ background:rgba(252,129,129,0.08); border:1px solid rgba(252,129,129,0.25); }}
.acc-overall {{ background:rgba(251,191,36,0.08); border:1px solid rgba(251,191,36,0.25); }}

/* ── CHECKLIST ROW ───────────────────── */
.chk-row {{
    display:flex; align-items:center; gap:1rem; padding:0.65rem 0;
    border-bottom:1px solid rgba(252,129,129,0.07);
    transition:background 0.15s;
}}
.chk-row:hover {{ background:rgba(252,129,129,0.03); border-radius:8px; padding-left:8px; }}

/* ── Streamlit overrides ─────────────── */
[data-testid="stFileUploader"] {{
    background:rgba(20,13,30,0.6); border:2px dashed rgba(252,129,129,0.2);
    border-radius:14px; padding:0.5rem;
}}
div[data-testid="stButton"] > button {{
    background:linear-gradient(135deg,rgba(252,129,129,0.12),rgba(246,135,179,0.08)) !important;
    border:1px solid rgba(252,129,129,0.3) !important; color:{CRIMSON} !important;
    border-radius:10px !important; font-family:'Fira Code',monospace !important;
    font-size:12px !important; transition:all 0.2s ease !important;
}}
div[data-testid="stButton"] > button:hover {{
    background:linear-gradient(135deg,rgba(252,129,129,0.22),rgba(246,135,179,0.15)) !important;
    border-color:{CRIMSON} !important; box-shadow:0 0 24px rgba(252,129,129,0.3) !important;
    transform:translateY(-2px) !important;
}}
div[data-testid="stExpander"] {{
    background:{LAYER} !important; border:1px solid {EDGE} !important; border-radius:12px !important;
}}
div[data-testid="stExpander"] summary {{ color:{MUTED} !important; }}
div[data-testid="stExpander"][open] summary {{ color:{CRIMSON} !important; }}
h1,h2,h3 {{ font-family:'Clash Display',sans-serif !important; color:{TEXT} !important; }}
.stRadio > label {{ display:none !important; }}

/* ── Animations ──────────────────────── */
@keyframes fadeUp {{ from{{opacity:0;transform:translateY(20px);}} to{{opacity:1;transform:translateY(0);}} }}
.f1{{animation:fadeUp 0.5s ease both;}} .f2{{animation:fadeUp 0.5s 0.08s ease both;}}
.f3{{animation:fadeUp 0.5s 0.16s ease both;}} .f4{{animation:fadeUp 0.5s 0.24s ease both;}}
.f5{{animation:fadeUp 0.5s 0.32s ease both;}}

::-webkit-scrollbar{{width:5px;height:5px;}} ::-webkit-scrollbar-track{{background:{VOID};}}
::-webkit-scrollbar-thumb{{background:{EDGE};border-radius:3px;}} ::-webkit-scrollbar-thumb:hover{{background:{CRIMSON};}}
</style>
""", unsafe_allow_html=True)

# ── Helper functions ──────────────────────────────────────────────────────────
def ui_success(msg): st.markdown(f'<div class="alert-success">✅ {msg}</div>', unsafe_allow_html=True)
def ui_warn(msg):    st.markdown(f'<div class="alert-warn">⚠️ {msg}</div>', unsafe_allow_html=True)
def ui_info(msg):    st.markdown(f'<div class="alert-info">ℹ️ {msg}</div>', unsafe_allow_html=True)
def ui_danger(msg):  st.markdown(f'<div class="alert-danger">🚨 {msg}</div>', unsafe_allow_html=True)

def kpi_row(*items):
    html = '<div class="kpi-orbit">'
    for icon, label, num, unit, cls in items:
        html += (f'<div class="kpi-card {cls}"><div class="pulse-ring"></div>'
                 f'<span class="kpi-icon">{icon}</span>'
                 f'<div class="kpi-label">{label}</div>'
                 f'<div class="kpi-num">{num}</div>'
                 f'<div class="kpi-unit">{unit}</div>'
                 f'<div class="kpi-bar"></div></div>')
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def mod_header(icon, code, title, desc):
    st.markdown(f"""
    <div class="mod-header f1"><div class="mod-header-line"></div>
        <span class="mod-icon">{icon}</span>
        <div><span class="mod-code">{code}</span>
        <div class="mod-title">{title}</div>
        <div class="mod-desc">{desc}</div></div>
    </div>""", unsafe_allow_html=True)

def step_track(pages, cur):
    nodes = ""
    for i, (p, ic) in enumerate(zip(pages, NAV_ICONS)):
        done   = i < cur
        active = i == cur
        scls   = "s-done" if done else ("s-active" if active else "")
        lcls   = "s-done" if done else ("s-active" if active else "")
        ccls   = "s-done-conn" if done else ""
        inner  = "✓" if done else ic
        nodes += (f'<div class="step-node {ccls}">'
                  f'<div class="step-circle {scls}">{inner}</div>'
                  f'<div class="step-lbl {lcls}">{p}</div></div>')
    st.markdown(f'<div class="steps-track">{nodes}</div>', unsafe_allow_html=True)

# ── Required files ────────────────────────────────────────────────────────────
REQUIRED_FILES = {
    "dailyActivity_merged.csv":     {"key_cols": ["ActivityDate", "TotalSteps", "Calories"],       "label": "Daily Activity",    "icon": "🏃"},
    "hourlySteps_merged.csv":       {"key_cols": ["ActivityHour", "StepTotal"],                    "label": "Hourly Steps",      "icon": "👣"},
    "hourlyIntensities_merged.csv": {"key_cols": ["ActivityHour", "TotalIntensity"],               "label": "Hourly Intensities","icon": "⚡"},
    "minuteSleep_merged.csv":       {"key_cols": ["date", "value", "logId"],                       "label": "Minute Sleep",      "icon": "💤"},
    "heartrate_seconds_merged.csv": {"key_cols": ["Time", "Value"],                                "label": "Heart Rate",        "icon": "❤️"},
}
def score_match(df, req_info):
    return sum(1 for col in req_info["key_cols"] if col in df.columns)

# ── Anomaly detection functions ───────────────────────────────────────────────
def detect_hr_anomalies(master, hr_high=100, hr_low=50, residual_sigma=2.0):
    df = master[["Id","Date","AvgHR","MaxHR","MinHR"]].dropna().copy()
    df["Date"] = pd.to_datetime(df["Date"])
    hr_daily = df.groupby("Date")["AvgHR"].mean().reset_index()
    hr_daily.columns = ["Date","AvgHR"]
    hr_daily = hr_daily.sort_values("Date")
    hr_daily["thresh_high"] = hr_daily["AvgHR"] > hr_high
    hr_daily["thresh_low"]  = hr_daily["AvgHR"] < hr_low
    hr_daily["rolling_med"] = hr_daily["AvgHR"].rolling(3, center=True, min_periods=1).median()
    hr_daily["residual"]    = hr_daily["AvgHR"] - hr_daily["rolling_med"]
    resid_std = hr_daily["residual"].std()
    hr_daily["resid_anomaly"] = hr_daily["residual"].abs() > (residual_sigma * resid_std)
    hr_daily["is_anomaly"]    = hr_daily["thresh_high"] | hr_daily["thresh_low"] | hr_daily["resid_anomaly"]
    def reason(row):
        r = []
        if row["thresh_high"]:   r.append(f"HR>{hr_high}")
        if row["thresh_low"]:    r.append(f"HR<{hr_low}")
        if row["resid_anomaly"]: r.append(f"Residual±{residual_sigma:.0f}σ")
        return ", ".join(r) if r else ""
    hr_daily["reason"] = hr_daily.apply(reason, axis=1)
    return hr_daily

def detect_steps_anomalies(master, steps_low=500, steps_high=25000, residual_sigma=2.0):
    df = master[["Date","TotalSteps"]].dropna().copy()
    df["Date"] = pd.to_datetime(df["Date"])
    sd = df.groupby("Date")["TotalSteps"].mean().reset_index().sort_values("Date")
    sd["thresh_low"]  = sd["TotalSteps"] < steps_low
    sd["thresh_high"] = sd["TotalSteps"] > steps_high
    sd["rolling_med"] = sd["TotalSteps"].rolling(3, center=True, min_periods=1).median()
    sd["residual"]    = sd["TotalSteps"] - sd["rolling_med"]
    resid_std = sd["residual"].std()
    sd["resid_anomaly"] = sd["residual"].abs() > (residual_sigma * resid_std)
    sd["is_anomaly"]    = sd["thresh_low"] | sd["thresh_high"] | sd["resid_anomaly"]
    def reason(row):
        r = []
        if row["thresh_low"]:    r.append(f"Steps<{steps_low}")
        if row["thresh_high"]:   r.append(f"Steps>{steps_high}")
        if row["resid_anomaly"]: r.append(f"Residual±{residual_sigma:.0f}σ")
        return ", ".join(r) if r else ""
    sd["reason"] = sd.apply(reason, axis=1)
    return sd

def detect_sleep_anomalies(master, sleep_low=60, sleep_high=600, residual_sigma=2.0):
    df = master[["Date","TotalSleepMinutes"]].dropna().copy()
    df["Date"] = pd.to_datetime(df["Date"])
    sd = df.groupby("Date")["TotalSleepMinutes"].mean().reset_index().sort_values("Date")
    sd["thresh_low"]  = (sd["TotalSleepMinutes"] > 0) & (sd["TotalSleepMinutes"] < sleep_low)
    sd["thresh_high"] = sd["TotalSleepMinutes"] > sleep_high
    sd["no_data"]     = sd["TotalSleepMinutes"] == 0
    sd["rolling_med"] = sd["TotalSleepMinutes"].rolling(3, center=True, min_periods=1).median()
    sd["residual"]    = sd["TotalSleepMinutes"] - sd["rolling_med"]
    resid_std = sd["residual"].std()
    sd["resid_anomaly"] = sd["residual"].abs() > (residual_sigma * resid_std)
    sd["is_anomaly"]    = sd["thresh_low"] | sd["thresh_high"] | sd["resid_anomaly"]
    def reason(row):
        r = []
        if row["no_data"]:       r.append("No device worn")
        if row["thresh_low"]:    r.append(f"Sleep<{sleep_low}min")
        if row["thresh_high"]:   r.append(f"Sleep>{sleep_high}min")
        if row["resid_anomaly"]: r.append(f"Residual±{residual_sigma:.0f}σ")
        return ", ".join(r) if r else ""
    sd["reason"] = sd.apply(reason, axis=1)
    return sd

def simulate_accuracy(master, n_inject=10):
    np.random.seed(42)
    df = master[["Date","AvgHR","TotalSteps","TotalSleepMinutes"]].dropna().copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df_daily = df.groupby("Date").mean().reset_index().sort_values("Date")
    results = {}
    for col, injvals, lo, hi, key in [
        ("AvgHR",           [115,120,125,35,40,45,118,130,38,42], 50,  100,   "Heart Rate"),
        ("TotalSteps",      [50,100,150,30000,35000,28000,80,200,31000,29000], 500, 25000, "Steps"),
        ("TotalSleepMinutes",[10,20,30,700,750,800,15,25,710,720], 60,  600,   "Sleep"),
    ]:
        sim = df_daily[["Date", col]].copy()
        idx = np.random.choice(len(sim), n_inject, replace=False)
        sim.loc[idx, col] = np.random.choice(injvals, n_inject, replace=True)
        sim["rm"] = sim[col].rolling(3, center=True, min_periods=1).median()
        sim["r"]  = sim[col] - sim["rm"]
        rs = sim["r"].std()
        sim["det"] = (sim[col] < lo) | (sim[col] > hi) | (sim["r"].abs() > 2 * rs)
        tp = sim.iloc[idx]["det"].sum()
        results[key] = {"injected": n_inject, "detected": int(tp), "accuracy": round(tp / n_inject * 100, 1)}
    results["Overall"] = round(np.mean([results[k]["accuracy"] for k in ["Heart Rate","Steps","Sleep"]]), 1)
    return results

# ══════════════════════════════════════════════════════════════════════════════
#  TOP NAV
# ══════════════════════════════════════════════════════════════════════════════
cur  = st.session_state.pg3
page = PAGES[cur]

links_html = ""
for i, (p, ic) in enumerate(zip(PAGES, NAV_ICONS)):
    cls = "active" if i == cur else ""
    links_html += (f'<div class="topnav-link {cls}">'
                   f'<span class="nav-dot"></span>'
                   f'<span style="font-size:11px;opacity:0.5;">{ic}</span>'
                   f'<span>{p}</span></div>')

st.markdown(f"""
<div class="topnav">
    <div class="topnav-brand">
        <div class="topnav-logo">
            <svg width="20" height="20" viewBox="0 0 32 32" fill="none">
                <polyline points="3,16 9,16 12,7 16,25 20,11 24,20 27,16 29,16"
                    stroke="{CRIMSON}" stroke-width="2.2" stroke-linecap="round"
                    stroke-linejoin="round" fill="none"/>
            </svg>
        </div>
        <div class="topnav-name">FitPulse</div>
        <span class="topnav-badge">M3</span>
    </div>
    <div class="topnav-links">{links_html}</div>
    <div class="topnav-right">
        <div class="topnav-stat">35 users · 31 days</div>
        <div class="topnav-live"><span class="live-dot"></span> ANOMALY SCAN</div>
    </div>
</div>""", unsafe_allow_html=True)

# Nav buttons
active_css = ""
for i in range(len(PAGES)):
    if i == cur:
        active_css += f"""
div[data-testid="column"]:nth-child({i+2}) div[data-testid="stButton"] > button {{
    background:linear-gradient(135deg,rgba(252,129,129,0.22),rgba(246,135,179,0.15)) !important;
    border-color:{CRIMSON} !important; color:{CRIMSON} !important;
    box-shadow:0 0 20px rgba(252,129,129,0.25) !important;
}}"""
st.markdown(f"<style>{active_css}</style>", unsafe_allow_html=True)

nb = st.columns(len(PAGES) + 2)
for i, (p, ic, desc) in enumerate(zip(PAGES, NAV_ICONS, NAV_DESCS)):
    with nb[i+1]:
        if st.button(f"{ic}  {p}", key=f"nav3_{p}", use_container_width=True, help=desc):
            st.session_state.pg3 = i
            st.rerun()

st.markdown("<hr class='v-div' style='margin-top:8px;'>", unsafe_allow_html=True)
step_track(PAGES, cur)

# ── guard helper (must be before if/elif chain) ───────────────────────────────
def require_detection():
    if not st.session_state.files_loaded:
        ui_warn("Go to **Overview** tab first to upload CSV files and load data.")
        return False
    if not st.session_state.anomaly_done:
        ui_warn("Go to **Overview** tab and click **Run All Anomaly Detection Methods** first.")
        return False
    return True

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: OVERVIEW  (data loading)
# ══════════════════════════════════════════════════════════════════════════════
if page == "Overview":
    st.markdown(f"""
    <div class="m3-hero f1">
        <div class="hero-ring"></div>
        <div style="position:relative;z-index:2;">
            <div class="hero-kicker">Milestone 3 · Anomaly Detection Observatory</div>
            <div class="hero-title">FitPulse<br>Anomaly Detector</div>
            <p class="hero-sub">Threshold violations · Rolling residuals · DBSCAN structural outliers · 90%+ accuracy validation on real Fitbit data.</p>
            <div class="hero-pills">
                <div class="hero-pill"><span>🚨</span> 3 Detection Methods</div>
                <div class="hero-pill"><span>❤️</span> Heart Rate</div>
                <div class="hero-pill"><span>💤</span> Sleep</div>
                <div class="hero-pill"><span>🚶</span> Steps</div>
                <div class="hero-pill"><span>🔍</span> DBSCAN Outliers</div>
                <div class="hero-pill"><span>🎯</span> 90%+ Accuracy</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    mod_header("📂", "SECTION 01 · DATA LOADING", "Upload Fitbit CSV Files",
               "Auto-detect all 5 required Fitbit CSV files by column structure — same dataset as Milestone 2")

    ui_info("Upload the same 5 Fitbit CSV files as Milestone 2. Files are auto-detected by column structure — you can drop them in any order.")

    uploaded_files = st.file_uploader(
        "📁  Drop all 5 Fitbit CSV files here",
        type="csv", accept_multiple_files=True, key="m3_uploader",
        help="Hold Ctrl / Cmd to select multiple files"
    )

    detected = {}
    if uploaded_files:
        raw_uploads = []
        for uf in uploaded_files:
            try:
                raw_uploads.append((uf.name, pd.read_csv(uf)))
            except Exception:
                pass
        for req_name, finfo in REQUIRED_FILES.items():
            best_s, best_df = 0, None
            for uname, udf in raw_uploads:
                s = score_match(udf, finfo)
                if s > best_s:
                    best_s, best_df = s, udf
            if best_s >= 2:
                detected[req_name] = best_df

    # File status grid
    st.markdown('<div class="file-grid">', unsafe_allow_html=True)
    for req_name, finfo in REQUIRED_FILES.items():
        found = req_name in detected
        cls   = "file-ok" if found else "file-miss"
        ico   = "✅" if found else "❌"
        st.markdown(
            f'<div class="file-card {cls}">'
            f'<div style="font-size:1.3rem">{ico} {finfo["icon"]}</div>'
            f'<div style="font-size:0.78rem;font-weight:600;color:{TEXT};margin-top:4px">{finfo["label"]}</div>'
            f'<div style="font-family:Fira Code,monospace;font-size:0.65rem;color:{MUTED};margin-top:2px">'
            f'{"Found ✓" if found else "Missing"}</div></div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

    n_up = len(detected)
    kpi_row(
        ("📁", "FILES DETECTED", str(n_up),    "/ 5",    "kpi-red"),
        ("❌", "FILES MISSING",  str(5-n_up),  "files",  "kpi-rose" if 5-n_up else "kpi-teal"),
        ("✅", "STATUS",        "Ready" if n_up==5 else "Waiting", "", "kpi-teal" if n_up==5 else "kpi-lav"),
        ("📊", "TOTAL ROWS",    "–",           "after load", "kpi-lav"),
        ("👤", "USERS",         "–",           "after load", "kpi-gold"),
    )

    if n_up < 5:
        missing = [REQUIRED_FILES[r]["label"] for r in REQUIRED_FILES if r not in detected]
        ui_warn(f"Missing: {', '.join(missing)}")

    if st.button("⚡  Load & Build Master DataFrame", disabled=(n_up < 5)):
        with st.spinner("Parsing and merging all datasets…"):
            try:
                daily    = detected["dailyActivity_merged.csv"].copy()
                hourly_s = detected["hourlySteps_merged.csv"].copy()
                hourly_i = detected["hourlyIntensities_merged.csv"].copy()
                sleep    = detected["minuteSleep_merged.csv"].copy()
                hr       = detected["heartrate_seconds_merged.csv"].copy()

                daily["ActivityDate"]    = pd.to_datetime(daily["ActivityDate"],    format="%m/%d/%Y")
                hourly_s["ActivityHour"] = pd.to_datetime(hourly_s["ActivityHour"], format="%m/%d/%Y %I:%M:%S %p")
                hourly_i["ActivityHour"] = pd.to_datetime(hourly_i["ActivityHour"], format="%m/%d/%Y %I:%M:%S %p")
                sleep["date"]            = pd.to_datetime(sleep["date"],            format="%m/%d/%Y %I:%M:%S %p")
                hr["Time"]               = pd.to_datetime(hr["Time"],               format="%m/%d/%Y %I:%M:%S %p")

                hr_minute = (hr.set_index("Time").groupby("Id")["Value"]
                               .resample("1min").mean().reset_index())
                hr_minute.columns = ["Id","Time","HeartRate"]
                hr_minute = hr_minute.dropna()
                hr_minute["Date"] = hr_minute["Time"].dt.date

                hr_daily = (hr_minute.groupby(["Id","Date"])["HeartRate"]
                            .agg(["mean","max","min","std"]).reset_index()
                            .rename(columns={"mean":"AvgHR","max":"MaxHR","min":"MinHR","std":"StdHR"}))

                sleep["Date"] = sleep["date"].dt.date
                sleep_daily = (sleep.groupby(["Id","Date"])
                               .agg(TotalSleepMinutes=("value","count"),
                                    DominantSleepStage=("value", lambda x: x.mode()[0]))
                               .reset_index())

                master = daily.copy().rename(columns={"ActivityDate":"Date"})
                master["Date"] = master["Date"].dt.date
                master = master.merge(hr_daily,    on=["Id","Date"], how="left")
                master = master.merge(sleep_daily, on=["Id","Date"], how="left")
                master["TotalSleepMinutes"]  = master["TotalSleepMinutes"].fillna(0)
                master["DominantSleepStage"] = master["DominantSleepStage"].fillna(0)
                for col in ["AvgHR","MaxHR","MinHR","StdHR"]:
                    master[col] = master.groupby("Id")[col].transform(lambda x: x.fillna(x.median()))

                st.session_state.update({
                    "daily": daily, "hourly_s": hourly_s, "hourly_i": hourly_i,
                    "sleep": sleep, "hr": hr, "hr_minute": hr_minute,
                    "master": master, "files_loaded": True
                })
                st.rerun()
            except Exception as e:
                st.error(f"Error building master: {e}")

    if st.session_state.files_loaded:
        master = st.session_state.master
        ui_success(f"Master DataFrame ready — {master.shape[0]:,} rows · {master['Id'].nunique()} users · {master['Date'].nunique()} dates")

        st.markdown("<hr class='v-div'>", unsafe_allow_html=True)
        mod_header("🔬", "DETECTION METHODS", "Three-Layer Anomaly Detection",
                   "All three methods run simultaneously — results viewable in the section tabs above")

        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:20px;">
            <div class="method-card mc-red f2">
                <div style="font-family:'Clash Display',sans-serif;font-size:15px;font-weight:700;color:{TEXT};margin-bottom:6px">① Threshold Violations</div>
                <div style="font-size:12px;color:{MUTED};line-height:1.7">Hard upper/lower limits on HR, Steps, Sleep. Fast, interpretable, clinical-grade.</div>
                <div style="margin-top:10px;"><span class="chip chip-red">HR>{hr_high} / <{hr_low}</span></div>
            </div>
            <div class="method-card mc-rose f3">
                <div style="font-family:'Clash Display',sans-serif;font-size:15px;font-weight:700;color:{TEXT};margin-bottom:6px">② Residual-Based</div>
                <div style="font-size:12px;color:{MUTED};line-height:1.7">Rolling median baseline. Flag days where actual deviates by ±{sigma:.0f}σ from expected.</div>
                <div style="margin-top:10px;"><span class="chip chip-rose">±{sigma:.0f}σ Rolling Median</span></div>
            </div>
            <div class="method-card mc-teal f4">
                <div style="font-family:'Clash Display',sans-serif;font-size:15px;font-weight:700;color:{TEXT};margin-bottom:6px">③ DBSCAN Structural</div>
                <div style="font-size:12px;color:{MUTED};line-height:1.7">Cluster users by behaviour. DBSCAN label −1 = outlier with atypical activity pattern.</div>
                <div style="margin-top:10px;"><span class="chip chip-teal">eps=2.2 · min_samples=2</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔍  Run All Anomaly Detection Methods"):
            with st.spinner("Running detection pipeline…"):
                try:
                    anom_hr    = detect_hr_anomalies(master,    hr_high, hr_low,  sigma)
                    anom_steps = detect_steps_anomalies(master, st_low,  25000,   sigma)
                    anom_sleep = detect_sleep_anomalies(master, sl_low,  sl_high, sigma)
                    st.session_state.update({
                        "anom_hr": anom_hr, "anom_steps": anom_steps,
                        "anom_sleep": anom_sleep, "anomaly_done": True
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"Detection error: {e}")

        if st.session_state.anomaly_done:
            anom_hr    = st.session_state.anom_hr
            anom_steps = st.session_state.anom_steps
            anom_sleep = st.session_state.anom_sleep
            n_hr    = int(anom_hr["is_anomaly"].sum())
            n_steps = int(anom_steps["is_anomaly"].sum())
            n_sleep = int(anom_sleep["is_anomaly"].sum())
            n_total = n_hr + n_steps + n_sleep

            ui_danger(f"Detection complete — {n_total} total anomaly flags  (HR: {n_hr} · Steps: {n_steps} · Sleep: {n_sleep})")
            kpi_row(
                ("❤️", "HR ANOMALIES",    str(n_hr),    "days", "kpi-red"),
                ("🚶", "STEPS ANOMALIES", str(n_steps), "days", "kpi-rose"),
                ("💤", "SLEEP ANOMALIES", str(n_sleep), "days", "kpi-lav"),
                ("🚨", "TOTAL FLAGS",     str(n_total), "flags","kpi-gold"),
                ("✅", "METHODS",         "3",          "active","kpi-teal"),
            )

            st.markdown(f"""
            <div style="display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 4px;">
                <span class="insight-badge badge-down">🚨 {n_total} total anomalies flagged</span>
                <span class="insight-badge badge-up">✓ 3 detection methods complete</span>
                <span class="insight-badge badge-warn">Navigate tabs above to explore charts</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("<hr class='v-div'>", unsafe_allow_html=True)
        st.markdown('<div class="glass-panel f4"><div class="panel-label">Master DataFrame Preview</div>', unsafe_allow_html=True)
        st.dataframe(master.head(12), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: HEART RATE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Heart Rate":
    mod_header("❤️", "SECTION 02 · HEART RATE", "HR Anomaly Detection Chart",
               f"Threshold violations (>{hr_high} / <{hr_low} bpm) + rolling residual ±{sigma:.0f}σ with interactive Plotly chart")

    if not require_detection(): st.stop()

    master     = st.session_state.master
    anom_hr    = st.session_state.anom_hr
    n_hr       = int(anom_hr["is_anomaly"].sum())
    hr_normal  = anom_hr[~anom_hr["is_anomaly"]]
    hr_anom    = anom_hr[anom_hr["is_anomaly"]]

    kpi_row(
        ("📅", "DAYS ANALYSED",  str(len(anom_hr)),  "days",    "kpi-red"),
        ("🚨", "ANOMALOUS DAYS", str(n_hr),          "flagged", "kpi-rose"),
        ("✅", "NORMAL DAYS",    str(len(anom_hr)-n_hr), "days", "kpi-teal"),
        ("📈", "AVG HR",         f"{anom_hr['AvgHR'].mean():.1f}", "bpm", "kpi-lav"),
        ("📊", "MAX HR",         f"{anom_hr['AvgHR'].max():.1f}", "bpm", "kpi-gold"),
    )

    st.markdown("<hr class='v-div'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px;">
        <span class="insight-badge badge-down">🚨 {n_hr} anomalous days detected</span>
        <span class="insight-badge badge-warn">Thresholds: HR&gt;{hr_high} / &lt;{hr_low} bpm</span>
        <span class="insight-badge badge-up">±{sigma:.0f}σ residual band shown</span>
    </div>""", unsafe_allow_html=True)

    ui_info(f"Red markers = anomaly days. Dashed lines = thresholds. Shaded band = ±{sigma:.0f}σ expected range. Hover for details.")

    st.markdown('<div class="glass-panel f2"><div class="panel-label">Heart Rate Timeline — Anomaly Highlights · Chart 1 of 5</div>', unsafe_allow_html=True)

    resid_std_hr  = anom_hr["residual"].std()
    rolling_upper = anom_hr["rolling_med"] + sigma * resid_std_hr
    rolling_lower = anom_hr["rolling_med"] - sigma * resid_std_hr

    fig_hr = go.Figure()
    fig_hr.add_trace(go.Scatter(x=anom_hr["Date"], y=rolling_upper, mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip"))
    fig_hr.add_trace(go.Scatter(x=anom_hr["Date"], y=rolling_lower, mode="lines",
        fill="tonexty", fillcolor="rgba(103,232,249,0.07)", line=dict(width=0), name=f"±{sigma:.0f}σ Expected Band"))
    fig_hr.add_trace(go.Scatter(x=anom_hr["Date"], y=anom_hr["AvgHR"], mode="lines+markers",
        name="Avg Heart Rate", line=dict(color=CRIMSON, width=2.5),
        marker=dict(size=5, color=CRIMSON),
        hovertemplate="<b>%{x}</b><br>HR: %{y:.1f} bpm<extra></extra>"))
    fig_hr.add_trace(go.Scatter(x=anom_hr["Date"], y=anom_hr["rolling_med"], mode="lines",
        name="Rolling Median", line=dict(color=TEAL, width=1.5, dash="dot"),
        hovertemplate="<b>%{x}</b><br>Median: %{y:.1f} bpm<extra></extra>"))
    if not hr_anom.empty:
        fig_hr.add_trace(go.Scatter(x=hr_anom["Date"], y=hr_anom["AvgHR"],
            mode="markers", name="🚨 Anomaly",
            marker=dict(color=ROSE, size=15, symbol="circle", line=dict(color="white", width=2),
                        opacity=1),
            hovertemplate="<b>%{x}</b><br>HR: %{y:.1f} bpm<br><b>ANOMALY</b><extra>⚠️</extra>"))
        for _, row in hr_anom.iterrows():
            fig_hr.add_annotation(x=row["Date"], y=row["AvgHR"],
                text=f"⚠️ {row['reason']}", showarrow=True,
                arrowhead=2, arrowcolor=ROSE, arrowsize=1.2, ax=0, ay=-48,
                font=dict(color=ROSE, size=9),
                bgcolor="rgba(20,13,30,0.9)", bordercolor="rgba(246,135,179,0.4)",
                borderwidth=1, borderpad=4)
    fig_hr.add_hline(y=hr_high, line_dash="dash", line_color=CRIMSON, line_width=1.5, opacity=0.7,
                     annotation_text=f"High ({hr_high} bpm)", annotation_position="top right",
                     annotation_font_color=CRIMSON)
    fig_hr.add_hline(y=hr_low, line_dash="dash", line_color=LAVENDER, line_width=1.5, opacity=0.7,
                     annotation_text=f"Low ({hr_low} bpm)", annotation_position="bottom right",
                     annotation_font_color=LAVENDER)

    apply_theme(fig_hr, "❤️ Heart Rate — Anomaly Detection (Real Fitbit Data)", height=500)
    fig_hr.update_layout(xaxis_title="Date", yaxis_title="Heart Rate (bpm)")
    st.plotly_chart(fig_hr, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if not hr_anom.empty:
        with st.expander(f"📋  View {len(hr_anom)} HR Anomaly Records"):
            st.dataframe(
                hr_anom[["Date","AvgHR","rolling_med","residual","reason"]]
                .rename(columns={"rolling_med":"Expected","residual":"Deviation","reason":"Anomaly Reason"})
                .round(2), use_container_width=True)

    # Residual distribution
    st.markdown("<hr class='v-div'>", unsafe_allow_html=True)
    st.markdown('<div class="glass-panel f3"><div class="panel-label">HR Residual Distribution — Anomaly vs Normal Days</div>', unsafe_allow_html=True)
    rc1, rc2 = st.columns(2)
    with rc1:
        fig_res = go.Figure()
        fig_res.add_trace(go.Histogram(x=anom_hr[~anom_hr["is_anomaly"]]["residual"],
            name="Normal", marker_color=TEAL, opacity=0.7, nbinsx=20))
        fig_res.add_trace(go.Histogram(x=anom_hr[anom_hr["is_anomaly"]]["residual"],
            name="Anomaly", marker_color=CRIMSON, opacity=0.85, nbinsx=10))
        apply_theme(fig_res, "Residual Distribution", height=300)
        fig_res.update_layout(barmode="overlay", xaxis_title="Residual (bpm)", yaxis_title="Count")
        st.plotly_chart(fig_res, use_container_width=True)
    with rc2:
        fig_box = go.Figure()
        fig_box.add_trace(go.Box(y=anom_hr[~anom_hr["is_anomaly"]]["AvgHR"],
            name="Normal Days", marker_color=TEAL, boxmean=True))
        fig_box.add_trace(go.Box(y=anom_hr[anom_hr["is_anomaly"]]["AvgHR"],
            name="Anomaly Days", marker_color=CRIMSON, boxmean=True))
        apply_theme(fig_box, "HR Distribution by Status", height=300)
        fig_box.update_layout(yaxis_title="Heart Rate (bpm)")
        st.plotly_chart(fig_box, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: SLEEP
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Sleep":
    mod_header("💤", "SECTION 03 · SLEEP", "Sleep Pattern Anomaly Visualization",
               f"Insufficient sleep (<{sl_low} min) · Excessive sleep (>{sl_high} min) · Residual-based detection")

    if not require_detection(): st.stop()

    master     = st.session_state.master
    anom_sleep = st.session_state.anom_sleep
    n_sleep    = int(anom_sleep["is_anomaly"].sum())
    sleep_anom = anom_sleep[anom_sleep["is_anomaly"]]

    kpi_row(
        ("📅", "DAYS ANALYSED",  str(len(anom_sleep)), "days",    "kpi-lav"),
        ("🚨", "ANOMALOUS DAYS", str(n_sleep),          "flagged", "kpi-red"),
        ("✅", "NORMAL DAYS",    str(len(anom_sleep)-n_sleep), "days", "kpi-teal"),
        ("😴", "AVG SLEEP",      f"{anom_sleep['TotalSleepMinutes'].mean():.0f}", "min/night", "kpi-rose"),
        ("📊", "HEALTHY RANGE",  f"{sl_low}–{sl_high}", "min", "kpi-gold"),
    )

    st.markdown("<hr class='v-div'>", unsafe_allow_html=True)
    ui_info(f"Lavender = insufficient sleep (<{sl_low} min). Red diamonds = anomaly days. Green band = healthy zone ({sl_low}–{sl_high} min).")

    st.markdown('<div class="glass-panel f2"><div class="panel-label">Sleep Duration Timeline — Dual Subplot · Chart 2 of 5</div>', unsafe_allow_html=True)

    fig_sleep = make_subplots(rows=2, cols=1, shared_xaxes=True,
        row_heights=[0.68, 0.32],
        subplot_titles=["Sleep Duration (avg minutes/night)", "Deviation from Expected Baseline"],
        vertical_spacing=0.09)

    fig_sleep.add_hrect(y0=sl_low, y1=sl_high, fillcolor="rgba(52,211,153,0.06)",
        line_width=0, annotation_text="✅ Healthy Zone",
        annotation_position="top right",
        annotation_font_color=TEAL, row=1, col=1)

    fig_sleep.add_trace(go.Scatter(x=anom_sleep["Date"], y=anom_sleep["TotalSleepMinutes"],
        mode="lines+markers", name="Sleep Minutes",
        line=dict(color=LAVENDER, width=2.5),
        marker=dict(size=5, color=LAVENDER),
        hovertemplate="<b>%{x}</b><br>Sleep: %{y:.0f} min<extra></extra>"), row=1, col=1)

    fig_sleep.add_trace(go.Scatter(x=anom_sleep["Date"], y=anom_sleep["rolling_med"],
        mode="lines", name="Rolling Median",
        line=dict(color=TEAL, width=1.5, dash="dot"),
        hovertemplate="<b>%{x}</b><br>Median: %{y:.0f} min<extra></extra>"), row=1, col=1)

    if not sleep_anom.empty:
        fig_sleep.add_trace(go.Scatter(x=sleep_anom["Date"], y=sleep_anom["TotalSleepMinutes"],
            mode="markers", name="🚨 Sleep Anomaly",
            marker=dict(color=CRIMSON, size=14, symbol="diamond", line=dict(color="white", width=2)),
            hovertemplate="<b>%{x}</b><br>Sleep: %{y:.0f} min<br><b>ANOMALY</b><extra>⚠️</extra>"),
            row=1, col=1)
        for _, row in sleep_anom.iterrows():
            fig_sleep.add_annotation(x=row["Date"], y=row["TotalSleepMinutes"],
                text=f"⚠️ {row['reason']}", showarrow=True,
                arrowhead=2, arrowcolor=ROSE, arrowsize=1.1, ax=20, ay=-40,
                font=dict(color=ROSE, size=8),
                bgcolor="rgba(20,13,30,0.9)", bordercolor="rgba(246,135,179,0.3)",
                borderwidth=1, borderpad=3, row=1, col=1)

    fig_sleep.add_hline(y=sl_low, line_dash="dash", line_color=CRIMSON, line_width=1.5, opacity=0.7, row=1, col=1,
        annotation_text=f"Min ({sl_low} min)", annotation_font_color=CRIMSON)
    fig_sleep.add_hline(y=sl_high, line_dash="dash", line_color=CYAN, line_width=1.5, opacity=0.7, row=1, col=1,
        annotation_text=f"Max ({sl_high} min)", annotation_font_color=CYAN)

    colors_resid = [CRIMSON if v else LAVENDER for v in anom_sleep["resid_anomaly"]]
    fig_sleep.add_trace(go.Bar(x=anom_sleep["Date"], y=anom_sleep["residual"],
        name="Residual", marker_color=colors_resid, opacity=0.8,
        hovertemplate="<b>%{x}</b><br>Residual: %{y:.0f} min<extra></extra>"), row=2, col=1)
    fig_sleep.add_hline(y=0, line_dash="solid", line_color=DIM, line_width=1, row=2, col=1)

    fig_sleep.update_layout(height=580, paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=TEXT, family="Inter, sans-serif"),
        showlegend=True,
        legend=dict(bgcolor="rgba(20,13,30,0.85)", bordercolor=EDGE, borderwidth=1, font=dict(color=TEXT)),
        hoverlabel=dict(bgcolor=CARD, bordercolor=EDGE, font=dict(color=TEXT)),
        margin=dict(l=55, r=30, t=60, b=50))
    fig_sleep.update_xaxes(gridcolor=GRID_CLR, tickfont=dict(color=MUTED, size=10))
    fig_sleep.update_yaxes(gridcolor=GRID_CLR, tickfont=dict(color=MUTED, size=10))
    st.plotly_chart(fig_sleep, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if not sleep_anom.empty:
        with st.expander(f"📋  View {len(sleep_anom)} Sleep Anomaly Records"):
            st.dataframe(
                sleep_anom[["Date","TotalSleepMinutes","rolling_med","residual","reason"]]
                .rename(columns={"TotalSleepMinutes":"Sleep (min)","rolling_med":"Expected",
                                 "residual":"Deviation","reason":"Anomaly Reason"})
                .round(2), use_container_width=True)

    st.markdown("<hr class='v-div'>", unsafe_allow_html=True)
    st.markdown('<div class="glass-panel f3"><div class="panel-label">Sleep Quality Distribution</div>', unsafe_allow_html=True)
    sc1, sc2 = st.columns(2)
    with sc1:
        fig_shist = go.Figure()
        fig_shist.add_trace(go.Histogram(x=anom_sleep[~anom_sleep["is_anomaly"]]["TotalSleepMinutes"],
            name="Normal nights", marker_color=LAVENDER, opacity=0.75, nbinsx=20))
        fig_shist.add_trace(go.Histogram(x=anom_sleep[anom_sleep["is_anomaly"]]["TotalSleepMinutes"],
            name="Anomaly nights", marker_color=CRIMSON, opacity=0.85, nbinsx=10))
        apply_theme(fig_shist, "Sleep Duration Distribution", height=300)
        fig_shist.update_layout(barmode="overlay", xaxis_title="Minutes", yaxis_title="Nights")
        st.plotly_chart(fig_shist, use_container_width=True)
    with sc2:
        cats = ["Normal","< Min","Excessive","No Data"]
        vals = [
            int((~anom_sleep["is_anomaly"]).sum()),
            int(anom_sleep["thresh_low"].sum()),
            int(anom_sleep["thresh_high"].sum()),
            int(anom_sleep["no_data"].sum()),
        ]
        fig_pie = go.Figure(go.Pie(labels=cats, values=vals, hole=0.5,
            marker=dict(colors=[TEAL, CRIMSON, GOLD, DIM]),
            textfont=dict(color=TEXT, size=11)))
        apply_theme(fig_pie, "Sleep Category Breakdown", height=300)
        fig_pie.update_layout(paper_bgcolor=PAPER_BG)
        st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: STEPS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Steps":
    mod_header("🚶", "SECTION 04 · STEPS", "Step Count Trend — Alert Bands & Residuals",
               f"Low activity (<{st_low:,} steps) · Extreme activity (>25,000) · Rolling residual deviation")

    if not require_detection(): st.stop()

    master     = st.session_state.master
    anom_steps = st.session_state.anom_steps
    n_steps    = int(anom_steps["is_anomaly"].sum())
    steps_anom = anom_steps[anom_steps["is_anomaly"]]

    kpi_row(
        ("📅", "DAYS ANALYSED",  str(len(anom_steps)), "days",  "kpi-teal"),
        ("🚨", "ANOMALOUS DAYS", str(n_steps),          "flagged","kpi-red"),
        ("✅", "NORMAL DAYS",    str(len(anom_steps)-n_steps), "days","kpi-rose"),
        ("🚶", "AVG STEPS",      f"{anom_steps['TotalSteps'].mean():,.0f}", "steps/day","kpi-lav"),
        ("📊", "MAX STEPS",      f"{anom_steps['TotalSteps'].max():,.0f}", "steps", "kpi-gold"),
    )

    st.markdown("<hr class='v-div'>", unsafe_allow_html=True)
    ui_info(f"Red bands = anomaly alert days. Dashed lines = step thresholds. Bar chart shows daily deviation from rolling trend.")

    st.markdown('<div class="glass-panel f2"><div class="panel-label">Daily Steps Trend — Alert Bands + Residuals · Chart 3 of 5</div>', unsafe_allow_html=True)

    fig_steps = make_subplots(rows=2, cols=1, shared_xaxes=True,
        row_heights=[0.65, 0.35],
        subplot_titles=["Daily Steps (avg across users)", "Residual Deviation from Trend"],
        vertical_spacing=0.09)

    for _, row in steps_anom.iterrows():
        d      = str(row["Date"])
        d_next = str(pd.Timestamp(d) + pd.Timedelta(days=1))[:10]
        fig_steps.add_vrect(x0=d, x1=d_next,
            fillcolor="rgba(252,129,129,0.12)", line_color="rgba(252,129,129,0.4)",
            line_width=1.2, row=1, col=1)

    fig_steps.add_trace(go.Scatter(x=anom_steps["Date"], y=anom_steps["TotalSteps"],
        mode="lines+markers", name="Avg Daily Steps",
        line=dict(color=TEAL, width=2.5), marker=dict(size=5, color=TEAL),
        hovertemplate="<b>%{x}</b><br>Steps: %{y:,.0f}<extra></extra>"), row=1, col=1)

    fig_steps.add_trace(go.Scatter(x=anom_steps["Date"], y=anom_steps["rolling_med"],
        mode="lines", name="Trend (Rolling Median)",
        line=dict(color=CYAN, width=2, dash="dash"),
        hovertemplate="<b>%{x}</b><br>Trend: %{y:,.0f}<extra></extra>"), row=1, col=1)

    if not steps_anom.empty:
        fig_steps.add_trace(go.Scatter(x=steps_anom["Date"], y=steps_anom["TotalSteps"],
            mode="markers", name="🚨 Steps Anomaly",
            marker=dict(color=CRIMSON, size=14, symbol="triangle-up", line=dict(color="white", width=2)),
            hovertemplate="<b>%{x}</b><br>Steps: %{y:,.0f}<br><b>ALERT</b><extra>⚠️</extra>"),
            row=1, col=1)

    fig_steps.add_hline(y=st_low, line_dash="dash", line_color=CRIMSON, line_width=1.5, opacity=0.8, row=1, col=1,
        annotation_text=f"Low Alert ({st_low:,} steps)", annotation_font_color=CRIMSON)
    fig_steps.add_hline(y=25000, line_dash="dash", line_color=ROSE, line_width=1.5, opacity=0.7, row=1, col=1,
        annotation_text="High Alert (25,000 steps)", annotation_font_color=ROSE)

    res_colors = [CRIMSON if v else TEAL for v in anom_steps["resid_anomaly"]]
    fig_steps.add_trace(go.Bar(x=anom_steps["Date"], y=anom_steps["residual"],
        name="Residual", marker_color=res_colors, opacity=0.85,
        hovertemplate="<b>%{x}</b><br>Deviation: %{y:,.0f} steps<extra></extra>"), row=2, col=1)
    fig_steps.add_hline(y=0, line_dash="solid", line_color=DIM, line_width=1, row=2, col=1)

    fig_steps.update_layout(height=580, paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=TEXT, family="Inter, sans-serif"), showlegend=True,
        legend=dict(bgcolor="rgba(20,13,30,0.85)", bordercolor=EDGE, borderwidth=1, font=dict(color=TEXT)),
        hoverlabel=dict(bgcolor=CARD, bordercolor=EDGE, font=dict(color=TEXT)),
        margin=dict(l=55, r=30, t=60, b=50))
    fig_steps.update_xaxes(gridcolor=GRID_CLR, tickfont=dict(color=MUTED, size=10))
    fig_steps.update_yaxes(gridcolor=GRID_CLR, tickfont=dict(color=MUTED, size=10))
    st.plotly_chart(fig_steps, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if not steps_anom.empty:
        with st.expander(f"📋  View {len(steps_anom)} Steps Anomaly Records"):
            st.dataframe(
                steps_anom[["Date","TotalSteps","rolling_med","residual","reason"]]
                .rename(columns={"TotalSteps":"Steps","rolling_med":"Expected",
                                 "residual":"Deviation","reason":"Anomaly Reason"})
                .round(2), use_container_width=True)

    st.markdown("<hr class='v-div'>", unsafe_allow_html=True)
    st.markdown('<div class="glass-panel f3"><div class="panel-label">Steps Analysis Breakdown</div>', unsafe_allow_html=True)
    sa1, sa2 = st.columns(2)
    with sa1:
        fig_sh = go.Figure()
        fig_sh.add_trace(go.Histogram(x=anom_steps[~anom_steps["is_anomaly"]]["TotalSteps"],
            name="Normal", marker_color=TEAL, opacity=0.7, nbinsx=20))
        fig_sh.add_trace(go.Histogram(x=anom_steps[anom_steps["is_anomaly"]]["TotalSteps"],
            name="Anomaly", marker_color=CRIMSON, opacity=0.85, nbinsx=10))
        apply_theme(fig_sh, "Steps Distribution", height=300)
        fig_sh.update_layout(barmode="overlay", xaxis_title="Steps", yaxis_title="Days")
        st.plotly_chart(fig_sh, use_container_width=True)
    with sa2:
        fig_scat = go.Figure()
        fig_scat.add_trace(go.Scatter(
            x=anom_steps["TotalSteps"], y=anom_steps["residual"],
            mode="markers",
            marker=dict(color=[CRIMSON if v else TEAL for v in anom_steps["is_anomaly"]],
                        size=10, opacity=0.8, line=dict(color="white", width=0.8)),
            text=anom_steps["Date"].astype(str),
            hovertemplate="<b>%{text}</b><br>Steps: %{x:,.0f}<br>Residual: %{y:,.0f}<extra></extra>"))
        apply_theme(fig_scat, "Steps vs Residual (red=anomaly)", height=300)
        fig_scat.update_layout(xaxis_title="Total Steps", yaxis_title="Residual")
        st.plotly_chart(fig_scat, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: DBSCAN
# ══════════════════════════════════════════════════════════════════════════════
elif page == "DBSCAN":
    mod_header("🔍", "SECTION 05 · DBSCAN", "Structural Outlier Detection via Clustering",
               "User-level anomaly detection — DBSCAN label −1 = structural outlier with atypical behaviour pattern")

    if not require_detection(): st.stop()
    master = st.session_state.master

    ui_info("Cluster each user using DBSCAN on their aggregated activity profile. Users labelled −1 don't fit any group — they are structural outliers.")

    cluster_cols = ["TotalSteps","Calories","VeryActiveMinutes",
                    "FairlyActiveMinutes","LightlyActiveMinutes",
                    "SedentaryMinutes","TotalSleepMinutes"]

    try:
        from sklearn.preprocessing import StandardScaler
        from sklearn.cluster import DBSCAN
        from sklearn.decomposition import PCA

        cf       = master.groupby("Id")[cluster_cols].mean().round(3).dropna()
        X_scaled = StandardScaler().fit_transform(cf)
        db_labels= DBSCAN(eps=2.2, min_samples=2).fit_predict(X_scaled)
        pca      = PCA(n_components=2, random_state=42)
        X_pca    = pca.fit_transform(X_scaled)
        var      = pca.explained_variance_ratio_ * 100

        cf["DBSCAN"]    = db_labels
        outlier_users   = cf[cf["DBSCAN"] == -1].index.tolist()
        n_outliers      = len(outlier_users)
        n_clusters      = len(set(db_labels)) - (1 if -1 in db_labels else 0)
        n_normal        = len(cf) - n_outliers

        kpi_row(
            ("👤", "TOTAL USERS",    str(len(cf)),    "users",    "kpi-lav"),
            ("🔍", "DBSCAN CLUSTERS",str(n_clusters), "groups",   "kpi-teal"),
            ("🚨", "OUTLIER USERS",  str(n_outliers), "anomalous","kpi-red"),
            ("✅", "NORMAL USERS",   str(n_normal),   "clustered","kpi-rose"),
            ("📊", "PCA VARIANCE",   f"{sum(var):.1f}%","PC1+PC2", "kpi-gold"),
        )

        st.markdown(f"""
        <div style="display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 16px;">
            <span class="insight-badge badge-down">🚨 {n_outliers} structural outlier users</span>
            <span class="insight-badge badge-up">✓ {n_normal} users clustered normally</span>
            <span class="insight-badge badge-warn">PC1+PC2 = {sum(var):.1f}% variance explained</span>
            <span class="insight-badge badge-up">K={n_clusters} DBSCAN groups</span>
        </div>""", unsafe_allow_html=True)

        st.markdown("<hr class='v-div'>", unsafe_allow_html=True)

        dc1, dc2 = st.columns([1.3, 1])
        with dc1:
            st.markdown('<div class="glass-panel f3"><div class="panel-label">DBSCAN PCA Projection — Outliers Highlighted · Chart 4 of 5</div>', unsafe_allow_html=True)
            CPAL = [TEAL, CYAN, GOLD, LAVENDER, ROSE]
            fig_db = go.Figure()
            for lbl in sorted(set(db_labels)):
                if lbl == -1: continue
                mask = db_labels == lbl
                fig_db.add_trace(go.Scatter(
                    x=X_pca[mask,0], y=X_pca[mask,1], mode="markers+text",
                    name=f"Cluster {lbl}",
                    marker=dict(size=14, color=CPAL[lbl % len(CPAL)], opacity=0.9,
                                line=dict(color="white", width=1.5)),
                    text=[str(uid)[-4:] for uid in cf.index[mask]],
                    textposition="top center", textfont=dict(size=8, color=TEXT),
                    hovertemplate="<b>User …%{text}</b><br>PC1: %{x:.2f}<br>PC2: %{y:.2f}<extra></extra>"))
            if n_outliers > 0:
                mask_out = db_labels == -1
                fig_db.add_trace(go.Scatter(
                    x=X_pca[mask_out,0], y=X_pca[mask_out,1], mode="markers+text",
                    name="🚨 Outlier",
                    marker=dict(size=20, color=CRIMSON, symbol="x", line=dict(color="white", width=2.5)),
                    text=[str(uid)[-4:] for uid in cf.index[mask_out]],
                    textposition="top center", textfont=dict(size=9, color=CRIMSON),
                    hovertemplate="<b>⚠️ OUTLIER …%{text}</b><br>PC1: %{x:.2f}<br>PC2: %{y:.2f}<extra>ANOMALY</extra>"))
                for i, uid in enumerate(cf.index[mask_out]):
                    xi, yi = X_pca[mask_out][i]
                    fig_db.add_shape(type="circle", x0=xi-0.35, y0=yi-0.35, x1=xi+0.35, y1=yi+0.35,
                        line=dict(color=CRIMSON, width=2, dash="dot"),
                        fillcolor="rgba(252,129,129,0.08)")
            apply_theme(fig_db, f"🔍 DBSCAN Outlier Detection — PCA Projection (eps=2.2)", height=480)
            fig_db.update_layout(xaxis_title=f"PC1 ({var[0]:.1f}% variance)",
                                 yaxis_title=f"PC2 ({var[1]:.1f}% variance)")
            st.plotly_chart(fig_db, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with dc2:
            st.markdown('<div class="glass-panel f4"><div class="panel-label">Cluster Feature Profiles</div>', unsafe_allow_html=True)
            for lbl in sorted(set(db_labels)):
                if lbl == -1:
                    st.markdown(f"""
                    <div style="border-radius:12px;padding:14px 16px;margin-bottom:12px;
                        background:rgba(252,129,129,0.05);border:1px solid rgba(252,129,129,0.15);
                        border-left:3px solid {CRIMSON};">
                        <div style="font-family:Clash Display,sans-serif;font-size:14px;font-weight:700;
                            color:{TEXT};margin-bottom:8px;">🚨 Outliers ({n_outliers} users)</div>
                        <div style="font-size:11px;color:{MUTED}">Users: {', '.join(['…'+str(u)[-4:] for u in cf.index[db_labels==-1]])}</div>
                        <div style="font-size:11px;color:{CRIMSON};margin-top:4px;font-family:Fira Code,monospace;">
                            Label: −1 · Anomalous behaviour</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    mask   = db_labels == lbl
                    ucount = int(mask.sum())
                    avg_s  = cf.loc[cf.index[mask], "TotalSteps"].mean()
                    avg_c  = cf.loc[cf.index[mask], "Calories"].mean()
                    tag    = "🏃 Active" if avg_s > 8000 else ("🚶 Moderate" if avg_s > 4000 else "🛋️ Sedentary")
                    st.markdown(f"""
                    <div style="border-radius:12px;padding:14px 16px;margin-bottom:12px;
                        background:rgba(52,211,153,0.05);border:1px solid rgba(52,211,153,0.15);
                        border-left:3px solid {TEAL};">
                        <div style="font-family:Clash Display,sans-serif;font-size:14px;font-weight:700;
                            color:{TEXT};margin-bottom:8px;">Cluster {lbl} · {ucount} users</div>
                        <div style="font-family:Fira Code,monospace;font-size:11px;color:{MUTED};line-height:1.9">
                            Avg Steps: <span style="color:{TEXT};font-weight:600">{avg_s:,.0f}</span><br>
                            Avg Calories: <span style="color:{TEXT};font-weight:600">{avg_c:,.0f}</span><br>
                            <span style="color:{TEAL}">{tag}</span>
                        </div>
                    </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if n_outliers > 0:
            with st.expander(f"📋  View {n_outliers} Outlier User Profiles"):
                st.dataframe(cf[cf["DBSCAN"]==-1][cluster_cols].round(2), use_container_width=True)

    except Exception as e:
        ui_warn(f"DBSCAN clustering skipped: {e}")

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: ACCURACY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Accuracy":
    mod_header("🎯", "SECTION 06 · ACCURACY", "Simulated Detection Accuracy — 90%+ Target",
               "Inject 10 known anomalies per signal, run detector, measure how many are caught. Validates 90%+ requirement.")

    if not st.session_state.files_loaded:
        ui_warn("Go to **Overview** tab first to upload CSV files and load data.")
        st.stop()

    master = st.session_state.master
    ui_info("10 known anomalies (extreme values) are injected into each signal. The detector runs and we measure how many it catches. This validates the 90%+ accuracy requirement.")

    if st.button("🎯  Run Accuracy Simulation (10 injected anomalies per signal)"):
        with st.spinner("Injecting anomalies and measuring detection rate…"):
            try:
                sim = simulate_accuracy(master, n_inject=10)
                st.session_state.sim_results    = sim
                st.session_state.simulation_done = True
                st.rerun()
            except Exception as e:
                st.error(f"Simulation error: {e}")

    if st.session_state.simulation_done and st.session_state.sim_results:
        sim     = st.session_state.sim_results
        overall = sim["Overall"]
        passed  = overall >= 90.0

        if passed:
            ui_success(f"Overall accuracy: {overall}% — ✅ MEETS 90%+ REQUIREMENT")
        else:
            ui_warn(f"Overall accuracy: {overall}% — below 90% target, adjust thresholds in sidebar")

        st.markdown("<hr class='v-div'>", unsafe_allow_html=True)

        # Accuracy cards
        st.markdown('<div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:20px;">', unsafe_allow_html=True)
        for signal in ["Heart Rate", "Steps", "Sleep"]:
            r   = sim[signal]
            acc = r["accuracy"]
            ok  = acc >= 90
            st.markdown(f"""
            <div class="acc-card {'acc-pass' if ok else 'acc-fail'}">
                <div style="font-size:2.2rem;font-weight:800;color:{'#34d399' if ok else '#fc8181'};
                    font-family:'Clash Display',sans-serif;line-height:1;">{acc}%</div>
                <div style="font-size:0.9rem;color:{TEXT};font-weight:600;margin:0.4rem 0">{signal}</div>
                <div style="font-size:0.78rem;color:{MUTED}">{r['detected']}/{r['injected']} detected</div>
                <div style="font-size:0.75rem;color:{'#34d399' if ok else '#fc8181'};
                    font-family:Fira Code,monospace;margin-top:6px">
                    {'✅ PASS' if ok else '⚠️ LOW'}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="acc-card acc-overall">
            <div style="font-size:2.2rem;font-weight:800;color:{'#fbbf24'};
                font-family:'Clash Display',sans-serif;line-height:1;">{overall}%</div>
            <div style="font-size:0.9rem;color:{TEXT};font-weight:600;margin:0.4rem 0">Overall</div>
            <div style="font-size:0.75rem;color:{'#34d399' if passed else '#fc8181'};
                font-family:Fira Code,monospace;margin-top:6px">
                {'✅ 90%+ ACHIEVED' if passed else '⚠️ BELOW TARGET'}</div>
        </div></div>""", unsafe_allow_html=True)

        st.markdown("<hr class='v-div'>", unsafe_allow_html=True)

        # Accuracy bar chart
        st.markdown('<div class="glass-panel f3"><div class="panel-label">Detection Accuracy vs 90% Target · Chart 5 of 5</div>', unsafe_allow_html=True)
        signals  = ["Heart Rate", "Steps", "Sleep"]
        accs     = [sim[s]["accuracy"] for s in signals]
        bar_cols = [TEAL if a >= 90 else CRIMSON for a in accs]

        fig_acc = go.Figure()
        fig_acc.add_trace(go.Bar(x=signals, y=accs, marker_color=bar_cols,
            marker_line=dict(width=0),
            text=[f"{a}%" for a in accs], textposition="outside",
            textfont=dict(color=TEXT, size=15, family="Clash Display, sans-serif"),
            hovertemplate="<b>%{x}</b><br>Accuracy: %{y}%<extra></extra>",
            name="Detection Accuracy", width=0.45))
        fig_acc.add_hline(y=90, line_dash="dash", line_color=ROSE, line_width=2.5,
                          annotation_text="90% Target", annotation_font_color=ROSE,
                          annotation_position="top right")
        # Goal band
        fig_acc.add_hrect(y0=90, y1=115, fillcolor="rgba(52,211,153,0.04)",
                          line_width=0, annotation_text="✅ Target Zone",
                          annotation_position="top left",
                          annotation_font_color=TEAL)
        apply_theme(fig_acc, "🎯 Simulated Anomaly Detection Accuracy", height=420)
        fig_acc.update_layout(yaxis_range=[0, 115], yaxis_title="Detection Accuracy (%)",
                              xaxis_title="Signal Type", showlegend=False)
        st.plotly_chart(fig_acc, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr class='v-div'>", unsafe_allow_html=True)

        # Gauge-style radial chart
        st.markdown('<div class="glass-panel f4"><div class="panel-label">Accuracy Gauge — Individual Signals</div>', unsafe_allow_html=True)
        gc1, gc2, gc3 = st.columns(3)
        for col, signal in zip([gc1, gc2, gc3], signals):
            with col:
                r = sim[signal]; acc = r["accuracy"]; ok = acc >= 90
                fig_g = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=acc,
                    number=dict(font=dict(color=TEAL if ok else CRIMSON, size=36,
                                          family="Clash Display, sans-serif"), suffix="%"),
                    title=dict(text=signal, font=dict(color=MUTED, size=13)),
                    gauge=dict(
                        axis=dict(range=[0, 100], tickfont=dict(color=DIM, size=9)),
                        bar=dict(color=TEAL if ok else CRIMSON, thickness=0.3),
                        bgcolor=DEEP,
                        borderwidth=0,
                        steps=[
                            dict(range=[0, 90],  color=LAYER),
                            dict(range=[90, 100], color="rgba(52,211,153,0.12)"),
                        ],
                        threshold=dict(line=dict(color=ROSE, width=3), value=90)
                    )
                ))
                fig_g.update_layout(height=220, paper_bgcolor=PAPER_BG,
                    font=dict(color=TEXT), margin=dict(l=20, r=20, t=30, b=10))
                st.plotly_chart(fig_g, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr class='v-div'>", unsafe_allow_html=True)

    # ── Milestone 3 Summary Checklist ─────────────────────────────────────────
    mod_header("✅", "MILESTONE 3 SUMMARY", "Completion Checklist",
               "All deliverables tracked — run each step to complete the milestone")

    all_done = st.session_state.anomaly_done and st.session_state.simulation_done
    checklist = [
        ("🚨", "Threshold Violations",  st.session_state.anomaly_done,    f"HR>{hr_high}/{hr_low}, Steps<{st_low}, Sleep<{sl_low}/<{sl_high}"),
        ("📉", "Residual-Based",         st.session_state.anomaly_done,    f"Rolling median ±{sigma:.0f}σ on all 3 signals"),
        ("🔍", "DBSCAN Outliers",        st.session_state.anomaly_done,    "Structural outliers via user clustering"),
        ("❤️", "HR Chart",               st.session_state.anomaly_done,    "Interactive Plotly · annotations + threshold lines"),
        ("💤", "Sleep Chart",            st.session_state.anomaly_done,    "Dual subplot · duration + residual bars"),
        ("🚶", "Steps Chart",            st.session_state.anomaly_done,    "Trend + alert bands + residual deviation"),
        ("🎯", "Accuracy Simulation",    st.session_state.simulation_done, "10 injected anomalies per signal · 90%+ target"),
    ]

    for icon, label, done, detail in checklist:
        dot = "✅" if done else "⬜"
        st.markdown(f"""
        <div class="chk-row">
            <span style="font-size:1.1rem">{dot}</span>
            <span style="font-size:0.88rem;font-weight:600;color:{TEXT};min-width:190px">{icon} {label}</span>
            <span style="font-size:0.8rem;color:{MUTED};font-family:Fira Code,monospace">{detail}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="term f3">
        <span class="hi">╔════════════════════════════════════════════╗</span><br>
        <span class="hi">║  FITPULSE · MILESTONE 3 · ANOMALY DETECTOR ║</span><br>
        <span class="hi">╚════════════════════════════════════════════╝</span><br><br>
        <span class="ok">✓</span>  <span class="hi">Dataset   </span>  35 users · 31 days · <span class="val">March–April 2016</span><br>
        <span class="ok">✓</span>  <span class="hi">Method 1  </span>  Threshold violations · HR / Steps / Sleep<br>
        <span class="ok">✓</span>  <span class="hi">Method 2  </span>  Residual ±<span class="val">{sigma:.0f}σ</span> rolling median baseline<br>
        <span class="ok">✓</span>  <span class="hi">Method 3  </span>  DBSCAN structural outliers · eps=<span class="val">2.2</span><br>
        <span class="ok">✓</span>  <span class="hi">Charts    </span>  5 interactive Plotly charts (HR, Sleep, Steps, PCA, Acc)<br>
        <span class="{'ok' if st.session_state.simulation_done else 'warn'}">{'✓' if st.session_state.simulation_done else '○'}</span>  <span class="hi">Accuracy  </span>  <span class="val">{'Target: 90%+ · ' + str(st.session_state.sim_results['Overall']) + '% achieved' if st.session_state.sim_results else 'Run simulation to validate'}</span><br><br>
        <span class="{'ok' if all_done else 'warn'}">{'STATUS: ALL SECTIONS COMPLETE ✓' if all_done else 'STATUS: PENDING — COMPLETE ALL STEPS ABOVE'}</span>
    </div>""", unsafe_allow_html=True)

    # Screenshots guide
    st.markdown(f"""
    <div class="glass-panel f4">
        <div class="panel-label">📸 Screenshots Required for Submission</div>
        <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:10px;font-size:0.82rem">
            <div style="background:rgba(252,129,129,0.05);border-radius:10px;padding:12px 14px;border:1px solid rgba(252,129,129,0.1)">
                <span style="color:{ROSE}">📸</span> <b>Chart 1</b> — Heart Rate with anomalies highlighted
            </div>
            <div style="background:rgba(252,129,129,0.05);border-radius:10px;padding:12px 14px;border:1px solid rgba(252,129,129,0.1)">
                <span style="color:{ROSE}">📸</span> <b>Chart 2</b> — Sleep pattern with alert bands
            </div>
            <div style="background:rgba(252,129,129,0.05);border-radius:10px;padding:12px 14px;border:1px solid rgba(252,129,129,0.1)">
                <span style="color:{ROSE}">📸</span> <b>Chart 3</b> — Step count trend with alert bands
            </div>
            <div style="background:rgba(252,129,129,0.05);border-radius:10px;padding:12px 14px;border:1px solid rgba(252,129,129,0.1)">
                <span style="color:{ROSE}">📸</span> <b>Chart 4</b> — DBSCAN outlier scatter (PCA)
            </div>
            <div style="background:rgba(252,129,129,0.05);border-radius:10px;padding:12px 14px;border:1px solid rgba(252,129,129,0.1);grid-column:1/-1">
                <span style="color:{ROSE}">📸</span> <b>Chart 5</b> — Accuracy bar chart (90%+ target line + gauges)
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-top:64px;padding:20px 0 12px;border-top:1px solid rgba(252,129,129,0.08);
    display:flex;align-items:center;justify-content:space-between;">
    <span style="font-family:'Fira Code',monospace;font-size:10px;color:{DIM};">FitPulse · Milestone 3 · Anomaly Detection</span>
    <span style="font-family:'Fira Code',monospace;font-size:10px;color:{DIM};">35 users · 2016 Fitbit Dataset</span>
</div>""", unsafe_allow_html=True)