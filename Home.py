# ═══════════════════════════════════════════════════════════════
#  FITPULSE  ·  HOME  ·  Home.py
#  Run:  streamlit run Home.py
# ═══════════════════════════════════════════════════════════════
import os
import streamlit as st

st.set_page_config(
    page_title="FitPulse",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE      = os.path.dirname(os.path.abspath(__file__))
M1_PAGE   = "pages/1preprocessing.py"
M2_PAGE   = "pages/2clustring.py"
M1_EXISTS = os.path.isfile(os.path.join(BASE, M1_PAGE))
M2_EXISTS = os.path.isfile(os.path.join(BASE, M2_PAGE))

# ════════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Space+Mono:wght@400;700&display=swap');

    section[data-testid="stSidebar"] {
        background: #07060f !important;
        background-image:
            radial-gradient(ellipse 140% 30% at 50% 0%,
                rgba(99,60,255,0.18) 0%, transparent 55%),
            linear-gradient(180deg, #09081a 0%, #06050e 100%) !important;
        border-right: 1px solid rgba(99,60,255,0.12) !important;
        box-shadow: 4px 0 40px rgba(0,0,0,0.6) !important;
    }
    section[data-testid="stSidebar"] * {
        font-family: 'Sora', sans-serif !important;
    }
    section[data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: 1px solid rgba(99,60,255,0.2) !important;
        color: #7c75b8 !important;
        border-radius: 10px !important;
        font-size: 12px !important;
        font-family: 'Space Mono', monospace !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        padding: 8px 14px !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(99,60,255,0.12) !important;
        border-color: rgba(99,60,255,0.5) !important;
        color: #a89fff !important;
        box-shadow: 0 0 20px rgba(99,60,255,0.2) !important;
    }
    </style>

    <!-- LOGO MARK -->
    <div style="text-align:center;padding:28px 16px 20px;">
        <div style="
            width:60px;height:60px;border-radius:18px;
            background:linear-gradient(135deg,#1a1040,#2d1870);
            border:1px solid rgba(99,60,255,0.5);
            display:flex;align-items:center;justify-content:center;
            margin:0 auto 14px;
            box-shadow:0 0 30px rgba(99,60,255,0.35),
                       inset 0 1px 0 rgba(255,255,255,0.08);
        ">
            <svg width="30" height="30" viewBox="0 0 32 32" fill="none">
                <polyline points="2,16 7,16 10,7 16,26 22,9 26,20 29,16 30,16"
                    stroke="url(#sg)" stroke-width="2.4"
                    stroke-linecap="round" stroke-linejoin="round"/>
                <defs>
                    <linearGradient id="sg" x1="0" y1="0" x2="32" y2="0">
                        <stop offset="0%" stop-color="#633cff"/>
                        <stop offset="100%" stop-color="#38bdf8"/>
                    </linearGradient>
                </defs>
            </svg>
        </div>
        <div style="font-family:'Sora',sans-serif;font-size:17px;
            font-weight:800;color:#e8e4ff;letter-spacing:0.5px;">
            FitPulse
        </div>
        <div style="font-family:'Space Mono',monospace;font-size:9px;
            color:#2e2a60;letter-spacing:3px;text-transform:uppercase;
            margin-top:4px;">
            Analytics
        </div>
    </div>

    <!-- DIVIDER -->
    <div style="height:1px;background:linear-gradient(90deg,transparent,
        rgba(99,60,255,0.2),transparent);margin:0 16px 20px;"></div>

    <!-- NAV LABEL -->
    <div style="font-family:'Space Mono',monospace;font-size:8px;
        letter-spacing:3px;color:#1e1a40;text-transform:uppercase;
        padding:0 20px 10px;">Navigate</div>
    """, unsafe_allow_html=True)

    # Nav buttons
    if st.button("🏠  Home", key="sb_home"):
        st.switch_page("Home.py")

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    if st.button("📊  Data Explorer", key="sb_m1",
                 disabled=not M1_EXISTS):
        st.switch_page(M1_PAGE)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    if st.button("🔬  Intelligence Lab", key="sb_m2",
                 disabled=not M2_EXISTS):
        st.switch_page(M2_PAGE)

    st.markdown("""
    <!-- BOTTOM BADGE -->
    <div style="position:absolute;bottom:20px;left:0;right:0;
        text-align:center;padding:0 16px;">
        <div style="background:rgba(99,60,255,0.06);
            border:1px solid rgba(99,60,255,0.12);
            border-radius:10px;padding:10px 14px;">
            <div style="font-family:'Space Mono',monospace;
                font-size:8px;color:#2e2a60;letter-spacing:1px;
                line-height:1.9;">
                2016 Fitbit Dataset<br>
                35 Users · 31 Days
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  MAIN CSS
# ════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800;900&family=Space+Mono:wght@400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp { font-family: 'Sora', sans-serif !important; }

    /* Hide Streamlit default multipage sidebar nav */
    [data-testid="stSidebarNav"] { display: none !important; }
    [data-testid="stSidebarNavItems"] { display: none !important; }
    [data-testid="stSidebarNavSeparator"] { display: none !important; }


.stApp {
    background: #06050e;
    background-image:
        radial-gradient(ellipse 120% 55% at 50% -5%,
            rgba(99,60,255,0.22) 0%, transparent 58%),
        radial-gradient(ellipse 60% 50% at 2% 55%,
            rgba(56,189,248,0.07) 0%, transparent 55%),
        radial-gradient(ellipse 55% 45% at 98% 75%,
            rgba(245,166,35,0.07) 0%, transparent 55%),
        radial-gradient(ellipse 40% 40% at 50% 100%,
            rgba(255,60,130,0.05) 0%, transparent 55%);
    min-height: 100vh;
    color: #e8e4ff;
}

/* Glow bar top */
.stApp::before {
    content: '';
    position: fixed; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg,
        transparent 0%, #633cff 20%, #38bdf8 45%,
        #ff3c82 70%, #f5a623 85%, transparent 100%);
    z-index: 99999; pointer-events: none;
    box-shadow: 0 0 50px rgba(99,60,255,0.5);
    animation: scanline 4s ease-in-out infinite;
}
@keyframes scanline {
    0%,100% { opacity:1; }
    50%      { opacity:0.7; }
}

#MainMenu, footer, header { visibility: hidden !important; }
.block-container {
    padding: 1.5rem 2rem 3rem !important;
    max-width: 100% !important;
}

/* ── HERO TITLE ──────────────────────────────────────────── */
.hero-wrap {
    position: relative;
    text-align: center;
    padding: 20px 20px 10px;
    overflow: hidden;
}
/* Animated background rings */
.hero-ring-1 {
    position: absolute;
    width: 600px; height: 600px;
    border-radius: 50%;
    border: 1px solid rgba(99,60,255,0.08);
    top: 50%; left: 50%;
    transform: translate(-50%,-50%);
    animation: ringPulse 4s ease-in-out infinite;
    pointer-events: none;
}
.hero-ring-2 {
    position: absolute;
    width: 400px; height: 400px;
    border-radius: 50%;
    border: 1px solid rgba(56,189,248,0.07);
    top: 50%; left: 50%;
    transform: translate(-50%,-50%);
    animation: ringPulse 4s ease-in-out 0.5s infinite;
    pointer-events: none;
}
.hero-ring-3 {
    position: absolute;
    width: 220px; height: 220px;
    border-radius: 50%;
    border: 1px solid rgba(245,166,35,0.08);
    top: 50%; left: 50%;
    transform: translate(-50%,-50%);
    animation: ringPulse 4s ease-in-out 1s infinite;
    pointer-events: none;
}
@keyframes ringPulse {
    0%,100% { transform: translate(-50%,-50%) scale(1); opacity:1; }
    50%      { transform: translate(-50%,-50%) scale(1.04); opacity:0.6; }
}

.hero-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 10px; letter-spacing: 5px;
    text-transform: uppercase;
    color: #633cff; margin-bottom: 16px;
    display: inline-flex; align-items: center; gap: 10px;
    position: relative; z-index: 2;
}
.hero-eyebrow::before, .hero-eyebrow::after {
    content: ''; width: 28px; height: 1px;
    background: linear-gradient(90deg, transparent, #633cff);
    box-shadow: 0 0 6px #633cff;
}
.hero-eyebrow::after { transform: scaleX(-1); }

.hero-title {
    font-size: 72px !important;
    font-weight: 900 !important;
    line-height: 0.95 !important;
    letter-spacing: -2px;
    margin-bottom: 0 !important;
    position: relative; z-index: 2;
}
.hero-title .t1 {
    display: block;
    background: linear-gradient(135deg, #ffffff 0%, #c4b5fd 40%, #818cf8 70%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-title .t2 {
    display: block;
    background: linear-gradient(135deg, #38bdf8 0%, #633cff 50%, #ff3c82 100%);
    background-size: 200% auto;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: titleShimmer 5s linear infinite;
}
@keyframes titleShimmer {
    0%{background-position:0% center;}
    100%{background-position:200% center;}
}

/* ── PULSE ORBS ──────────────────────────────────────────── */
.orb-row {
    display: flex; align-items: center; justify-content: center;
    gap: 20px; margin: 20px 0 24px;
}
.orb {
    width: 12px; height: 12px; border-radius: 50%;
    animation: orbBeat 2s ease-in-out infinite;
}
.orb-1 { background:#633cff; box-shadow:0 0 14px #633cff;
          animation-delay:0s; }
.orb-2 { background:#38bdf8; box-shadow:0 0 14px #38bdf8;
          animation-delay:0.3s; width:8px; height:8px; }
.orb-3 { background:#ff3c82; box-shadow:0 0 14px #ff3c82;
          animation-delay:0.6s; }
.orb-4 { background:#f5a623; box-shadow:0 0 14px #f5a623;
          animation-delay:0.9s; width:8px; height:8px; }
.orb-5 { background:#4ade80; box-shadow:0 0 14px #4ade80;
          animation-delay:1.2s; }
@keyframes orbBeat {
    0%,100%{transform:scale(1);opacity:1;}
    50%{transform:scale(1.5);opacity:0.6;}
}
.orb-line {
    flex:1; max-width:80px; height:1px;
    background:linear-gradient(90deg,transparent,rgba(99,60,255,0.2),transparent);
}

/* ── CARDS ───────────────────────────────────────────────── */
.cards-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin: 0 0 16px;
}

.card {
    border-radius: 22px;
    padding: 0;
    position: relative;
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.35s cubic-bezier(0.34,1.4,0.64,1),
                box-shadow 0.35s ease;
    min-height: 320px;
}
.card:hover { transform: translateY(-8px) scale(1.01); }

/* M1 card */
.card-m1 {
    background:
        radial-gradient(ellipse 80% 60% at 90% 20%,
            rgba(99,60,255,0.22) 0%, transparent 60%),
        radial-gradient(ellipse 60% 80% at 10% 80%,
            rgba(56,189,248,0.12) 0%, transparent 55%),
        linear-gradient(145deg, #12103a 0%, #0a0820 60%, #080616 100%);
    border: 1px solid rgba(99,60,255,0.25);
    box-shadow:
        0 24px 60px rgba(0,0,0,0.6),
        0 0 0 1px rgba(255,255,255,0.04) inset;
}
.card-m1:hover {
    border-color: rgba(99,60,255,0.55);
    box-shadow:
        0 32px 80px rgba(0,0,0,0.7),
        0 0 80px rgba(99,60,255,0.15),
        0 0 0 1px rgba(99,60,255,0.08) inset;
}

/* M2 card */
.card-m2 {
    background:
        radial-gradient(ellipse 80% 60% at 10% 20%,
            rgba(245,166,35,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 80% at 90% 80%,
            rgba(255,60,130,0.10) 0%, transparent 55%),
        linear-gradient(145deg, #1a1208 0%, #100c08 60%, #080608 100%);
    border: 1px solid rgba(245,166,35,0.22);
    box-shadow:
        0 24px 60px rgba(0,0,0,0.6),
        0 0 0 1px rgba(255,255,255,0.04) inset;
}
.card-m2:hover {
    border-color: rgba(245,166,35,0.5);
    box-shadow:
        0 32px 80px rgba(0,0,0,0.7),
        0 0 80px rgba(245,166,35,0.12),
        0 0 0 1px rgba(245,166,35,0.06) inset;
}

/* Accent top strip */
.card::before {
    content: '';
    position: absolute; top: 0; left: 8%; right: 8%; height: 1px;
    background: linear-gradient(90deg, transparent,
        var(--ca), transparent);
    box-shadow: 0 0 16px var(--ca);
}
.card-m1 { --ca: rgba(99,60,255,0.85); }
.card-m2 { --ca: rgba(245,166,35,0.85); }

/* Inner glow orb */
.card-glow {
    position: absolute;
    width: 240px; height: 240px;
    border-radius: 50%;
    pointer-events: none;
    transition: opacity 0.3s ease;
}
.glow-m1 {
    top: -60px; right: -60px;
    background: radial-gradient(circle,
        rgba(99,60,255,0.18) 0%, transparent 70%);
}
.glow-m2 {
    top: -60px; left: -60px;
    background: radial-gradient(circle,
        rgba(245,166,35,0.15) 0%, transparent 70%);
}
.card:hover .card-glow { opacity: 1.5; }

.card-inner { padding: 36px 32px 32px; position: relative; z-index: 2; }

/* Big number watermark */
.card-num {
    position: absolute; right: 28px; bottom: 20px;
    font-size: 120px; font-weight: 900; line-height: 1;
    pointer-events: none; opacity: 0.04;
    color: var(--ca);
    transition: opacity 0.3s ease;
    letter-spacing: -4px;
}
.card:hover .card-num { opacity: 0.08; }

/* Icon cluster */
.card-icon-cluster {
    display: flex; align-items: center; gap: 8px;
    margin-bottom: 20px;
}
.card-icon-main {
    width: 48px; height: 48px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; flex-shrink: 0;
}
.icon-m1 {
    background: rgba(99,60,255,0.15);
    border: 1px solid rgba(99,60,255,0.3);
    box-shadow: 0 0 20px rgba(99,60,255,0.2);
}
.icon-m2 {
    background: rgba(245,166,35,0.12);
    border: 1px solid rgba(245,166,35,0.25);
    box-shadow: 0 0 20px rgba(245,166,35,0.18);
}
.card-icon-dots {
    display: flex; gap: 5px;
}
.icon-dot {
    width: 6px; height: 6px; border-radius: 50%;
    animation: dotFade 2s ease-in-out infinite;
}
.dot-m1-a { background:#633cff; animation-delay:0s; }
.dot-m1-b { background:#38bdf8; animation-delay:0.3s; }
.dot-m1-c { background:#818cf8; animation-delay:0.6s; }
.dot-m2-a { background:#f5a623; animation-delay:0s; }
.dot-m2-b { background:#ff3c82; animation-delay:0.3s; }
.dot-m2-c { background:#fcd34d; animation-delay:0.6s; }
@keyframes dotFade {
    0%,100%{opacity:1;transform:scale(1);}
    50%{opacity:0.3;transform:scale(0.7);}
}

.card-label {
    font-family: 'Space Mono', monospace;
    font-size: 9px; letter-spacing: 3px; text-transform: uppercase;
    margin-bottom: 10px;
    display: flex; align-items: center; gap: 8px;
}
.label-m1 { color: #818cf8; }
.label-m2 { color: #f5a623; }
.card-label::before {
    content: ''; width: 14px; height: 1px;
    background: currentColor;
    box-shadow: 0 0 4px currentColor;
}

.card-title {
    font-size: 38px; font-weight: 800;
    color: #f0ecff; letter-spacing: -1px;
    line-height: 1.05; margin-bottom: 16px;
}

/* Visual data bars */
.data-bars {
    display: flex; gap: 5px; margin-bottom: 20px;
    align-items: flex-end; height: 36px;
}
.bar {
    border-radius: 3px 3px 0 0;
    width: 10px; flex-shrink: 0;
    animation: barGrow 1.5s ease-out both;
}
@keyframes barGrow {
    from { transform: scaleY(0); transform-origin: bottom; }
    to   { transform: scaleY(1); transform-origin: bottom; }
}

/* Visual dots grid for M2 */
.dot-grid {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    gap: 5px; margin-bottom: 20px;
}
.dg-dot {
    width: 6px; height: 6px; border-radius: 50%;
    opacity: 0.15;
}
.dg-dot.lit { opacity: 0.9; animation: litPulse 2s ease-in-out infinite; }
@keyframes litPulse {
    0%,100%{opacity:0.9;} 50%{opacity:0.3;}
}

/* Stat row */
.card-stats {
    display: flex; gap: 0;
    border-top: 1px solid rgba(255,255,255,0.05);
    padding-top: 16px; margin-top: 4px;
}
.cs { flex: 1; text-align: center; }
.cs + .cs { border-left: 1px solid rgba(255,255,255,0.05); }
.cs-n {
    font-size: 22px; font-weight: 800; color: #f0ecff;
    letter-spacing: -0.5px;
}
.cs-l {
    font-family: 'Space Mono', monospace;
    font-size: 8px; color: #2e2a60;
    letter-spacing: 1.5px; text-transform: uppercase; margin-top: 2px;
}

/* ── BOTTOM STATS STRIP ──────────────────────────────────── */
.stats-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px; margin-bottom: 16px;
}
.ss-cell {
    border-radius: 14px; padding: 16px 18px;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    text-align: center;
    transition: all 0.2s ease;
}
.ss-cell:hover {
    background: rgba(99,60,255,0.05);
    border-color: rgba(99,60,255,0.15);
}
.ss-n {
    font-size: 28px; font-weight: 800; color: #e8e4ff;
    letter-spacing: -1px; line-height: 1;
}
.ss-l {
    font-family: 'Space Mono', monospace;
    font-size: 8px; color: #2e2a60;
    letter-spacing: 2px; text-transform: uppercase; margin-top: 5px;
}
.ss-bar {
    height: 2px; border-radius: 2px;
    margin: 8px auto 0;
    animation: barShimmer 3s ease-in-out infinite;
}
@keyframes barShimmer {
    0%{opacity:0.4;} 50%{opacity:1;} 100%{opacity:0.4;}
}

/* ── FOOTER LINE ─────────────────────────────────────────── */
.home-foot {
    display: flex; align-items: center; justify-content: center;
    gap: 16px; margin-top: 8px; opacity: 0.25;
}
.foot-dot {
    width: 3px; height: 3px; border-radius: 50%;
    background: #633cff;
}
.foot-txt {
    font-family: 'Space Mono', monospace;
    font-size: 9px; color: #633cff; letter-spacing: 2px;
    text-transform: uppercase;
}

/* ── Button overrides ────────────────────────────────────── */
div[data-testid="stButton"]:has(button[key="btn_m1"]) > button {
    background: linear-gradient(135deg, #4f46e5, #633cff) !important;
    border: none !important; color: white !important;
    border-radius: 12px !important; font-weight: 700 !important;
    font-size: 14px !important; padding: 12px 24px !important;
    box-shadow: 0 4px 24px rgba(99,60,255,0.45) !important;
    transition: all 0.25s ease !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
}
div[data-testid="stButton"]:has(button[key="btn_m1"]) > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 40px rgba(99,60,255,0.6) !important;
}

div[data-testid="stButton"]:has(button[key="btn_m2"]) > button {
    background: linear-gradient(135deg, #c2620a, #f5a623) !important;
    border: none !important; color: white !important;
    border-radius: 12px !important; font-weight: 700 !important;
    font-size: 14px !important; padding: 12px 24px !important;
    box-shadow: 0 4px 24px rgba(245,166,35,0.4) !important;
    transition: all 0.25s ease !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
}
div[data-testid="stButton"]:has(button[key="btn_m2"]) > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 40px rgba(245,166,35,0.55) !important;
}

/* ── Animations ──────────────────────────────────────────── */
@keyframes rise {
    from { opacity:0; transform:translateY(28px); }
    to   { opacity:1; transform:translateY(0); }
}
.r1{animation:rise 0.55s ease both;}
.r2{animation:rise 0.55s 0.1s ease both;}
.r3{animation:rise 0.55s 0.2s ease both;}
.r4{animation:rise 0.55s 0.3s ease both;}
.r5{animation:rise 0.55s 0.4s ease both;}

::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-track{background:#06050e;}
::-webkit-scrollbar-thumb{background:#1e1840;border-radius:2px;}
::-webkit-scrollbar-thumb:hover{background:#633cff;}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  HERO
# ════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrap r1">
    <div class="hero-ring-1"></div>
    <div class="hero-ring-2"></div>
    <div class="hero-ring-3"></div>
    <div class="hero-eyebrow">Fitness · Analytics · Intelligence</div>
    <div class="hero-title">
        <span class="t1">FitPulse</span>
        <span class="t2">Analytics</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Pulse orbs
st.markdown("""
<div class="orb-row r2">
    <div class="orb-line"></div>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    <div class="orb orb-4"></div>
    <div class="orb orb-5"></div>
    <div class="orb-line"></div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  CARDS — using components.html to bypass sanitizer
# ════════════════════════════════════════════════════════════════
import streamlit.components.v1 as components

CARD_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800;900&family=Space+Mono:wght@400;700&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{background:transparent;font-family:'Sora',sans-serif;overflow:hidden;}
.card{border-radius:22px;padding:32px 28px 28px;position:relative;
overflow:hidden;height:320px;display:flex;flex-direction:column;
transition:transform 0.35s cubic-bezier(0.34,1.4,0.64,1),box-shadow 0.35s ease;}

/* M1 */
.cm1{background:radial-gradient(ellipse 80% 60% at 90% 20%,rgba(99,60,255,0.22) 0%,transparent 60%),
    radial-gradient(ellipse 60% 80% at 10% 80%,rgba(56,189,248,0.12) 0%,transparent 55%),
    linear-gradient(145deg,#12103a 0%,#0a0820 60%,#080616 100%);
    border:1px solid rgba(99,60,255,0.25);
    box-shadow:0 24px 60px rgba(0,0,0,0.6),0 0 0 1px rgba(255,255,255,0.04) inset;}
.cm1:hover{border-color:rgba(99,60,255,0.55);
    box-shadow:0 32px 80px rgba(0,0,0,0.7),0 0 80px rgba(99,60,255,0.15),0 0 0 1px rgba(99,60,255,0.08) inset;
    transform:translateY(-6px);}
/* M2 */
.cm2{background:radial-gradient(ellipse 80% 60% at 10% 20%,rgba(245,166,35,0.18) 0%,transparent 60%),
    radial-gradient(ellipse 60% 80% at 90% 80%,rgba(255,60,130,0.10) 0%,transparent 55%),
    linear-gradient(145deg,#1a1208 0%,#100c08 60%,#080608 100%);
    border:1px solid rgba(245,166,35,0.22);
    box-shadow:0 24px 60px rgba(0,0,0,0.6),0 0 0 1px rgba(255,255,255,0.04) inset;}
.cm2:hover{border-color:rgba(245,166,35,0.5);
    box-shadow:0 32px 80px rgba(0,0,0,0.7),0 0 80px rgba(245,166,35,0.12),0 0 0 1px rgba(245,166,35,0.06) inset;
    transform:translateY(-6px);}
/* Accent lines */
.cm1::before{content:'';position:absolute;top:0;left:8%;right:8%;height:1px;
    background:linear-gradient(90deg,transparent,rgba(99,60,255,0.85),transparent);
    box-shadow:0 0 16px rgba(99,60,255,0.85);}
.cm2::before{content:'';position:absolute;top:0;left:8%;right:8%;height:1px;
    background:linear-gradient(90deg,transparent,rgba(245,166,35,0.85),transparent);
    box-shadow:0 0 16px rgba(245,166,35,0.85);}
/* Glow orbs */
.glow{position:absolute;width:240px;height:240px;border-radius:50%;pointer-events:none;}
.gm1{top:-60px;right:-60px;background:radial-gradient(circle,rgba(99,60,255,0.18) 0%,transparent 70%);}
.gm2{top:-60px;left:-60px;background:radial-gradient(circle,rgba(245,166,35,0.15) 0%,transparent 70%);}
/* Watermark num */
.wm{position:absolute;right:24px;bottom:16px;font-size:110px;font-weight:900;
    line-height:1;opacity:0.05;letter-spacing:-3px;pointer-events:none;}
.wm1{color:rgba(99,60,255,1);}
.wm2{color:rgba(245,166,35,1);}
/* Icon */
.icon-box{width:46px;height:46px;border-radius:13px;display:flex;
    align-items:center;justify-content:center;font-size:20px;
    margin-bottom:16px;flex-shrink:0;}
.ib1{background:rgba(99,60,255,0.15);border:1px solid rgba(99,60,255,0.3);
     box-shadow:0 0 20px rgba(99,60,255,0.2);}
.ib2{background:rgba(245,166,35,0.12);border:1px solid rgba(245,166,35,0.25);
     box-shadow:0 0 20px rgba(245,166,35,0.18);}
/* Label */
.lbl{font-family:'Space Mono',monospace;font-size:9px;letter-spacing:3px;
    text-transform:uppercase;margin-bottom:8px;
    display:flex;align-items:center;gap:7px;}
.lbl::before{content:'';width:12px;height:1px;background:currentColor;}
.lm1{color:#818cf8;} .lm2{color:#f5a623;}
/* Title */
.ttl{font-size:34px;font-weight:800;color:#f0ecff;
    letter-spacing:-0.8px;line-height:1.05;margin-bottom:14px;}
/* Visual bars (M1) */
.bars{display:flex;gap:4px;align-items:flex-end;height:32px;margin-bottom:16px;}
.b{border-radius:2px 2px 0 0;width:9px;}
/* Dot grid (M2) */
.dgrid{display:grid;grid-template-columns:repeat(8,1fr);gap:5px;margin-bottom:16px;}
.dd{width:6px;height:6px;border-radius:50%;background:#f5a623;opacity:0.12;}
.dd.on{opacity:0.85;}
/* Stats */
.stats{display:flex;border-top:1px solid rgba(255,255,255,0.06);padding-top:14px;margin-top:auto;}
.st{flex:1;text-align:center;}
.st+.st{border-left:1px solid rgba(255,255,255,0.06);}
.sn{font-size:20px;font-weight:800;color:#f0ecff;letter-spacing:-0.5px;}
.sl{font-family:'Space Mono',monospace;font-size:8px;color:#3a3660;
    letter-spacing:1.5px;text-transform:uppercase;margin-top:2px;}
</style>"""

M1_BAR_HEIGHTS = [60,75,45,85,55,90,40,70,80,50,65,88]
M1_BARS = "".join([
    f"<div class='b' style='height:{h}%;background:linear-gradient(180deg,"
    f"rgba(99,60,255,0.9),rgba(56,189,248,0.4));'></div>"
    for h in M1_BAR_HEIGHTS
])

M2_LIT = {3,7,10,14,17,21,24,28,31,35}
M2_DOTS = "".join([
    f"<div class='dd {'on' if i in M2_LIT else ''}'></div>"
    for i in range(40)
])

card_m1_html = (
    CARD_CSS +
    "<div class='card cm1'>"
    "<div class='glow gm1'></div>"
    "<div class='wm wm1'>01</div>"
    "<div class='icon-box ib1'>📊</div>"
    "<div class='lbl lm1'>Milestone 01</div>"
    "<div class='ttl'>Data<br>Explorer</div>"
    f"<div class='bars'>{M1_BARS}</div>"
    "<div class='stats'>"
    "<div class='st'><div class='sn'>3</div><div class='sl'>Pages</div></div>"
    "<div class='st'><div class='sn'>8+</div><div class='sl'>Charts</div></div>"
    "<div class='st'><div class='sn'>CSV</div><div class='sl'>Input</div></div>"
    "</div></div>"
)

card_m2_html = (
    CARD_CSS +
    "<div class='card cm2'>"
    "<div class='glow gm2'></div>"
    "<div class='wm wm2'>02</div>"
    "<div class='icon-box ib2'>🔬</div>"
    "<div class='lbl lm2'>Milestone 02</div>"
    "<div class='ttl'>Intelligence<br>Lab</div>"
    f"<div class='dgrid'>{M2_DOTS}</div>"
    "<div class='stats'>"
    "<div class='st'><div class='sn'>35</div><div class='sl'>Users</div></div>"
    "<div class='st'><div class='sn'>4</div><div class='sl'>Sections</div></div>"
    "<div class='st'><div class='sn'>ML</div><div class='sl'>Models</div></div>"
    "</div></div>"
)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="r3">', unsafe_allow_html=True)
    components.html(card_m1_html, height=330, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="r3">', unsafe_allow_html=True)
    components.html(card_m2_html, height=330, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  ACTION BUTTONS
# ════════════════════════════════════════════════════════════════
b1, b2 = st.columns(2)
with b1:
    if st.button("▶  Open Data Explorer", key="btn_m1",
                 disabled=not M1_EXISTS):
        st.switch_page(M1_PAGE)
    if not M1_EXISTS:
        st.markdown(
            "<p style='font-family:Space Mono,monospace;font-size:9px;"
            "color:#f87171;text-align:center;margin-top:4px;'>"
            "pages/1preprocessing.py not found</p>",
            unsafe_allow_html=True
        )

with b2:
    if st.button("▶  Open Intelligence Lab", key="btn_m2",
                 disabled=not M2_EXISTS):
        st.switch_page(M2_PAGE)
    if not M2_EXISTS:
        st.markdown(
            "<p style='font-family:Space Mono,monospace;font-size:9px;"
            "color:#f87171;text-align:center;margin-top:4px;'>"
            "pages/2clustring.py not found</p>",
            unsafe_allow_html=True
        )

# ════════════════════════════════════════════════════════════════
#  STATS STRIP
# ════════════════════════════════════════════════════════════════
st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
st.markdown("""
<div class="stats-strip r5">
    <div class="ss-cell">
        <div class="ss-n">35</div>
        <div class="ss-l">Users</div>
        <div class="ss-bar" style="width:70%;background:linear-gradient(90deg,#633cff,#38bdf8);"></div>
    </div>
    <div class="ss-cell">
        <div class="ss-n">31</div>
        <div class="ss-l">Days</div>
        <div class="ss-bar" style="width:55%;background:linear-gradient(90deg,#38bdf8,#4ade80);"></div>
    </div>
    <div class="ss-cell">
        <div class="ss-n">174K</div>
        <div class="ss-l">HR Records</div>
        <div class="ss-bar" style="width:90%;background:linear-gradient(90deg,#ff3c82,#f5a623);"></div>
    </div>
    <div class="ss-cell">
        <div class="ss-n">10</div>
        <div class="ss-l">ML Features</div>
        <div class="ss-bar" style="width:45%;background:linear-gradient(90deg,#f5a623,#fcd34d);"></div>
    </div>
</div>

<div class="home-foot r5">
    <div class="foot-dot"></div>
    <div class="foot-txt">FitPulse · 2016 Fitbit · 2026</div>
    <div class="foot-dot"></div>
</div>
""", unsafe_allow_html=True)