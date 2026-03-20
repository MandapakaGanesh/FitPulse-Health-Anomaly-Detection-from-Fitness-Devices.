# =========================================================
# IMPORTS
# =========================================================
import time
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from preprocessing import preprocess_fitness_data, run_eda

@st.cache_data
def run_eda_cached(df_bytes):
    import io, pandas as pd
    df = pd.read_csv(io.BytesIO(df_bytes))
    return run_eda(df)


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="FitPulse Analytics",
    page_icon="📈",
    layout="wide"
)

# =========================================================
# CHART THEME
# =========================================================
CHART_BG      = "#060b18"
CHART_SURFACE = "#0c1528"
CHART_TEXT    = "#e2e8f0"
CHART_SUBTEXT = "#64748b"
CHART_ACCENT  = "#38bdf8"
CHART_ACCENT2 = "#a78bfa"
CHART_ACCENT3 = "#f472b6"
CHART_ACCENT4 = "#34d399"
PALETTE       = [CHART_ACCENT, CHART_ACCENT2, CHART_ACCENT3, CHART_ACCENT4,
                 "#fb923c", "#facc15", "#818cf8", "#f87171"]

def apply_dark_style(fig, ax):
    fig.patch.set_facecolor(CHART_BG)
    ax.set_facecolor(CHART_SURFACE)
    ax.tick_params(colors=CHART_SUBTEXT, labelsize=9)
    ax.xaxis.label.set_color(CHART_SUBTEXT)
    ax.yaxis.label.set_color(CHART_SUBTEXT)
    ax.title.set_color(CHART_TEXT)
    ax.title.set_fontsize(13)
    ax.title.set_fontweight("bold")
    for spine in ax.spines.values():
        spine.set_edgecolor((1, 1, 1, 0.08))
    ax.grid(True, color=(1, 1, 1, 0.05), linewidth=0.6, linestyle="--")
    fig.tight_layout()

def apply_dark_style_multi(fig, axes_list):
    fig.patch.set_facecolor(CHART_BG)
    for ax in axes_list:
        ax.set_facecolor(CHART_SURFACE)
        ax.tick_params(colors=CHART_SUBTEXT, labelsize=9)
        ax.xaxis.label.set_color(CHART_SUBTEXT)
        ax.yaxis.label.set_color(CHART_SUBTEXT)
        ax.title.set_color(CHART_TEXT)
        ax.title.set_fontsize(12)
        ax.title.set_fontweight("bold")
        for spine in ax.spines.values():
            spine.set_edgecolor((1, 1, 1, 0.08))
        ax.grid(True, color=(1, 1, 1, 0.05), linewidth=0.5, linestyle="--")
    fig.tight_layout(pad=2.5)

# =========================================================
# INFO TOGGLE HELPER
# =========================================================
def info_toggle(key, title, objective, insights):
    """Render a hover tooltip ⓘ button overlaid on top-right of chart wrapper."""
    st.markdown(f"""
    <style>
    #fp-wrap-{key} {{ position: relative; }}
    </style>
    <div class="fp-info-float" id="fp-float-{key}">
        <div class="fp-info-wrap" id="fp-info-{key}">
            <div class="fp-info-btn">ⓘ</div>
            <div class="fp-info-tooltip">
                <div class="fp-info-tooltip-title">{title}</div>
                <div class="fp-info-cols">
                    <div class="fp-info-col fp-info-col-obj">
                        <div class="fp-info-col-head"><span>🎯</span><span>Objective</span></div>
                        <div class="fp-info-col-body">{objective}</div>
                    </div>
                    <div class="fp-info-col fp-info-col-ins">
                        <div class="fp-info-col-head"><span>💡</span><span>What to Look For</span></div>
                        <div class="fp-info-col-body">{insights}</div>
                    </div>
                </div>
                <div class="fp-info-arrow"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)




# =========================================================
# PAGE ORDER & HELPERS
# =========================================================
PAGE_ORDER = ["Overview", "Preprocessing", "EDA"]

def go_to(page_name):
    """Navigate to a page by setting session state and rerunning."""
    st.session_state["current_page"] = PAGE_ORDER.index(page_name)
    st.rerun()

def render_step_indicator(current_page):
    steps = [
        ("1", "Overview"),
        ("2", "⚗️ Preprocessing"),
        ("3", "🧠 EDA"),
    ]
    current_idx = PAGE_ORDER.index(current_page)
    parts = ""
    for i, (num, label) in enumerate(steps):
        if i < current_idx:
            c_cls, l_cls, inner = "done", "done", "✓"
        elif i == current_idx:
            c_cls, l_cls, inner = "active", "active", num
        else:
            c_cls, l_cls, inner = "", "", num

        parts += f"""
        <div class="step-item">
            <div class="step-circle {c_cls}">{inner}</div>
            <span class="step-label {l_cls}">{label}</span>
        </div>"""
        if i < len(steps) - 1:
            conn = "done" if i < current_idx else ""
            parts += f'<div class="step-connector {conn}"></div>'

    st.markdown(f'<div class="step-indicator">{parts}</div>', unsafe_allow_html=True)

# =========================================================
# ALL CSS — single block
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800;900&family=DM+Sans:wght@400;500;600;700&display=swap');
* { font-family: 'DM Sans', sans-serif; }
h1, h2, .hero-title { font-family: 'Syne', sans-serif !important; }

/* ===== CSS Variables for cohesive theming ===== */
:root {
    --bg-base:      #060b18;
    --bg-mid:       #0c1528;
    --bg-surface:   #111d35;
    --accent-blue:  #38bdf8;
    --accent-indigo:#6366f1;
    --accent-purple:#a78bfa;
    --accent-green: #34d399;
    --text-primary: #e2e8f0;
    --text-muted:   #64748b;
}

/* ===== Rich layered background ===== */
.stApp {
    background-color: var(--bg-base);
    background-image:
        radial-gradient(ellipse 80% 60% at -10% 0%,
            rgba(56,189,248,0.13) 0%,
            transparent 65%),
        radial-gradient(ellipse 60% 70% at 110% 30%,
            rgba(99,102,241,0.14) 0%,
            transparent 60%),
        radial-gradient(ellipse 50% 40% at 5% 95%,
            rgba(167,139,250,0.09) 0%,
            transparent 55%),
        linear-gradient(rgba(56,189,248,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56,189,248,0.025) 1px, transparent 1px),
        linear-gradient(160deg, #080e1e 0%, #0a1628 45%, #06101f 100%);
    background-size:
        100% 100%,
        100% 100%,
        100% 100%,
        48px 48px,
        48px 48px,
        100% 100%;
    color: var(--text-primary);
    min-height: 100vh;
}

/* Thin glowing top border */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(56,189,248,0.6) 30%,
        rgba(99,102,241,0.8) 60%,
        transparent 100%);
    z-index: 9999;
    pointer-events: none;
}

/* Hide default multipage nav */
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebarNavItems"] { display: none !important; }
[data-testid="stSidebarNavSeparator"] { display: none !important; }

section[data-testid="stSidebar"] {
    background-color: var(--bg-base);
    background-image:
        radial-gradient(ellipse 120% 40% at 50% 0%,
            rgba(56,189,248,0.1) 0%,
            transparent 60%),
        linear-gradient(180deg, #07111f 0%, #050d1a 100%);
    border-right: 1px solid rgba(56,189,248,0.1) !important;
    box-shadow: 4px 0 32px rgba(0,0,0,0.5);
}

/* ===== Glass Card ===== */
.glass-card {
    background: rgba(255,255,255,0.035);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 30px;
    border: 1px solid rgba(56,189,248,0.12);
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.04) inset,
        0 12px 40px rgba(0,0,0,0.5),
        0 1px 0 rgba(255,255,255,0.06) inset;
    margin-bottom: 24px;
}

/* ===== KPI Cards ===== */
.kpi-card {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 18px;
    padding: 28px;
    border: 1px solid rgba(255,255,255,0.07);
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.03) inset,
        0 8px 32px rgba(0,0,0,0.45);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
}
.kpi-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 48px rgba(0,0,0,0.55), 0 0 0 1px rgba(56,189,248,0.15);
    border-color: rgba(56,189,248,0.2);
}
.kpi-title { font-size: 13px; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.65; font-weight: 600; }
.kpi-value { font-size: 38px; font-weight: 800; margin-top: 6px; }
.kpi-blue   { border-left: 5px solid #38bdf8; }
.kpi-purple { border-left: 5px solid #a78bfa; }
.kpi-pink   { border-left: 5px solid #f472b6; }
.kpi-green  { border-left: 5px solid #34d399; }

/* ===== EDA Banners ===== */
.eda-section-banner {
    background: linear-gradient(90deg, rgba(56,189,248,0.15) 0%, rgba(167,139,250,0.08) 100%);
    border-left: 4px solid #38bdf8;
    border-radius: 0 12px 12px 0;
    padding: 14px 20px;
    margin: 28px 0 16px 0;
    display: flex;
    align-items: center;
    gap: 12px;
}
.eda-section-banner .banner-icon { font-size: 22px; }
.eda-section-banner .banner-title { font-size: 17px; font-weight: 700; color: #e2e8f0; margin: 0; }
.eda-section-banner .banner-desc  { font-size: 12px; color: #94a3b8; margin: 2px 0 0 0; }

/* ===== Chart Wrapper ===== */
.chart-wrapper {
    background: rgba(6,11,24,0.75);
    backdrop-filter: blur(12px);
    border-radius: 18px;
    border: 1px solid rgba(56,189,248,0.1);
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5), 0 1px 0 rgba(255,255,255,0.04) inset;
}

/* ===== Hover Info Tooltip ===== */
.fp-info-float {
    display: flex;
    justify-content: flex-end;
    margin-top: 6px;
    margin-bottom: 4px;
    padding-right: 2px;
    position: relative;
    z-index: 200;
}
/* When inside a chart-wrapper, overlap onto the chart */
.chart-wrapper .fp-info-float {
    margin-top: -34px;
    margin-bottom: 10px;
}
.fp-info-wrap {
    position: relative;
    display: inline-flex;
    align-items: center;
}
.fp-info-btn {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: rgba(56,189,248,0.1);
    border: 1px solid rgba(56,189,248,0.3);
    color: #38bdf8;
    font-size: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
    user-select: none;
    flex-shrink: 0;
}
.fp-info-btn:hover {
    background: rgba(56,189,248,0.22);
    border-color: #38bdf8;
    box-shadow: 0 0 12px rgba(56,189,248,0.35);
    transform: scale(1.12);
}
.fp-info-tooltip {
    position: absolute;
    top: 34px;
    right: 0;
    width: 520px;
    max-width: 90vw;
    background: linear-gradient(135deg, #0c1830 0%, #091225 100%);
    border: 1px solid rgba(56,189,248,0.25);
    border-radius: 16px;
    padding: 18px 20px 16px 20px;
    box-shadow: 0 16px 48px rgba(0,0,0,0.7), 0 0 0 1px rgba(255,255,255,0.04) inset;
    opacity: 0;
    pointer-events: none;
    transform: translateY(-6px) scale(0.97);
    transition: opacity 0.22s ease, transform 0.22s cubic-bezier(0.34,1.56,0.64,1);
    z-index: 9999;
}
.fp-info-wrap:hover .fp-info-tooltip {
    opacity: 1;
    pointer-events: auto;
    transform: translateY(0) scale(1);
}
.fp-info-tooltip-title {
    font-size: 12px;
    font-weight: 800;
    color: #38bdf8;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(56,189,248,0.12);
}
.fp-info-cols {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}
.fp-info-col {
    border-radius: 10px;
    padding: 13px 14px;
}
.fp-info-col-obj {
    background: rgba(99,102,241,0.09);
    border: 1px solid rgba(99,102,241,0.2);
}
.fp-info-col-ins {
    background: rgba(52,211,153,0.07);
    border: 1px solid rgba(52,211,153,0.2);
}
.fp-info-col-head {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 8px;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.2px;
    text-transform: uppercase;
}
.fp-info-col-obj .fp-info-col-head { color: #818cf8; }
.fp-info-col-ins .fp-info-col-head { color: #34d399; }
.fp-info-col-body {
    font-size: 12px;
    color: #94a3b8;
    line-height: 1.65;
}
.fp-info-arrow {
    position: absolute;
    top: -7px;
    right: 8px;
    width: 13px;
    height: 13px;
    background: #0c1830;
    border-top: 1px solid rgba(56,189,248,0.25);
    border-left: 1px solid rgba(56,189,248,0.25);
    transform: rotate(45deg);
    border-radius: 2px 0 0 0;
}

/* ===== Insight Pill ===== */
.insight-pill {
    display: inline-block;
    background: rgba(56,189,248,0.15);
    border: 1px solid rgba(56,189,248,0.3);
    color: #7dd3fc;
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 12px;
    font-weight: 600;
    margin: 4px 4px 4px 0;
}

/* ===== Date Badge ===== */
.date-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(52,211,153,0.12);
    border: 1px solid rgba(52,211,153,0.25);
    color: #6ee7b7;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 15px;
    font-weight: 600;
    margin: 4px 0;
}

/* ===== Divider ===== */
.eda-divider {
    height: 1px;
    background: linear-gradient(90deg, rgba(56,189,248,0.3), rgba(167,139,250,0.1), transparent);
    margin: 32px 0;
    border: none;
}

/* ===== Metrics ===== */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.08);
    padding: 24px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0px 8px 24px rgba(0,0,0,0.30);
    transition: all 0.3s ease;
}
[data-testid="metric-container"]:hover { transform: translateY(-6px); }

/* ===== DataFrame ===== */
[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.05);
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.10);
}

/* ===== File Uploader — Rich Drop Zone ===== */
[data-testid="stFileUploader"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
[data-testid="stFileUploader"] > div {
    background: rgba(6,11,24,0.7) !important;
    border: 2px dashed rgba(56,189,248,0.25) !important;
    border-radius: 20px !important;
    transition: all 0.3s ease !important;
    padding: 0 !important;
}
[data-testid="stFileUploader"] > div:hover {
    border-color: rgba(56,189,248,0.6) !important;
    background: rgba(56,189,248,0.04) !important;
    box-shadow: 0 0 40px rgba(56,189,248,0.1), inset 0 0 40px rgba(56,189,248,0.03) !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
    border: none !important;
    padding: 40px 20px !important;
    text-align: center !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] {
    color: #64748b !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] span {
    font-size: 14px !important;
    color: #94a3b8 !important;
}
/* Browse button */
[data-testid="stFileUploader"] button {
    background: linear-gradient(135deg, rgba(56,189,248,0.15), rgba(99,102,241,0.15)) !important;
    border: 1px solid rgba(56,189,248,0.3) !important;
    color: #38bdf8 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 8px 20px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stFileUploader"] button:hover {
    background: linear-gradient(135deg, rgba(56,189,248,0.25), rgba(99,102,241,0.25)) !important;
    border-color: rgba(56,189,248,0.6) !important;
    box-shadow: 0 4px 16px rgba(56,189,248,0.25) !important;
    transform: translateY(-1px) !important;
}
/* Uploaded file chip */
[data-testid="stFileUploaderFile"] {
    background: rgba(52,211,153,0.06) !important;
    border: 1px solid rgba(52,211,153,0.2) !important;
    border-radius: 12px !important;
    padding: 10px 16px !important;
    color: #6ee7b7 !important;
}

h1 { font-size: 40px; font-weight: 800; font-family: 'Syne', sans-serif !important; }

/* ===== Hero animations ===== */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulseBorder {
    0%, 100% { box-shadow: 0 0 0 0 rgba(56,189,248,0); }
    50%       { box-shadow: 0 0 0 6px rgba(56,189,248,0.08); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position: 200% center; }
}
@keyframes floatOrb {
    0%, 100% { transform: translateY(0px) scale(1); }
    50%       { transform: translateY(-14px) scale(1.04); }
}
.hero-animate { animation: fadeUp 0.7s ease both; }
.hero-animate-2 { animation: fadeUp 0.7s ease 0.15s both; }
.hero-animate-3 { animation: fadeUp 0.7s ease 0.3s both; }

/* ===== Hero title gradient text ===== */
.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 42px !important;
    font-weight: 900 !important;
    line-height: 1.15 !important;
    background: linear-gradient(135deg, #e2e8f0 0%, #38bdf8 50%, #a78bfa 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s linear infinite, fadeUp 0.7s ease both;
    margin: 0 0 14px 0 !important;
}

/* ===== Upload drop zone — bold ===== */
[data-testid="stFileUploader"] { background: transparent !important; border: none !important; padding: 0 !important; }
[data-testid="stFileUploader"] > div {
    background:
        radial-gradient(ellipse 60% 80% at 50% 110%, rgba(56,189,248,0.07) 0%, transparent 65%),
        rgba(6,11,24,0.65) !important;
    border: 2px dashed rgba(56,189,248,0.35) !important;
    border-radius: 22px !important;
    transition: all 0.35s cubic-bezier(0.34,1.56,0.64,1) !important;
    animation: pulseBorder 3.5s ease-in-out infinite !important;
}
[data-testid="stFileUploader"] > div:hover {
    border-color: #38bdf8 !important;
    background:
        radial-gradient(ellipse 60% 80% at 50% 110%, rgba(56,189,248,0.14) 0%, transparent 65%),
        rgba(8,18,36,0.8) !important;
    box-shadow:
        0 0 0 4px rgba(56,189,248,0.08),
        0 20px 60px rgba(56,189,248,0.15),
        inset 0 0 40px rgba(56,189,248,0.05) !important;
    transform: translateY(-2px) !important;
    animation: none !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
    border: none !important;
    padding: 52px 40px !important;
    text-align: center !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] span {
    font-size: 15px !important;
    color: #475569 !important;
    font-weight: 500 !important;
}
[data-testid="stFileUploader"] button {
    background: linear-gradient(135deg, #38bdf8 0%, #6366f1 100%) !important;
    border: none !important; color: white !important;
    border-radius: 12px !important; font-weight: 700 !important;
    font-size: 14px !important; padding: 12px 30px !important;
    box-shadow: 0 4px 24px rgba(56,189,248,0.4), 0 1px 0 rgba(255,255,255,0.15) inset !important;
    transition: all 0.25s ease !important; letter-spacing: 0.3px !important;
    margin-top: 6px !important;
}
[data-testid="stFileUploader"] button:hover {
    box-shadow: 0 10px 36px rgba(56,189,248,0.6) !important;
    transform: translateY(-3px) scale(1.04) !important;
}
[data-testid="stFileUploader"] button:active {
    transform: translateY(0) scale(0.98) !important;
}
[data-testid="stFileUploaderFile"] {
    background: rgba(52,211,153,0.05) !important;
    border: 1px solid rgba(52,211,153,0.2) !important;
    border-radius: 12px !important; color: #6ee7b7 !important;
}

/* ===== Primary Button Global Style ===== */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #38bdf8 0%, #6366f1 100%);
    border: none;
    border-radius: 12px;
    color: white;
    font-weight: 700;
    font-size: 14px;
    letter-spacing: 0.3px;
    padding: 14px 24px;
    box-shadow: 0 4px 20px rgba(56,189,248,0.3);
    transition: all 0.25s ease;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #7dd3fc 0%, #818cf8 100%);
    box-shadow: 0 8px 32px rgba(56,189,248,0.5);
    transform: translateY(-2px) scale(1.02);
    color: white;
}
div[data-testid="stButton"] > button[kind="primary"]:active {
    transform: translateY(0px) scale(0.98);
    box-shadow: 0 3px 12px rgba(56,189,248,0.25);
}

/* ===== Step Indicator ===== */
.step-indicator {
    display: flex;
    align-items: center;
    margin: 0 0 28px 0;
    padding: 18px 24px;
    background: rgba(6,11,24,0.6);
    border: 1px solid rgba(56,189,248,0.1);
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4), 0 1px 0 rgba(255,255,255,0.04) inset;
    backdrop-filter: blur(12px);
}
.step-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    flex: 1;
}
.step-circle {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 700;
    border: 2px solid rgba(255,255,255,0.12);
    background: rgba(255,255,255,0.06);
    color: #64748b;
}
.step-circle.done   { background: rgba(52,211,153,0.2); border-color: #34d399; color: #34d399; }
.step-circle.active { background: linear-gradient(135deg,#38bdf8,#6366f1); border-color: #38bdf8; color: white; box-shadow: 0 0 16px rgba(56,189,248,0.4); }
.step-label { font-size: 11px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; white-space: nowrap; }
.step-label.active { color: #e2e8f0; }
.step-label.done   { color: #34d399; }
.step-connector { height: 2px; flex: 1; background: rgba(255,255,255,0.08); margin-bottom: 18px; }
.step-connector.done { background: #34d399; }

/* ===== Sidebar nav cards (visual only) ===== */
.nav-card {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 13px 16px;
    margin-bottom: 6px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.05);
    background: rgba(6,11,24,0.5);
    color: #64748b;
    font-size: 13px;
    transition: all 0.2s ease;
}
.nav-card.active {
    background: rgba(56,189,248,0.08);
    border-color: rgba(56,189,248,0.25);
    color: #e2e8f0;
    font-weight: 700;
    box-shadow: 0 0 20px rgba(56,189,248,0.08);
}
.nav-card-dot {
    width: 7px; height: 7px;
    background: #38bdf8;
    border-radius: 50%;
    box-shadow: 0 0 8px #38bdf8;
    margin-left: auto;
}
.nav-card-num {
    width: 24px; height: 24px;
    border-radius: 6px;
    background: rgba(255,255,255,0.08);
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 700; color: #94a3b8;
    flex-shrink: 0;
}
.nav-card.active .nav-card-num {
    background: rgba(56,189,248,0.2);
    color: #38bdf8;
}

/* ===== Sidebar brand ===== */
.sidebar-brand {
    text-align: center;
    padding: 20px 10px 22px 10px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 18px;
}
.brand-name { font-size: 18px; font-weight: 800; color: #e2e8f0; letter-spacing: 0.5px; }
.brand-sub  { font-size: 10px; color: #475569; letter-spacing: 1.5px; text-transform: uppercase; margin-top: 3px; }

/* ===== Next Button Banner ===== */
.next-banner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(6,11,24,0.7);
    border: 1px solid rgba(56,189,248,0.18);
    border-radius: 16px;
    padding: 22px 28px;
    margin-top: 40px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4), 0 1px 0 rgba(56,189,248,0.06) inset;
    backdrop-filter: blur(12px);
}
.next-banner:hover {
    background: rgba(56,189,248,0.07);
    border-color: rgba(56,189,248,0.4);
    box-shadow: 0 8px 40px rgba(56,189,248,0.18), 0 0 0 1px rgba(56,189,248,0.12);
    transform: translateY(-2px);
}
.next-banner-text .next-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #38bdf8;
    font-weight: 700;
    margin: 0;
}
.next-banner-text .next-title {
    font-size: 20px;
    font-weight: 800;
    color: #e2e8f0;
    margin: 5px 0 0 0;
    letter-spacing: -0.3px;
}
.next-banner-text .next-desc {
    font-size: 12px;
    color: #64748b;
    margin: 5px 0 0 0;
    line-height: 1.5;
}

/* ===== Styled Next Streamlit Buttons ===== */
div[data-testid="stButton"]:has(button[kind="primary"]).next-btn-wrap > button,
div[data-testid="stButton"] > button[key="next_overview"],
div[data-testid="stButton"] > button[key="next_pre"] {
    width: 100%;
}

/* Target next buttons by key via attribute selectors */
button[kind="primaryFormSubmit"] { display: none; }

div.next-btn-container div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #38bdf8 0%, #6366f1 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 16px 32px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0.4px !important;
    box-shadow: 0 4px 24px rgba(56,189,248,0.35) !important;
    transition: all 0.25s ease !important;
    cursor: pointer !important;
    width: 100% !important;
    margin-top: 4px !important;
}
div.next-btn-container div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #7dd3fc 0%, #818cf8 100%) !important;
    box-shadow: 0 8px 36px rgba(56,189,248,0.55) !important;
    transform: translateY(-3px) scale(1.02) !important;
    color: white !important;
}
div.next-btn-container div[data-testid="stButton"] > button:active {
    transform: translateY(0px) scale(0.98) !important;
    box-shadow: 0 3px 12px rgba(56,189,248,0.3) !important;
}
@media (max-width: 768px) {
    .kpi-card { padding: 18px !important; }
    .kpi-value { font-size: 28px !important; }
    .glass-card { padding: 20px !important; border-radius: 16px !important; }
    .step-indicator { padding: 12px 14px !important; }
    .step-label { font-size: 9px !important; }
    .next-banner { padding: 16px 18px !important; }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
# ── Home button — always top of sidebar ──────────────────
st.sidebar.markdown("""
<style>
.home-btn-outer > div > button {
    background: linear-gradient(135deg,
        rgba(56,189,248,0.12), rgba(99,102,241,0.08)) !important;
    border: 1px solid rgba(56,189,248,0.25) !important;
    color: #38bdf8 !important;
    border-radius: 10px !important;
    font-size: 12px !important; font-weight: 600 !important;
    width: 100% !important; padding: 9px 14px !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.3px !important;
}
.home-btn-outer > div > button:hover {
    background: linear-gradient(135deg,
        rgba(56,189,248,0.22), rgba(99,102,241,0.15)) !important;
    border-color: #38bdf8 !important;
    box-shadow: 0 0 18px rgba(56,189,248,0.25) !important;
}
</style>
<div class="home-btn-outer">
""", unsafe_allow_html=True)
if st.sidebar.button("🏠  Back to Home", key="main_home_btn"):
    st.switch_page("Home.py")
st.sidebar.markdown("</div>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<hr style='border:none;border-top:1px solid rgba(56,189,248,0.08);"
    "margin:0 0 14px;'>",
    unsafe_allow_html=True
)

# Branding
st.sidebar.markdown("""
<div class="sidebar-brand">
    <div style="margin-bottom:10px;">
        <svg width="50" height="50" viewBox="0 0 50 50" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="50" height="50" rx="13" fill="url(#g1)"/>
            <polyline points="7,25 15,25 19,13 23,37 27,19 31,29 35,25 43,25"
                stroke="white" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
            <defs>
                <linearGradient id="g1" x1="0" y1="0" x2="50" y2="50" gradientUnits="userSpaceOnUse">
                    <stop offset="0%" stop-color="#38bdf8"/>
                    <stop offset="100%" stop-color="#6366f1"/>
                </linearGradient>
            </defs>
        </svg>
    </div>
    <div class="brand-name">FitPulse</div>
    <div class="brand-sub">Analytics Dashboard</div>
</div>
""", unsafe_allow_html=True)

# Navigation — use session state index to control the radio
if "current_page" not in st.session_state:
    st.session_state["current_page"] = 0

nav_labels = ["Overview", "Preprocessing", "EDA"]
nav_icons  = ["🗂️", "⚗️", "🧠"]
nav_descs  = ["Dataset summary & preview", "Transform & clean data", "Explore deep insights"]

# The actual functional widget (hidden label)
selected = st.sidebar.radio(
    "nav",
    nav_labels,
    index=st.session_state["current_page"],
    label_visibility="collapsed"
)
# Keep session state in sync when user clicks the radio directly
st.session_state["current_page"] = nav_labels.index(selected)
page = selected

# Decorative nav cards below (visual feedback only)
for i, (label, icon, desc) in enumerate(zip(nav_labels, nav_icons, nav_descs)):
    is_active = label == page
    card_cls  = "active" if is_active else ""
    dot_html  = '<span class="nav-card-dot"></span>' if is_active else ""
    st.sidebar.markdown(f"""
    <div class="nav-card {card_cls}">
        <span class="nav-card-num">{i+1}</span>
        <span style="flex:1;">
            <span style="display:block;">{icon} {label}</span>
            <span style="font-size:11px; color:#475569; font-weight:400;">{desc}</span>
        </span>
        {dot_html}
    </div>
    """, unsafe_allow_html=True)

# How-to tip card
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="background:rgba(56,189,248,0.07);border:1px solid rgba(56,189,248,0.18);
border-radius:12px;padding:14px 16px;color:#7dd3fc;font-size:12px;line-height:1.7;">
    <strong style="color:#38bdf8;">💡 How to use</strong><br>
    1. Upload a CSV file<br>
    2. Run Preprocessing<br>
    3. Explore EDA insights
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
compact = st.sidebar.checkbox("⊞  Compact Mode", value=False)
if compact:
    st.sidebar.markdown(
        '<style>section[data-testid="stSidebar"] .nav-card { padding:8px 12px !important; font-size:12px !important; }'
        '.sidebar-brand { padding:14px 10px 14px 10px !important; }'
        '.brand-name { font-size:15px !important; }</style>',
        unsafe_allow_html=True
    )

st.sidebar.markdown("<div style='margin-top:8px;'>", unsafe_allow_html=True)
if st.sidebar.button("🔄  Reset Dashboard", use_container_width=True):
    st.session_state.clear()
    st.rerun()
st.sidebar.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="margin-top:16px;color:#334155;font-size:11px;text-align:center;letter-spacing:0.3px;">
    FitPulse Analytics · v1.0
</div>
""", unsafe_allow_html=True)

# =========================================================
# HERO — bold landing
# =========================================================
st.markdown(
    '<div style="position:relative;overflow:hidden;border-radius:28px;padding:40px 40px 36px 40px;margin-bottom:20px;'
    'background:radial-gradient(ellipse 70% 80% at 10% 0%,rgba(56,189,248,0.18) 0%,transparent 60%),'
    'radial-gradient(ellipse 50% 60% at 90% 100%,rgba(99,102,241,0.18) 0%,transparent 60%),'
    'linear-gradient(160deg,#09111f 0%,#070e1c 100%);'
    'border:1px solid rgba(56,189,248,0.18);box-shadow:0 24px 80px rgba(0,0,0,0.6),0 1px 0 rgba(255,255,255,0.05) inset;">'
    '<div style="position:absolute;top:-60px;right:-60px;width:280px;height:280px;border-radius:50%;'
    'background:radial-gradient(circle,rgba(99,102,241,0.15) 0%,transparent 70%);pointer-events:none;"></div>'
    '<div style="position:absolute;inset:0;border-radius:28px;overflow:hidden;'
    'background-image:linear-gradient(rgba(56,189,248,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(56,189,248,0.04) 1px,transparent 1px);'
    'background-size:40px 40px;pointer-events:none;opacity:0.6;"></div>'
    '<div style="margin-bottom:20px;">'
    '<span style="display:inline-flex;align-items:center;gap:7px;background:rgba(56,189,248,0.1);'
    'border:1px solid rgba(56,189,248,0.25);border-radius:999px;padding:5px 14px 5px 10px;'
    'font-size:11px;font-weight:700;letter-spacing:1.2px;color:#38bdf8;text-transform:uppercase;">'
    '<span style="width:6px;height:6px;border-radius:50%;background:#38bdf8;box-shadow:0 0 8px #38bdf8;display:inline-block;"></span>'
    'Fitness Analytics Platform</span></div>'
    '<h1 style="font-family:Syne,sans-serif;font-size:52px;font-weight:900;line-height:1.1;'
    'background:linear-gradient(135deg,#ffffff 0%,#93c5fd 45%,#a78bfa 100%);background-size:200% auto;'
    '-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;'
    'margin:0 0 16px 0;max-width:680px;">FitPulse<br>Analytics</h1>'
    '<p style="font-size:17px;color:#64748b;margin:0 0 32px 0;line-height:1.7;max-width:520px;">'
    'Transform raw fitness data into actionable insights.<br>Upload &middot; Clean &middot; Explore &mdash; in three steps.</p>'
    '<div style="display:flex;gap:10px;flex-wrap:wrap;">'
    '<div style="display:flex;align-items:center;gap:6px;background:rgba(255,255,255,0.04);'
    'border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:7px 14px;font-size:12px;color:#94a3b8;">'
    '<span style="color:#38bdf8;">&#9889;</span> Smart Preprocessing</div>'
    '<div style="display:flex;align-items:center;gap:6px;background:rgba(255,255,255,0.04);'
    'border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:7px 14px;font-size:12px;color:#94a3b8;">'
    '<span style="color:#a78bfa;">&#128202;</span> Visual EDA</div>'
    '<div style="display:flex;align-items:center;gap:6px;background:rgba(255,255,255,0.04);'
    'border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:7px 14px;font-size:12px;color:#94a3b8;">'
    '<span style="color:#34d399;">&#128190;</span> Export Cleaned CSV</div>'
    '</div></div>',
    unsafe_allow_html=True
)

# =========================================================
# UPLOAD — bold drop zone
# =========================================================
st.markdown(
    '<div style="display:flex;align-items:center;gap:10px;font-size:13px;color:#94a3b8;margin:0 0 8px 2px;">'
    '<span style="font-size:18px;">📁</span>'
    '<span>Upload your <strong style="color:#e2e8f0;">Fitness CSV dataset</strong> to start analysis'
    ' &nbsp;·&nbsp; <span style="color:#475569;">CSV / XLSX · Max 200MB · Works on mobile</span></span>'
    '</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">'
    '<div style="height:1px;flex:1;background:linear-gradient(90deg,rgba(56,189,248,0.3),transparent);"></div>'
    '<span style="font-size:11px;font-weight:700;color:#334155;letter-spacing:2px;text-transform:uppercase;">Drop Zone</span>'
    '<div style="height:1px;flex:1;background:linear-gradient(270deg,rgba(56,189,248,0.3),transparent);"></div>'
    '</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Drop your CSV or Excel file here, or click Browse",
    type=None,
    label_visibility="collapsed",
    help="Tap 'Browse files' → select your CSV or Excel file from Files / Downloads / Google Drive"
)

# Python-side validation (type=None allows all files so mobile browsers don't filter)
if uploaded_file is not None:
    _name = uploaded_file.name.lower()
    if not (_name.endswith(".csv") or _name.endswith(".txt") or _name.endswith(".xlsx") or _name.endswith(".xls")):
        st.error(f"❌ **{uploaded_file.name}** is not supported. Please upload a `.csv` or `.xlsx` file.")
        uploaded_file = None

# ── Post-upload file info card ──
if uploaded_file is not None:
    file_size_kb = round(uploaded_file.size / 1024, 1)
    file_size_str = f"{file_size_kb} KB" if file_size_kb < 1024 else f"{round(file_size_kb/1024,2)} MB"
    st.markdown(f"""
    <div style="
        display:flex; align-items:center; gap:16px;
        background: linear-gradient(90deg, rgba(52,211,153,0.07), rgba(52,211,153,0.03));
        border: 1px solid rgba(52,211,153,0.22);
        border-radius: 16px; padding: 16px 22px; margin: 10px 0 20px 0;
    ">
        <div style="
            width:42px;height:42px;border-radius:12px;flex-shrink:0;
            background:rgba(52,211,153,0.15);border:1px solid rgba(52,211,153,0.3);
            display:flex;align-items:center;justify-content:center;font-size:20px;
        ">✅</div>
        <div style="flex:1;">
            <div style="font-size:14px;font-weight:700;color:#6ee7b7;margin-bottom:3px;">File Ready</div>
            <div style="font-size:12px;color:#475569;">
                <strong style="color:#94a3b8;">{uploaded_file.name}</strong>
                &nbsp;·&nbsp;{file_size_str}
            </div>
        </div>
        <span style="
            background:rgba(52,211,153,0.12);border:1px solid rgba(52,211,153,0.25);
            border-radius:8px;padding:5px 12px;font-size:11px;
            font-weight:800;color:#34d399;letter-spacing:1px;
        ">{uploaded_file.name.split(".")[-1].upper()}</span>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# MAIN APPLICATION
# =========================================================
if uploaded_file is not None:

    # Reset session if new file uploaded
    if "last_file" not in st.session_state or st.session_state.last_file != uploaded_file.name:
        st.session_state.preprocessed = False
        st.session_state.eda_done     = False
        st.session_state.last_file    = uploaded_file.name

    uploaded_file.seek(0)
    _fname = uploaded_file.name.lower()
    if _fname.endswith(".xlsx") or _fname.endswith(".xls"):
        try:
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        except Exception as _e:
            st.error(f"❌ Could not read Excel file: {_e}")
            st.stop()
    else:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as _e:
            st.error(f"❌ Could not read CSV file: {_e}")
            st.stop()

    # ==========================================================
    # OVERVIEW
    # ==========================================================
    if page == "Overview":

        render_step_indicator("Overview")
        st.markdown("## Dataset Overview")

        total_nulls = int(df.isnull().sum().sum())
        num_cols    = df.select_dtypes(include="number").shape[1]
        cat_cols    = df.select_dtypes(exclude="number").shape[1]

        col1, col2, col3, col4, col5 = st.columns(5)
        kpis = [
            (col1, "kpi-blue",   "Rows",               f"{df.shape[0]:,}"),
            (col2, "kpi-purple", "Columns",             f"{df.shape[1]:,}"),
            (col3, "kpi-pink",   "Missing Values",      f"{total_nulls:,}"),
            (col4, "kpi-green",  "Numeric Columns",     f"{num_cols:,}"),
            (col5, "kpi-blue",   "Categorical Columns", f"{cat_cols:,}"),
        ]
        for col, cls, title, val in kpis:
            with col:
                st.markdown(f"""
                <div class="kpi-card {cls}" style="padding:20px 16px;">
                    <div class="kpi-title">{title}</div>
                    <div class="kpi-value" style="font-size:30px;">{val}</div>
                </div>
                """, unsafe_allow_html=True)

        # Smart warning for tiny datasets
        if df.shape[0] < 20:
            st.warning("⚠️ Dataset is very small (< 20 rows). Insights may not be reliable.")

        # Dataset Summary Card
        memory_mb = df.memory_usage(deep=True).sum() / (1024**2)
        null_pct  = (total_nulls / (df.shape[0] * df.shape[1]) * 100) if df.shape[0] > 0 else 0
        st.markdown(f"""
        <div class="glass-card" style="padding:20px 24px;margin-top:20px;">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
                <span style="font-size:15px;font-weight:800;color:#e2e8f0;">📋 Dataset Summary</span>
                <span style="font-size:11px;color:#475569;background:rgba(56,189,248,0.08);
                border:1px solid rgba(56,189,248,0.15);border-radius:6px;padding:2px 10px;
                font-weight:600;letter-spacing:0.5px;">{df.shape[0]:,} rows × {df.shape[1]} cols</span>
            </div>
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;">
                <div style="background:rgba(56,189,248,0.06);border:1px solid rgba(56,189,248,0.12);
                border-radius:10px;padding:12px 14px;">
                    <div style="font-size:10px;color:#38bdf8;font-weight:700;letter-spacing:1px;text-transform:uppercase;">Records</div>
                    <div style="font-size:20px;font-weight:800;color:#e2e8f0;margin-top:4px;">{df.shape[0]:,}</div>
                </div>
                <div style="background:rgba(167,139,250,0.06);border:1px solid rgba(167,139,250,0.12);
                border-radius:10px;padding:12px 14px;">
                    <div style="font-size:10px;color:#a78bfa;font-weight:700;letter-spacing:1px;text-transform:uppercase;">Features</div>
                    <div style="font-size:20px;font-weight:800;color:#e2e8f0;margin-top:4px;">{df.shape[1]}</div>
                </div>
                <div style="background:rgba(52,211,153,0.06);border:1px solid rgba(52,211,153,0.12);
                border-radius:10px;padding:12px 14px;">
                    <div style="font-size:10px;color:#34d399;font-weight:700;letter-spacing:1px;text-transform:uppercase;">Memory</div>
                    <div style="font-size:20px;font-weight:800;color:#e2e8f0;margin-top:4px;">{memory_mb:.1f} MB</div>
                </div>
                <div style="background:rgba(244,114,182,0.06);border:1px solid rgba(244,114,182,0.12);
                border-radius:10px;padding:12px 14px;">
                    <div style="font-size:10px;color:#f472b6;font-weight:700;letter-spacing:1px;text-transform:uppercase;">Null %</div>
                    <div style="font-size:20px;font-weight:800;color:#e2e8f0;margin-top:4px;">{null_pct:.1f}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Sample Data + Column Stats
        tab1, tab2 = st.tabs(["📄 Sample Data", "📊 Column Statistics"])
        with tab1:
            st.dataframe(df.head(10), use_container_width=True)
        with tab2:
            st.dataframe(df.describe().T.style.format("{:.2f}"), use_container_width=True)

        # Next button banner
        st.markdown("""
        <div class="next-banner">
            <div class="next-banner-text">
                <p class="next-label">✦ Up Next · Step 2 of 3</p>
                <p class="next-title">⚗️ Preprocessing</p>
                <p class="next-desc">Clean your data — handle nulls, fix types &amp; interpolate missing values</p>
            </div>
            <div style="font-size:32px; opacity:0.3;">→</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class='next-btn-container'>
        <style>
        div.next-btn-container + div[data-testid="stButton"] > button,
        div[data-testid="stButton"]:nth-of-type(2) > button {
            background: linear-gradient(135deg, #38bdf8, #6366f1) !important;
            color: white !important; border: none !important;
            border-radius: 14px !important; padding: 16px 32px !important;
            font-size: 15px !important; font-weight: 700 !important;
            box-shadow: 0 4px 24px rgba(56,189,248,0.35) !important;
            width: 100% !important; transition: all 0.25s ease !important;
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("Continue to Preprocessing  ➜", key="next_overview", type="primary", use_container_width=True):
            go_to("Preprocessing")
        st.markdown("</div>", unsafe_allow_html=True)

    # ==========================================================
    # PREPROCESSING
    # ==========================================================
    elif page == "Preprocessing":

        render_step_indicator("Preprocessing")
        st.markdown("## Data Cleaning Pipeline")

        if "preprocessed" not in st.session_state:
            st.session_state.preprocessed = False

        if st.button("⚗️ Run Preprocessing", type="primary"):

            pipeline_steps = [
                ("🗓️ Converting Date column to datetime",      "✔ Converted Date column to datetime."),
                ("🔃 Sorting dataset by User_ID and Date",     "✔ Sorted dataset by User_ID and Date."),
                ("📐 Applying user-wise linear interpolation", "✔ Applied user-wise linear interpolation."),
                ("🔁 Handling boundary nulls (ffill/bfill)",   "✔ Handled boundary nulls using forward/backward fill."),
                ("🏋️ Filling missing Workout_Type values",     "✔ Filled missing Workout_Type with 'No Workout'."),
            ]

            step_placeholders = []
            for label, _ in pipeline_steps:
                ph = st.empty()
                ph.markdown(f"""
                <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);
                border-radius:10px;padding:12px 18px;margin-bottom:8px;color:#94a3b8;font-size:14px;">
                    ⏳ &nbsp; {label}...
                </div>""", unsafe_allow_html=True)
                step_placeholders.append(ph)

            progress_bar = st.progress(0, text="Running pipeline...")
            cleaned_df, steps, report = preprocess_fitness_data(df.copy())

            for i, (ph, (_, done_label)) in enumerate(zip(step_placeholders, pipeline_steps)):
                time.sleep(0.5)
                progress_bar.progress(
                    (i + 1) / len(pipeline_steps),
                    text=f"Step {i+1}/{len(pipeline_steps)} — {done_label}"
                )
                ph.markdown(f"""
                <div style="background:linear-gradient(90deg,rgba(52,211,153,0.12),rgba(52,211,153,0.04));
                border:1px solid rgba(52,211,153,0.35);border-radius:10px;padding:12px 18px;
                margin-bottom:8px;color:#6ee7b7;font-size:14px;font-weight:600;">
                    ✅ &nbsp; {done_label}
                </div>""", unsafe_allow_html=True)

            st.session_state.cleaned_df  = cleaned_df
            st.session_state.steps       = steps
            st.session_state.report      = report
            st.session_state.preprocessed = True

        if st.session_state.preprocessed:

            st.success("✅ Preprocessing Completed Successfully")

            # Data Quality Report
            orig_rows    = df.shape[0]
            clean_rows   = st.session_state.cleaned_df.shape[0]
            rows_removed = orig_rows - clean_rows
            nulls_before = int(st.session_state.report["nulls_before"].sum())
            nulls_after  = int(st.session_state.report["nulls_after"].sum())
            nulls_fixed  = nulls_before - nulls_after

            st.markdown("""
            <div style="background:rgba(52,211,153,0.05);border:1px solid rgba(52,211,153,0.15);
            border-radius:16px;padding:18px 22px;margin:16px 0;">
                <div style="font-size:13px;font-weight:800;color:#34d399;letter-spacing:0.5px;margin-bottom:12px;">
                    📊 Data Quality Report
                </div>
            </div>
            """, unsafe_allow_html=True)
            qc1, qc2, qc3, qc4 = st.columns(4)
            for col_w, label, val, delta, good in [
                (qc1, "Original Rows",    orig_rows,    None,           True),
                (qc2, "Rows After Clean", clean_rows,   None,           True),
                (qc3, "Rows Removed",     rows_removed, None,           rows_removed == 0),
                (qc4, "Nulls Fixed",      nulls_fixed,  f"/{nulls_before} total", True),
            ]:
                with col_w:
                    st.metric(label, f"{val:,}", delta=delta)

            # Null comparison
            st.markdown("""
            <div style="background:linear-gradient(90deg,rgba(56,189,248,0.12),rgba(167,139,250,0.06));
            border-left:4px solid #38bdf8;border-radius:0 12px 12px 0;padding:12px 18px;margin:20px 0 14px 0;">
                <span style="font-size:16px;font-weight:700;color:#e2e8f0;">🔍 Null Value Comparison</span>
                <p style="margin:2px 0 0 0;font-size:12px;color:#94a3b8;">Missing value counts before and after cleaning</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                <div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.2);
                border-radius:10px;padding:10px 16px;margin-bottom:8px;">
                    <span style="color:#fca5a5;font-weight:700;font-size:13px;">❌ Before Cleaning</span>
                </div>
                """, unsafe_allow_html=True)
                st.dataframe(st.session_state.report["nulls_before"], use_container_width=True)
            with col2:
                st.markdown("""
                <div style="background:rgba(52,211,153,0.08);border:1px solid rgba(52,211,153,0.2);
                border-radius:10px;padding:10px 16px;margin-bottom:8px;">
                    <span style="color:#6ee7b7;font-weight:700;font-size:13px;">✅ After Cleaning</span>
                </div>
                """, unsafe_allow_html=True)
                st.dataframe(st.session_state.report["nulls_after"], use_container_width=True)

            # Cleaned data preview
            st.markdown("""
            <div style="background:linear-gradient(90deg,rgba(52,211,153,0.12),rgba(56,189,248,0.06));
            border-left:4px solid #34d399;border-radius:0 12px 12px 0;padding:12px 18px;margin:24px 0 14px 0;">
                <span style="font-size:16px;font-weight:700;color:#e2e8f0;">🧹 Cleaned Dataset Preview</span>
                <p style="margin:2px 0 0 0;font-size:12px;color:#94a3b8;">First 10 rows of your cleaned data</p>
            </div>
            """, unsafe_allow_html=True)

            cleaned_df     = st.session_state.cleaned_df
            total_rows     = len(cleaned_df)
            total_cols     = cleaned_df.shape[1]
            remaining_nulls = int(cleaned_df.isnull().sum().sum())

            k1, k2, k3 = st.columns(3)
            with k1:
                st.markdown(f"""
                <div class="kpi-card kpi-green" style="padding:16px 20px;">
                    <div class="kpi-title">Total Rows</div>
                    <div class="kpi-value" style="font-size:28px;">{total_rows:,}</div>
                </div>
                """, unsafe_allow_html=True)
            with k2:
                st.markdown(f"""
                <div class="kpi-card kpi-blue" style="padding:16px 20px;">
                    <div class="kpi-title">Columns</div>
                    <div class="kpi-value" style="font-size:28px;">{total_cols:,}</div>
                </div>
                """, unsafe_allow_html=True)
            with k3:
                st.markdown(f"""
                <div class="kpi-card kpi-pink" style="padding:16px 20px;">
                    <div class="kpi-title">Remaining Nulls</div>
                    <div class="kpi-value" style="font-size:28px;">{remaining_nulls:,}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.dataframe(cleaned_df.head(10), use_container_width=True)

            with st.expander("🔬 View Column Info (dtypes & null counts)"):
                col_info = pd.DataFrame({
                    "Column":     cleaned_df.columns,
                    "Data Type":  cleaned_df.dtypes.values.astype(str),
                    "Null Count": cleaned_df.isnull().sum().values,
                    "Null %":     (cleaned_df.isnull().sum().values / total_rows * 100).round(2)
                })
                st.dataframe(col_info, use_container_width=True)

            # Download
            st.markdown("""
            <div style="background:linear-gradient(90deg,rgba(167,139,250,0.12),rgba(56,189,248,0.06));
            border-left:4px solid #a78bfa;border-radius:0 12px 12px 0;padding:12px 18px;margin:24px 0 14px 0;">
                <span style="font-size:16px;font-weight:700;color:#e2e8f0;">⬇️ Download Cleaned Dataset</span>
                <p style="margin:2px 0 0 0;font-size:12px;color:#94a3b8;">Save the fully cleaned CSV to your machine</p>
            </div>
            """, unsafe_allow_html=True)

            st.download_button(
                "⬇ Download Cleaned CSV",
                st.session_state.cleaned_df.to_csv(index=False).encode("utf-8"),
                "cleaned_fitness_data.csv",
                "text/csv"
            )

            # Next button banner
            st.markdown("""
            <div class="next-banner">
                <div class="next-banner-text">
                    <p class="next-label">✦ Up Next · Step 3 of 3</p>
                    <p class="next-title">🧠 EDA</p>
                    <p class="next-desc">Explore correlations, distributions, outliers &amp; heart rate trends</p>
                </div>
                <div style="font-size:32px; opacity:0.3;">→</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class='next-btn-container'>
            <style>
            div[data-testid="stButton"] button[kind="primary"] {
                background: linear-gradient(135deg, #38bdf8 0%, #6366f1 100%) !important;
                color: white !important; border: none !important;
                border-radius: 14px !important; padding: 16px 32px !important;
                font-size: 15px !important; font-weight: 700 !important;
                letter-spacing: 0.4px !important;
                box-shadow: 0 4px 24px rgba(56,189,248,0.35) !important;
                transition: all 0.25s ease !important; width: 100% !important;
            }
            div[data-testid="stButton"] button[kind="primary"]:hover {
                background: linear-gradient(135deg, #7dd3fc 0%, #818cf8 100%) !important;
                box-shadow: 0 10px 36px rgba(56,189,248,0.6) !important;
                transform: translateY(-3px) scale(1.02) !important;
            }
            div[data-testid="stButton"] button[kind="primary"]:active {
                transform: translateY(0) scale(0.98) !important;
                box-shadow: 0 3px 12px rgba(56,189,248,0.3) !important;
            }
            </style>
            """, unsafe_allow_html=True)
            if st.button("Continue to EDA  ➜", key="next_pre", type="primary", use_container_width=True):
                go_to("EDA")
            st.markdown("</div>", unsafe_allow_html=True)

    # ==========================================================
    # EDA
    # ==========================================================
    elif page == "EDA":

        render_step_indicator("EDA")

        if not st.session_state.get("preprocessed", False):
            st.markdown("""
            <div style="background:rgba(251,146,60,0.08);border:1px solid rgba(251,146,60,0.3);
            border-radius:16px;padding:24px 28px;margin:20px 0;display:flex;align-items:flex-start;gap:16px;">
                <span style="font-size:28px;flex-shrink:0;">🔒</span>
                <div>
                    <div style="font-size:16px;font-weight:700;color:#fb923c;margin-bottom:6px;">
                        Preprocessing Required
                    </div>
                    <div style="font-size:13px;color:#64748b;line-height:1.6;">
                        EDA requires clean data. Please run the preprocessing pipeline first before
                        exploring visualizations and insights.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("⚗️ Go to Preprocessing", type="primary"):
                go_to("Preprocessing")
            st.stop()

        st.markdown("""
        <div class="glass-card" style="padding:24px 30px; margin-bottom:20px;">
            <h2 style="margin:0 0 6px 0; font-size:28px; font-weight:800;">
                🧠 Exploratory Data Analysis
            </h2>
            <p style="margin:0; color:#94a3b8; font-size:15px;">
                Deep-dive into your fitness dataset — distributions, correlations, outliers, and trends.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if "eda_done" not in st.session_state:
            st.session_state.eda_done = False

        # Sticky sidebar EDA button
        st.sidebar.markdown("---")
        if st.sidebar.button("🧠 Run EDA", type="primary", use_container_width=True):
            with st.spinner("Analysing your dataset..."):
                st.session_state.eda = run_eda_cached(df.to_csv(index=False).encode())
            st.session_state.eda_done = True

        col_run, col_info = st.columns([3,1])
        with col_run:
            if st.button("▶ Run Full EDA", type="primary"):
                with st.spinner("Analysing your dataset..."):
                    st.session_state.eda = run_eda_cached(df.to_csv(index=False).encode())
                st.session_state.eda_done = True
        with col_info:
            st.caption("💡 Tip: Use sidebar '🧠 Run EDA' button while scrolling charts.")

        if st.session_state.eda_done:

            eda          = st.session_state.eda
            all_numeric  = eda["numeric_cols"]

            # Controls row
            ctrl1, ctrl2 = st.columns([1,1])
            with ctrl1:
                numeric_cols = st.multiselect(
                    "📐 Select numeric columns to analyse",
                    all_numeric,
                    default=all_numeric[:min(4, len(all_numeric))],
                    help="Choose which numeric columns appear in distribution & boxplot charts"
                )
                if not numeric_cols:
                    numeric_cols = all_numeric
            with ctrl2:
                workout_opts = ["All"] + sorted(df["Workout_Type"].dropna().unique().tolist()) if "Workout_Type" in df.columns else ["All"]
                workout_filter = st.selectbox(
                    "🏋️ Filter by Workout Type",
                    workout_opts,
                    help="Filter all charts and analysis to a specific workout type"
                )
            # Apply workout filter
            df_filtered = df.copy()
            if workout_filter != "All" and "Workout_Type" in df.columns:
                df_filtered = df[df["Workout_Type"] == workout_filter]
                st.info(f"🔍 Showing **{workout_filter}** sessions only — {len(df_filtered):,} records")

            st.success("✅ EDA completed — scroll down to explore all insights.")
            st.caption("💡 Tip: Values near ±1 indicate strong correlation. Boxplot whiskers show data spread. Outliers are plotted as individual dots.")

            # Auto-computed key insights
            top_corr_pair, top_corr_val = ("—", 0)
            corr_df = eda["correlation"]
            for c1 in corr_df.columns:
                for c2 in corr_df.columns:
                    if c1 < c2:
                        v = abs(corr_df.loc[c1, c2])
                        if v > top_corr_val:
                            top_corr_val, top_corr_pair = v, f"{c1} & {c2}"
            top_workout = eda["workout_counts"].idxmax() if not eda["workout_counts"].empty else "—"
            avg_hr_all  = eda["sample_user"]["Heart_Rate (bpm)"].mean()

            st.markdown(f"""
            <div class="glass-card" style="padding:22px 26px; margin-bottom:20px;">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">
                    <span style="font-size:20px;">🔎</span>
                    <span style="font-size:16px;font-weight:800;color:#e2e8f0;">Key Insights</span>
                    <span style="font-size:11px;color:#475569;font-weight:600;letter-spacing:1px;
                    background:rgba(56,189,248,0.1);border:1px solid rgba(56,189,248,0.2);
                    border-radius:6px;padding:2px 10px;margin-left:4px;">AUTO-COMPUTED</span>
                </div>
                <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;">
                    <div style="background:rgba(56,189,248,0.06);border:1px solid rgba(56,189,248,0.15);
                    border-radius:12px;padding:14px 16px;">
                        <div style="font-size:10px;font-weight:700;color:#38bdf8;letter-spacing:1.2px;
                        text-transform:uppercase;margin-bottom:6px;">Top Correlation</div>
                        <div style="font-size:14px;font-weight:700;color:#e2e8f0;">{top_corr_pair}</div>
                        <div style="font-size:12px;color:#64748b;margin-top:3px;">r = {top_corr_val:.2f}</div>
                    </div>
                    <div style="background:rgba(167,139,250,0.06);border:1px solid rgba(167,139,250,0.15);
                    border-radius:12px;padding:14px 16px;">
                        <div style="font-size:10px;font-weight:700;color:#a78bfa;letter-spacing:1.2px;
                        text-transform:uppercase;margin-bottom:6px;">Top Workout Type</div>
                        <div style="font-size:14px;font-weight:700;color:#e2e8f0;">{top_workout}</div>
                        <div style="font-size:12px;color:#64748b;margin-top:3px;">Most frequent session</div>
                    </div>
                    <div style="background:rgba(244,114,182,0.06);border:1px solid rgba(244,114,182,0.15);
                    border-radius:12px;padding:14px 16px;">
                        <div style="font-size:10px;font-weight:700;color:#f472b6;letter-spacing:1.2px;
                        text-transform:uppercase;margin-bottom:6px;">Avg Heart Rate</div>
                        <div style="font-size:14px;font-weight:700;color:#e2e8f0;">{avg_hr_all:.1f} BPM</div>
                        <div style="font-size:12px;color:#64748b;margin-top:3px;">Sample user average</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<hr class='eda-divider'>", unsafe_allow_html=True)

            # Quick navigation via JS scrollIntoView
            import streamlit.components.v1 as _components
            _components.html("""
            <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:4px;font-family:'DM Sans',sans-serif;">
                <span style="font-size:11px;font-weight:700;color:#64748b;letter-spacing:1px;
                text-transform:uppercase;align-self:center;padding:5px 0;">JUMP TO:</span>
                <button onclick="window.parent.document.getElementById('fp-date-range').scrollIntoView({behavior:'smooth'})"
                style="background:rgba(56,189,248,0.12);border:1px solid rgba(56,189,248,0.3);
                color:#38bdf8;border-radius:8px;padding:6px 13px;font-size:12px;font-weight:600;
                cursor:pointer;transition:all 0.2s;" onmouseover="this.style.background='rgba(56,189,248,0.22)'"
                onmouseout="this.style.background='rgba(56,189,248,0.12)'">📅 Date Range</button>
                <button onclick="window.parent.document.getElementById('fp-correlation').scrollIntoView({behavior:'smooth'})"
                style="background:rgba(244,114,182,0.12);border:1px solid rgba(244,114,182,0.3);
                color:#f472b6;border-radius:8px;padding:6px 13px;font-size:12px;font-weight:600;
                cursor:pointer;transition:all 0.2s;" onmouseover="this.style.background='rgba(244,114,182,0.22)'"
                onmouseout="this.style.background='rgba(244,114,182,0.12)'">🔥 Correlation</button>
                <button onclick="window.parent.document.getElementById('fp-distributions').scrollIntoView({behavior:'smooth'})"
                style="background:rgba(167,139,250,0.12);border:1px solid rgba(167,139,250,0.3);
                color:#a78bfa;border-radius:8px;padding:6px 13px;font-size:12px;font-weight:600;
                cursor:pointer;transition:all 0.2s;" onmouseover="this.style.background='rgba(167,139,250,0.22)'"
                onmouseout="this.style.background='rgba(167,139,250,0.12)'">📈 Distributions</button>
                <button onclick="window.parent.document.getElementById('fp-outliers').scrollIntoView({behavior:'smooth'})"
                style="background:rgba(52,211,153,0.12);border:1px solid rgba(52,211,153,0.3);
                color:#34d399;border-radius:8px;padding:6px 13px;font-size:12px;font-weight:600;
                cursor:pointer;transition:all 0.2s;" onmouseover="this.style.background='rgba(52,211,153,0.22)'"
                onmouseout="this.style.background='rgba(52,211,153,0.12)'">📦 Outliers</button>
                <button onclick="window.parent.document.getElementById('fp-workout').scrollIntoView({behavior:'smooth'})"
                style="background:rgba(251,146,60,0.12);border:1px solid rgba(251,146,60,0.3);
                color:#fb923c;border-radius:8px;padding:6px 13px;font-size:12px;font-weight:600;
                cursor:pointer;transition:all 0.2s;" onmouseover="this.style.background='rgba(251,146,60,0.22)'"
                onmouseout="this.style.background='rgba(251,146,60,0.12)'">🏋️ Workout</button>
                <button onclick="window.parent.document.getElementById('fp-heartrate').scrollIntoView({behavior:'smooth'})"
                style="background:rgba(244,114,182,0.12);border:1px solid rgba(244,114,182,0.3);
                color:#f472b6;border-radius:8px;padding:6px 13px;font-size:12px;font-weight:600;
                cursor:pointer;transition:all 0.2s;" onmouseover="this.style.background='rgba(244,114,182,0.22)'"
                onmouseout="this.style.background='rgba(244,114,182,0.12)'">❤️ Heart Rate</button>
            </div>
            """, height=52, scrolling=False)

            st.markdown('<div id="fp-date-range"></div>', unsafe_allow_html=True)
            # ── 1. DATE RANGE ─────────────────────────────────────────
            st.markdown("""
            <div class="eda-section-banner">
                <span class="banner-icon">📅</span>
                <div>
                    <p class="banner-title">Date Range</p>
                    <p class="banner-desc">Time coverage of your fitness data</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="date-badge">
                📆 &nbsp; {eda['date_range'][0]} &nbsp;→&nbsp; {eda['date_range'][1]}
            </div>
            """, unsafe_allow_html=True)
            info_toggle(
                key="date_range",
                title="Date Range",
                objective="Displays the full temporal span of your fitness dataset — from the earliest recorded session to the most recent. This gives you an immediate sense of how long the data has been collected and whether the dataset is recent or historical.",
                insights="Check whether the date range is long enough for meaningful trend analysis (ideally 4+ weeks). A very narrow range may limit the reliability of time-series insights. Also note any unexpected gaps between the start and end dates that could indicate missing data periods."
            )
            st.markdown("<hr class='eda-divider'>", unsafe_allow_html=True)

            st.markdown('<div id="fp-correlation"></div>', unsafe_allow_html=True)
            # ── 2. CORRELATION HEATMAP ────────────────────────────────
            st.markdown("""
            <div class="eda-section-banner">
                <span class="banner-icon">🔥</span>
                <div>
                    <p class="banner-title">Correlation Heatmap</p>
                    <p class="banner-desc">How strongly each numeric feature relates to another (−1 to +1)</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
            fig1, ax1 = plt.subplots(figsize=(13, 7))
            fig1.patch.set_facecolor(CHART_BG)
            ax1.set_facecolor(CHART_BG)
            sns.heatmap(
                eda["correlation"], annot=True, cmap="coolwarm", fmt=".2f",
                linewidths=0.4, linecolor="#1e293b", ax=ax1,
                annot_kws={"size": 9, "color": CHART_TEXT},
                cbar_kws={"shrink": 0.8}
            )
            ax1.tick_params(colors=CHART_SUBTEXT, labelsize=9)
            ax1.set_title("Feature Correlation Matrix", color=CHART_TEXT, fontsize=14, fontweight="bold", pad=14)
            cbar = ax1.collections[0].colorbar
            cbar.ax.tick_params(colors=CHART_SUBTEXT, labelsize=8)
            fig1.tight_layout()
            st.pyplot(fig1)
            buf1 = __import__('io').BytesIO(); fig1.savefig(buf1, format="png", dpi=150, bbox_inches="tight", facecolor=CHART_BG)
            st.download_button("⬇ Download Heatmap", buf1.getvalue(), "correlation_heatmap.png", "image/png", key="dl_heatmap")
            st.markdown('</div>', unsafe_allow_html=True)
            info_toggle(
                key="correlation_heatmap",
                title="Correlation Heatmap",
                objective="Measures and visualises the pairwise linear relationship between all numeric features in your dataset. Each cell shows a Pearson correlation coefficient ranging from −1 (perfect negative) to +1 (perfect positive), with 0 indicating no linear relationship.",
                insights="Focus on the darkest red cells (strong positive correlation, e.g. calories burned vs. workout duration) and darkest blue cells (strong negative correlation). Correlations above 0.7 or below −0.7 are particularly noteworthy. Avoid using two highly correlated features as independent inputs in any model, as they carry redundant information."
            )
            st.markdown("<hr class='eda-divider'>", unsafe_allow_html=True)

            st.markdown('<div id="fp-distributions"></div>', unsafe_allow_html=True)
            # ── 3. DISTRIBUTIONS ──────────────────────────────────────
            st.markdown("""
            <div class="eda-section-banner">
                <span class="banner-icon">📈</span>
                <div>
                    <p class="banner-title">Distribution of Numeric Features</p>
                    <p class="banner-desc">Histogram + KDE curve for each numeric column</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            # Section-level info toggle for distributions
            info_toggle(
                key="distributions_overview",
                title="Distribution Charts (All Features)",
                objective="Reveals the shape, spread, and central tendency of each numeric variable. The histogram bars show how frequently values fall within each range, while the KDE (Kernel Density Estimate) curve traces the smooth underlying probability distribution.",
                insights="Look for bell-shaped (normal) distributions, which are ideal for many statistical methods. Right-skewed distributions (long tail to the right) are common in fitness data like calories or workout duration. Heavy skew or multiple peaks (bimodal) may suggest distinct subgroups in your data, such as beginner vs. advanced users."
            )
            st.markdown("<br>", unsafe_allow_html=True)
            cols2 = st.columns(3)
            for i, col_name in enumerate(numeric_cols):
                fig, ax = plt.subplots(figsize=(6, 3.5))
                sns.histplot(df_filtered[col_name].dropna(), kde=True, ax=ax,
                             color=PALETTE[i % len(PALETTE)], edgecolor="none",
                             alpha=0.75, line_kws={"linewidth": 2})
                ax.set_title(f"{col_name}")
                ax.set_xlabel("")
                apply_dark_style(fig, ax)
                with cols2[i % 3]:
                    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
                    st.pyplot(fig)
                    # Per-column info toggle inside the chart wrapper
                    info_toggle(
                        key=f"dist_{col_name}",
                        title=f"{col_name} Distribution",
                        objective=f"Shows how values of <strong>{col_name}</strong> are spread across your dataset. The bars represent the frequency of observations in each value range, and the smooth KDE curve estimates the underlying probability density.",
                        insights=f"Check whether <strong>{col_name}</strong> is roughly symmetric or skewed. A long right tail means a few users have very high values. The tallest bar indicates the most common range. Flat or widely spread distributions suggest high variability across users or sessions."
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<hr class='eda-divider'>", unsafe_allow_html=True)

            st.markdown('<div id="fp-outliers"></div>', unsafe_allow_html=True)
            # ── 4. BOXPLOTS ───────────────────────────────────────────
            st.markdown("""
            <div class="eda-section-banner">
                <span class="banner-icon">📦</span>
                <div>
                    <p class="banner-title">Outlier Detection</p>
                    <p class="banner-desc">Boxplots reveal spread, medians, and potential outliers per feature</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            # Section-level info toggle for boxplots
            info_toggle(
                key="boxplots_overview",
                title="Outlier Detection Boxplots (All Features)",
                objective="Boxplots summarise the statistical distribution of each numeric feature using five key values: minimum, Q1 (25th percentile), median, Q3 (75th percentile), and maximum. Individual dots beyond the whiskers represent statistical outliers — values more than 1.5× the interquartile range from the box edges.",
                insights="A compact box with short whiskers means consistent, predictable data. A wide box indicates high variability. Dots beyond the whiskers are potential outliers — these could be data entry errors, exceptional athletic performance, or sensor malfunctions. Investigate outliers before modelling to decide whether to remove, cap, or keep them."
            )
            st.markdown("<br>", unsafe_allow_html=True)
            cols3 = st.columns(2)
            for i, col_name in enumerate(numeric_cols):
                fig, ax = plt.subplots(figsize=(6, 3.2))
                sns.boxplot(x=df_filtered[col_name].dropna(), ax=ax,
                            color=PALETTE[i % len(PALETTE)],
                            flierprops=dict(marker="o", markerfacecolor=CHART_ACCENT3, markersize=4, alpha=0.6),
                            boxprops=dict(alpha=0.8),
                            whiskerprops=dict(color=CHART_SUBTEXT),
                            capprops=dict(color=CHART_SUBTEXT),
                            medianprops=dict(color="#facc15", linewidth=2))
                ax.set_title(f"{col_name}")
                ax.set_xlabel("")
                apply_dark_style(fig, ax)
                with cols3[i % 2]:
                    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
                    st.pyplot(fig)
                    # Per-column boxplot info toggle
                    info_toggle(
                        key=f"box_{col_name}",
                        title=f"{col_name} Boxplot",
                        objective=f"Visualises the spread and outliers for <strong>{col_name}</strong>. The yellow line marks the median value. The box spans Q1–Q3 (the middle 50% of data). Whiskers extend to the furthest non-outlier point. Pink dots beyond the whiskers are statistical outliers.",
                        insights=f"The yellow median line for <strong>{col_name}</strong> tells you the typical value. If the median is shifted far from the centre of the box, the data is skewed. Pink outlier dots indicate unusually high or low values — check whether these are valid extreme performances or data errors worth investigating."
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<hr class='eda-divider'>", unsafe_allow_html=True)

            st.markdown('<div id="fp-workout"></div>', unsafe_allow_html=True)
            # ── 5. WORKOUT DISTRIBUTION ───────────────────────────────
            st.markdown("""
            <div class="eda-section-banner">
                <span class="banner-icon">🏋️</span>
                <div>
                    <p class="banner-title">Workout Type Distribution</p>
                    <p class="banner-desc">Breakdown of workout sessions by type</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            workout_counts  = eda["workout_counts"]
            col_pie, col_bar = st.columns(2)

            with col_pie:
                st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
                fig3, ax3 = plt.subplots(figsize=(5.5, 5))
                fig3.patch.set_facecolor(CHART_BG)
                wedges, texts, autotexts = ax3.pie(
                    workout_counts, labels=workout_counts.index, autopct="%1.1f%%",
                    colors=PALETTE[:len(workout_counts)], startangle=140,
                    wedgeprops=dict(edgecolor=CHART_BG, linewidth=2), pctdistance=0.80
                )
                for t in texts:   t.set_color(CHART_SUBTEXT); t.set_fontsize(10)
                for at in autotexts: at.set_color(CHART_TEXT); at.set_fontsize(9); at.set_fontweight("bold")
                ax3.set_ylabel("")
                ax3.set_title("Workout Split", color=CHART_TEXT, fontsize=13, fontweight="bold")
                fig3.tight_layout()
                st.pyplot(fig3)
                info_toggle(
                    key="workout_pie",
                    title="Workout Split Pie Chart",
                    objective="Shows the proportional share of each workout type across all sessions in the dataset. Each slice represents one workout category and its percentage of total training volume.",
                    insights="A dominant slice (>50%) suggests the dataset is heavily biased toward one workout type, which may affect model generalisation. A balanced split across types is ideal for comparative analysis. Look for underrepresented workout types — they may have insufficient data for reliable per-type insights."
                )
                st.markdown('</div>', unsafe_allow_html=True)

            with col_bar:
                st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
                fig3b, ax3b = plt.subplots(figsize=(5.5, 5))
                bars = ax3b.barh(workout_counts.index, workout_counts.values,
                                 color=PALETTE[:len(workout_counts)], edgecolor="none", height=0.55)
                for bar, val in zip(bars, workout_counts.values):
                    ax3b.text(bar.get_width() + max(workout_counts.values) * 0.01,
                              bar.get_y() + bar.get_height() / 2, f"{val:,}",
                              va="center", ha="left", color=CHART_TEXT, fontsize=9, fontweight="bold")
                ax3b.set_title("Session Counts", color=CHART_TEXT, fontsize=13, fontweight="bold")
                ax3b.set_xlabel("Count", color=CHART_SUBTEXT)
                ax3b.invert_yaxis()
                apply_dark_style(fig3b, ax3b)
                st.pyplot(fig3b)
                info_toggle(
                    key="workout_bar",
                    title="Session Counts Bar Chart",
                    objective="Provides an absolute count comparison of sessions per workout type. Unlike the pie chart, this makes it easy to compare exact session volumes side by side without converting percentages.",
                    insights="The longest bar is the most frequently logged workout type. Compare the gap between the top two workout types — a very large gap may mean your data heavily represents one training style. Small counts (short bars) for certain workout types mean those insights may be less statistically reliable."
                )
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<hr class='eda-divider'>", unsafe_allow_html=True)

            # ── 6. USER SUMMARY ───────────────────────────────────────
            st.markdown("""
            <div class="eda-section-banner">
                <span class="banner-icon">👥</span>
                <div>
                    <p class="banner-title">User-Level Average Summary</p>
                    <p class="banner-desc">Per-user aggregated averages across all tracked metrics</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(eda["user_summary"], use_container_width=True)
            info_toggle(
                key="user_summary",
                title="User-Level Average Summary Table",
                objective="Aggregates each user's fitness data into a single summary row of averages. This allows you to compare users directly across all metrics — heart rate, calories burned, workout duration, steps, and more — on an equal footing regardless of how many sessions each user has logged.",
                insights="Look for users with unusually high or low averages compared to the group — they may be outliers or represent different fitness levels. Large variance across users suggests the dataset captures a diverse population, which is good for generalisation. Use this table to identify power users (high activity) vs. low-engagement users for segmentation."
            )
            st.markdown("<hr class='eda-divider'>", unsafe_allow_html=True)

            st.markdown('<div id="fp-heartrate"></div>', unsafe_allow_html=True)
            # ── 7. HEART RATE TIME SERIES ─────────────────────────────
            st.markdown("""
            <div class="eda-section-banner">
                <span class="banner-icon">❤️</span>
                <div>
                    <p class="banner-title">Heart Rate Time-Series</p>
                    <p class="banner-desc">BPM trend over time for a sample user</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            sample_df = eda["sample_user"].copy()
            sample_df["HR_MA"] = sample_df["Heart_Rate (bpm)"].rolling(window=3, center=True).mean()
            st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
            fig4, ax4 = plt.subplots(figsize=(12, 4))
            ax4.fill_between(sample_df["Date"], sample_df["Heart_Rate (bpm)"],
                             alpha=0.12, color=CHART_ACCENT3)
            ax4.plot(sample_df["Date"], sample_df["Heart_Rate (bpm)"],
                     color=CHART_ACCENT3, linewidth=1.5, marker="o", markersize=3,
                     markerfacecolor=CHART_ACCENT3, markeredgecolor=CHART_BG, markeredgewidth=1,
                     alpha=0.6, label="Raw BPM")
            ax4.plot(sample_df["Date"], sample_df["HR_MA"],
                     color="#facc15", linewidth=2.5, linestyle="--", label="3-pt Rolling Avg", zorder=5)
            ax4.legend(loc="upper right", fontsize=8, facecolor=CHART_SURFACE,
                       edgecolor=(1,1,1,0.1), labelcolor=CHART_TEXT)
            max_idx = sample_df["Heart_Rate (bpm)"].idxmax()
            min_idx = sample_df["Heart_Rate (bpm)"].idxmin()
            ax4.annotate(f"Peak: {sample_df.loc[max_idx,'Heart_Rate (bpm)']:.0f} bpm",
                         xy=(sample_df.loc[max_idx,"Date"], sample_df.loc[max_idx,"Heart_Rate (bpm)"]),
                         xytext=(10,10), textcoords="offset points",
                         color="#facc15", fontsize=8, fontweight="bold",
                         arrowprops=dict(arrowstyle="->", color="#facc15", lw=1))
            ax4.annotate(f"Low: {sample_df.loc[min_idx,'Heart_Rate (bpm)']:.0f} bpm",
                         xy=(sample_df.loc[min_idx,"Date"], sample_df.loc[min_idx,"Heart_Rate (bpm)"]),
                         xytext=(10,-18), textcoords="offset points",
                         color=CHART_ACCENT4, fontsize=8, fontweight="bold",
                         arrowprops=dict(arrowstyle="->", color=CHART_ACCENT4, lw=1))
            ax4.set_title("Heart Rate Trend — Sample User", pad=12)
            ax4.set_xlabel("Date")
            ax4.set_ylabel("BPM")
            plt.xticks(rotation=40, ha="right")
            apply_dark_style(fig4, ax4)
            st.pyplot(fig4)
            st.markdown('</div>', unsafe_allow_html=True)

            info_toggle(
                key="heart_rate_trend",
                title="Heart Rate Time-Series",
                objective="Plots a sample user's heart rate (BPM) across all their recorded sessions over time. The pink line shows raw per-session BPM values, while the dashed yellow line is a 3-point rolling average that smooths out noise to reveal the underlying cardiovascular trend. Peak and low BPM sessions are annotated automatically.",
                insights="An upward trend in the rolling average over time could indicate increasing workout intensity or cardiovascular fatigue. A downward trend may reflect improving cardiovascular fitness (lower resting or exercise heart rate is often a sign of better fitness). Sudden spikes far above the rolling average may point to especially intense sessions, illness, or sensor anomalies worth investigating."
            )

            buf4 = __import__('io').BytesIO(); fig4.savefig(buf4, format="png", dpi=150, bbox_inches="tight", facecolor=CHART_BG)
            st.download_button("⬇ Download HR Chart", buf4.getvalue(), "heart_rate_trend.png", "image/png", key="dl_hr")
            avg_hr = sample_df["Heart_Rate (bpm)"].mean()
            max_hr = sample_df["Heart_Rate (bpm)"].max()
            min_hr = sample_df["Heart_Rate (bpm)"].min()
            st.markdown(f"""
            <div style="margin-top:10px;">
                <span class="insight-pill">Avg BPM: {avg_hr:.1f}</span>
                <span class="insight-pill">Peak: {max_hr:.0f}</span>
                <span class="insight-pill">Low: {min_hr:.0f}</span>
                <span class="insight-pill">Range: {max_hr - min_hr:.0f} bpm</span>
            </div>
            """, unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div style="
    margin-top: 60px;
    padding: 24px 0 16px 0;
    border-top: 1px solid rgba(56,189,248,0.1);
    text-align: center;
">
    <div style="font-size:13px;font-weight:700;color:#334155;letter-spacing:0.5px;">
        FitPulse Analytics
    </div>
    <div style="font-size:11px;color:#1e293b;margin-top:4px;">
        Data Exploration Tool &nbsp;·&nbsp; Built with Streamlit &nbsp;·&nbsp; v1.0
    </div>
</div>
""", unsafe_allow_html=True)