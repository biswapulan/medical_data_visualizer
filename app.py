import streamlit as st
import medical_data_visualizer
import pandas as pd
import numpy as np
import base64
import os

# ── Helper: load a local JPG/PNG and convert to base64 for HTML embedding ──
def img_to_base64(path: str) -> str | None:
    """Returns a base64 data-URI string for a local image file, or None if not found."""
    if not path or not os.path.exists(path):
        return None
    ext = os.path.splitext(path)[1].lower().replace(".", "")
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(ext, "jpeg")
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/{mime};base64,{data}"

# ══════════════════════════════════════════════
#  PAGE CONFIG  ← must be the very first call
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="MediViz | Minor Project",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.dialog("System Notice")
def under_construction_dialog():
    st.markdown(
"""<div style="
background: linear-gradient(160deg, #060d1a, #0b1320);
border: 1px solid rgba(0,229,255,0.35);
border-radius: 16px;
padding: 22px 24px;
box-shadow: 0 0 28px rgba(0,229,255,0.18);
">

<div style="
font-family:'Rajdhani',sans-serif;
font-size:20px;
font-weight:700;
color:#00e5ff;
margin-bottom:8px;
text-shadow:0 0 14px rgba(0,229,255,.4);
">
🚧 Website Under Development
</div>

<div style="
font-family:'DM Sans',sans-serif;
font-size:14px;
color:rgba(180,210,255,.75);
line-height:1.7;
">
Some features may be incomplete or subject to change.<br>
Please interpret results with appropriate discretion.
</div>

</div>""",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.2, 2, 1.2])
    with col2:
        if st.button("✔ Proceed to Dashboard"):
            st.session_state["understood"] = True
            st.rerun()


if "understood" not in st.session_state:
    under_construction_dialog()



# ══════════════════════════════════════════════
#  GLOBAL STYLES
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

:root {
  --cyan:   #00e5ff;
  --green:  #69ff47;
  --pink:   #ff2d78;
  --gold:   #ffd166;
  --bg:     #04080f;
  --card:   #0b1320;
  --border: rgba(0,229,255,0.18);
  --glow:   0 0 24px rgba(0,229,255,0.25);
}

/* ── Base ── */
.stApp { background: var(--bg); color: #d0e8ff; font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 5px; background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--cyan); border-radius: 4px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #060d1a 0%, #04080f 100%) !important;
  border-right: 1px solid var(--border) !important;
}

/* ══════════════════════
   HERO
══════════════════════ */
.hero {
  position: relative;
  border-radius: 24px;
  border: 1px solid var(--border);
  padding: 56px 48px 48px;
  text-align: center;
  overflow: hidden;
  margin-bottom: 28px;
  background: radial-gradient(ellipse at 50% 0%, rgba(0,229,255,0.07) 0%, transparent 65%),
              linear-gradient(160deg, #060d1a 0%, #0b1320 100%);
}

/* animated scan line */
.hero::before {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 60%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0,229,255,0.06), transparent);
  animation: scan 4s linear infinite;
}
@keyframes scan { to { left: 160%; } }

/* corner brackets */
.hero::after {
  content: '';
  position: absolute;
  inset: 10px;
  border-radius: 18px;
  background: transparent;
  border: 1px solid rgba(0,229,255,0.07);
  pointer-events: none;
}

.hero-eyebrow {
  display: inline-block;
  font-family: 'Space Mono', monospace;
  font-size: 10px;
  letter-spacing: 4px;
  color: var(--cyan);
  background: rgba(0,229,255,0.08);
  border: 1px solid rgba(0,229,255,0.3);
  border-radius: 40px;
  padding: 5px 18px;
  margin-bottom: 22px;
  animation: pulse-border 2.5s ease-in-out infinite;
}
@keyframes pulse-border {
  0%,100% { box-shadow: 0 0 0 0 rgba(0,229,255,0.3); }
  50%      { box-shadow: 0 0 0 6px rgba(0,229,255,0); }
}

.hero-title {
  font-family: 'Rajdhani', sans-serif;
  font-size: clamp(36px, 6vw, 72px);
  font-weight: 700;
  line-height: 1;
  margin: 0 0 14px;
  background: linear-gradient(90deg, #00e5ff 0%, #69ff47 50%, #00e5ff 100%);
  background-size: 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradient-move 5s linear infinite;
}
@keyframes gradient-move { to { background-position: 200%; } }

.hero-sub {
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  font-weight: 300;
  color: rgba(180,210,255,0.65);
  max-width: 540px;
  margin: 0 auto 36px;
  line-height: 1.7;
}

.hero-kpis {
  display: flex;
  justify-content: center;
  gap: 48px;
  flex-wrap: wrap;
}
.hero-kpi-val {
  font-family: 'Rajdhani', sans-serif;
  font-size: 34px;
  font-weight: 700;
  color: var(--green);
  display: block;
  text-shadow: 0 0 18px rgba(105,255,71,0.45);
}
.hero-kpi-lbl {
  font-family: 'Space Mono', monospace;
  font-size: 9px;
  letter-spacing: 2.5px;
  color: rgba(180,210,255,0.45);
  text-transform: uppercase;
}

/* ══════════════════════
   METRIC CARDS
══════════════════════ */
.m-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin: 22px 0 30px;
}
.m-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 26px 18px;
  text-align: center;
  transition: transform .3s, box-shadow .3s;
  position: relative;
  overflow: hidden;
}
.m-card:hover { transform: translateY(-6px); box-shadow: var(--glow); }
.m-card .bar {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 3px;
  border-radius: 0 0 18px 18px;
}
.m-card.c1 .bar { background: linear-gradient(90deg, var(--cyan), #0080ff); }
.m-card.c2 .bar { background: linear-gradient(90deg, var(--green), #00cc77); }
.m-card.c3 .bar { background: linear-gradient(90deg, var(--pink), #ff8c00); }
.m-card.c4 .bar { background: linear-gradient(90deg, var(--gold), #ff6b35); }

.m-icon  { font-size: 26px; margin-bottom: 8px; display: block; }
.m-val {
  font-family: 'Rajdhani', sans-serif;
  font-size: 32px;
  font-weight: 700;
  color: #fff;
  display: block;
  line-height: 1;
  margin-bottom: 5px;
}
.m-lbl {
  font-family: 'Space Mono', monospace;
  font-size: 9px;
  letter-spacing: 2px;
  color: rgba(180,210,255,0.45);
  text-transform: uppercase;
}

/* ══════════════════════
   SECTION HEADINGS
══════════════════════ */
.sec-head {
  font-family: 'Rajdhani', sans-serif;
  font-size: 24px;
  font-weight: 700;
  color: var(--cyan);
  letter-spacing: 1px;
  margin-bottom: 4px;
  text-shadow: 0 0 16px rgba(0,229,255,0.35);
}
.sec-rule {
  height: 2px;
  width: 56px;
  background: linear-gradient(90deg, var(--cyan), var(--green));
  border-radius: 1px;
  margin-bottom: 22px;
}

/* ══════════════════════
   TEAM CARDS
══════════════════════ */
.team-wrap {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
  margin-top: 10px;
}
.t-card {
  background: linear-gradient(155deg, #0d1826, #0b1320);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 30px 20px 22px;
  width: 172px;
  text-align: center;
  transition: all .35s cubic-bezier(.34,1.56,.64,1);
  cursor: default;
}
.t-card:hover {
  transform: translateY(-10px) scale(1.04);
  border-color: var(--cyan);
  box-shadow: 0 22px 48px rgba(0,229,255,0.18), 0 0 0 1px rgba(0,229,255,0.25);
}
.t-avatar {
  width: 82px; height: 82px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--cyan), var(--green));
  margin: 0 auto 14px;
  display: flex; align-items: center; justify-content: center;
  font-size: 34px;
  box-shadow: 0 0 22px rgba(0,229,255,0.3);
  overflow: hidden;
}
.t-avatar img { width:100%; height:100%; object-fit:cover; border-radius:50%; }
.t-name {
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 14px;
  color: #e0f0ff;
  margin-bottom: 4px;
}
.t-role {
  font-family: 'Space Mono', monospace;
  font-size: 9px;
  letter-spacing: 1.5px;
  color: var(--cyan);
  text-transform: uppercase;
}
.t-contrib {
  font-family: 'DM Sans', sans-serif;
  font-size: 11px;
  color: rgba(180,210,255,0.4);
  margin-top: 8px;
}

/* ══════════════════════
   GLASS CARD
══════════════════════ */
.glass-card {
  background: rgba(11,19,32,0.85);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 26px;
  backdrop-filter: blur(8px);
}

/* ══════════════════════
   TAGS
══════════════════════ */
.tag {
  display: inline-block;
  font-family: 'Space Mono', monospace;
  font-size: 10px;
  letter-spacing: 1px;
  padding: 4px 12px;
  border-radius: 20px;
  margin: 3px;
}
.tag-b { background:rgba(0,229,255,.1);  border:1px solid rgba(0,229,255,.35); color:var(--cyan); }
.tag-g { background:rgba(105,255,71,.1); border:1px solid rgba(105,255,71,.35); color:var(--green); }
.tag-p { background:rgba(255,45,120,.1); border:1px solid rgba(255,45,120,.35); color:var(--pink); }
.tag-y { background:rgba(255,209,102,.1);border:1px solid rgba(255,209,102,.35); color:var(--gold); }

/* ══════════════════════
   INFO BOX
══════════════════════ */
.info-box {
  background: rgba(0,229,255,.05);
  border-left: 3px solid var(--cyan);
  border-radius: 0 12px 12px 0;
  padding: 14px 18px;
  margin-top: 16px;
  font-size: 13px;
  color: rgba(180,210,255,.8);
  line-height: 1.6;
}

/* ══════════════════════
   PLOT BOX
══════════════════════ */
.plot-box {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 28px;
  margin: 18px 0;
}

/* ══════════════════════
   TYPING (sidebar)
══════════════════════ */
.typing {
  font-family: 'Space Mono', monospace;
  font-size: 11px;
  color: var(--green) !important;
  border-right: 2px solid var(--green);
  white-space: nowrap;
  overflow: hidden;
  animation: type 3.5s steps(28,end) infinite, blink .7s step-end infinite;
  max-width: 230px;
}
@keyframes type  { 0%{width:0} 55%{width:100%} 90%{width:100%} 100%{width:0} }
@keyframes blink { from,to{border-color:transparent} 50%{border-color:var(--green)} }

/* ══════════════════════
   HEARTBEAT LINE (decoration)
══════════════════════ */
.hb-wrap {
  width: 100%;
  overflow: hidden;
  height: 36px;
  margin: 6px 0 22px;
  opacity: 0.35;
}
.hb-svg { width: 100%; height: 100%; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  LOAD DATA SAFELY
# ══════════════════════════════════════════════
try:
    df = medical_data_visualizer.df
except AttributeError:
    st.error("⚠️ Could not load `df` from medical_data_visualizer.py")
    st.stop()

# ── Computed metrics ──
total_patients = len(df)

avg_age_raw = pd.to_numeric(df['age'], errors='coerce').mean() if 'age' in df.columns else None
if avg_age_raw is None or pd.isna(avg_age_raw):
    avg_age_str = "N/A"
elif avg_age_raw > 365:
    avg_age_str = str(int(avg_age_raw // 365.25))
else:
    avg_age_str = str(int(round(avg_age_raw)))

high_chol    = int(df[df['cholesterol'] > 0].shape[0]) if 'cholesterol' in df.columns else 0
cardio_cases = int(df['cardio'].sum())                  if 'cardio'      in df.columns else 0
cardio_pct   = round(cardio_cases / total_patients * 100, 1) if total_patients else 0


# ══════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:22px 0 12px">
      <div style="font-family:'Rajdhani',sans-serif;font-size:26px;font-weight:700;
                  background:linear-gradient(90deg,#00e5ff,#69ff47);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                  line-height:1;">🫀 MEDI<span style="-webkit-text-fill-color:#69ff47">VIZ</span></div>
      <div style="font-family:'Space Mono',monospace;font-size:9px;
                  color:rgba(180,210,255,.35);letter-spacing:3px;margin-top:5px;">
        MINOR PROJECT · 2025
      </div>
    </div>
    <hr style="border-color:rgba(0,229,255,.12);margin:4px 0 18px">
    """, unsafe_allow_html=True)

    st.markdown('<div class="typing">▶ Analyzing patient data...</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    page = st.selectbox("📂 Section", [
        "🏠  Home",
        "👥  Our Team",
        "📊  Categorical Plot",
        "🌡️  Heat Map",
        "🔬  Data Explorer",
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:rgba(0,229,255,.05);border:1px solid rgba(0,229,255,.18);
                border-radius:12px;padding:14px 16px;font-size:12px;
                color:rgba(180,210,255,.7);line-height:1.8;font-family:'DM Sans',sans-serif;">
      <div style="color:var(--cyan);font-family:'Space Mono',monospace;
                  font-size:10px;letter-spacing:1px;margin-bottom:6px;">📌 QUICK STATS</div>
      👥 <b style="color:#fff">{total_patients:,}</b> patients<br>
      🫀 <b style="color:#ff2d78">{cardio_pct}%</b> CVD positive<br>
      🎂 Avg age <b style="color:#69ff47">{avg_age_str} yrs</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Space Mono',monospace;font-size:9px;
                color:rgba(180,210,255,.25);text-align:center;letter-spacing:1.5px;line-height:2;">
      PYTHON · PANDAS · SEABORN<br>MATPLOTLIB · STREAMLIT<br>
      <span style="color:rgba(0,229,255,.25);">── ── ── ── ── ──</span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  HEARTBEAT DECORATION (reusable)
# ══════════════════════════════════════════════════════════
HEARTBEAT = """
<div class="hb-wrap">
  <svg class="hb-svg" viewBox="0 0 800 36" preserveAspectRatio="none">
    <polyline points="0,18 80,18 100,4 115,32 130,18 160,18 170,2 180,34 190,18 260,18
                      280,4 295,32 310,18 340,18 350,2 360,34 370,18 440,18
                      460,4 475,32 490,18 520,18 530,2 540,34 550,18 620,18
                      640,4 655,32 670,18 700,18 710,2 720,34 730,18 800,18"
          fill="none" stroke="#00e5ff" stroke-width="1.5" stroke-linejoin="round"/>
  </svg>
</div>
"""


# ══════════════════════════════════════════════════════════
#  PAGE: HOME
# ══════════════════════════════════════════════════════════
if page == "🏠  Home":

    st.markdown(f"""
    <div class="hero">
      <div class="hero-eyebrow">🩺 MINOR PROJECT &nbsp;·&nbsp; MEDICAL DATA SCIENCE &nbsp;·&nbsp; 2025</div>
      <div class="hero-title">MediViz Dashboard</div>
      <div class="hero-sub">
        Visualizing cardiovascular disease patterns from 70,000+ real-world medical records
        using Python, statistical analysis, and interactive data science tools.
      </div>
      <div class="hero-kpis">
        <div><span class="hero-kpi-val">{total_patients:,}</span><span class="hero-kpi-lbl">Patients</span></div>
        <div><span class="hero-kpi-val">12</span><span class="hero-kpi-lbl">Features</span></div>
        <div><span class="hero-kpi-val">{cardio_pct}%</span><span class="hero-kpi-lbl">CVD Rate</span></div>
        <div><span class="hero-kpi-val">5</span><span class="hero-kpi-lbl">Team Members</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(HEARTBEAT, unsafe_allow_html=True)

    # ── Metric cards ──
    st.markdown(f"""
    <div class="m-grid">
      <div class="m-card c1"><span class="bar"></span>
        <span class="m-icon">👥</span>
        <span class="m-val">{total_patients:,}</span>
        <span class="m-lbl">Total Patients</span>
      </div>
      <div class="m-card c2"><span class="bar"></span>
        <span class="m-icon">🎂</span>
        <span class="m-val">{avg_age_str}</span>
        <span class="m-lbl">Avg Age (Yrs)</span>
      </div>
      <div class="m-card c3"><span class="bar"></span>
        <span class="m-icon">🧪</span>
        <span class="m-val">{high_chol:,}</span>
        <span class="m-lbl">High Cholesterol</span>
      </div>
      <div class="m-card c4"><span class="bar"></span>
        <span class="m-icon">🫀</span>
        <span class="m-val">{cardio_pct}%</span>
        <span class="m-lbl">Cardio Positive</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Project overview ──
    st.markdown("""
    <div class="glass-card" style="margin:10px 0 24px">
      <div class="sec-head">📌 Project Overview</div>
      <div class="sec-rule"></div>
      <p style="font-size:14px;color:rgba(180,210,255,.75);line-height:1.85;margin:0 0 18px">
        This minor project applies <b style="color:#fff">data science</b> and
        <b style="color:#fff">statistical visualization</b> techniques on anonymized
        medical examination records. Our goal is to surface hidden correlations between
        lifestyle habits, health markers, and cardiovascular disease — contributing to
        intuition around early detection patterns.
      </p>
      <div>
        <span class="tag tag-b">Python 3</span>
        <span class="tag tag-b">Pandas</span>
        <span class="tag tag-b">NumPy</span>
        <span class="tag tag-g">Matplotlib</span>
        <span class="tag tag-g">Seaborn</span>
        <span class="tag tag-g">Streamlit</span>
        <span class="tag tag-p">Healthcare Data</span>
        <span class="tag tag-p">CVD Detection</span>
        <span class="tag tag-y">Statistics</span>
        <span class="tag tag-y">Data Visualization</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Dataset preview ──
    st.markdown('<div class="sec-head">📋 Dataset Preview</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-rule"></div>', unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True)

    with st.expander("📖 Column Reference Guide"):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
| Column | Meaning |
|---|---|
| `age` | Age in days |
| `height` | Height in cm |
| `weight` | Weight in kg |
| `ap_hi` | Systolic blood pressure |
| `ap_lo` | Diastolic blood pressure |
| `cholesterol` | 1=normal · 2=above · 3=high |
""")
        with c2:
            st.markdown("""
| Column | Meaning |
|---|---|
| `gluc` | Glucose level |
| `smoke` | Smoker (0/1) |
| `alco` | Alcohol intake (0/1) |
| `active` | Physical activity (0/1) |
| `cardio` | **CVD presence — TARGET** |
""")


# ══════════════════════════════════════════════════════════
#  PAGE: OUR TEAM
# ══════════════════════════════════════════════════════════
elif page == "👥  Our Team":

    st.markdown("""
    <div class="hero" style="padding:42px 40px 36px">
      <div class="hero-eyebrow">👨‍💻 THE BUILDERS</div>
      <div class="hero-title" style="font-size:clamp(28px,4vw,52px)">Meet Our Team</div>
      <div class="hero-sub">
        Five friends, one idea, countless hours of debugging — and this dashboard was born.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(HEARTBEAT, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════
    #  ✏️  EDIT YOUR TEAM DETAILS HERE
    #
    #  HOW TO ADD PHOTOS:
    #   Option A – Local JPG (recommended):
    #     Put photo1.jpg, photo2.jpg ... in the SAME folder as app.py
    #     Then set  "photo": "photo1.jpg"
    #
    #   Option B – Online URL:
    #     Set  "photo": "https://example.com/yourphoto.jpg"
    #
    #   No photo? Just keep  "photo": None  → emoji shows instead
    # ════════════════════════════════════════════════════════════════
    team = [
        {
            "name":    "Smruti Somyashree Parida",       # ← replace with real name
            "role":    "Team Lead",
            "emoji":   "😎",
            "contrib": "Architecture & Coordination",
            "photo":   None,               # e.g.  "photo1.jpg"  or  "https://..."
        },
        {
            "name":    "Sunayana Bal",
            "role":    "Data Engineer",
            "emoji":   "📊",
            "contrib": "Data Cleaning & EDA",
            "photo":   None,               # e.g.  "photo2.jpg"
        },
        {
            "name":    "Tanushree Pradhan",
            "role":    "Viz Developer",
            "emoji":   "📈",
            "contrib": "Charts & Plots",
            "photo":   None,               # e.g.  "photo3.jpg"
        },
        {
            "name":    "Sulekha Deo",
            "role":    "UI Designer",
            "emoji":   "🎨",
            "contrib": "Dashboard & Styling",
            "photo":   None,               # e.g.  "photo4.jpg"
        },
        {
            "name":    "Shrabani Parida",
            "role":    "Research Analyst",
            "emoji":   "🔬",
            "contrib": "Insights & Documentation",
            "photo":   None,               # e.g.  "photo5.jpg"
        },
    ]
    # ════════════════════════════════════════════

    # Build cards HTML
    cards = ""
    for m in team:
        if m["photo"]:
            # Try local file first (converts to base64 so Streamlit HTML can embed it)
            b64 = img_to_base64(m["photo"])
            src = b64 if b64 else m["photo"]  # fall back to URL if not a local path
            avatar = f'<img src="{src}" alt="{m["name"]}" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">'
        else:
            avatar = m["emoji"]
        cards += f"""
        <div class="t-card">
          <div class="t-avatar">{avatar}</div>
          <div class="t-name">{m['name']}</div>
          <div class="t-role">{m['role']}</div>
          <div class="t-contrib">{m['contrib']}</div>
        </div>"""

    st.markdown(f"""
    <div class="glass-card">
      <div class="sec-head" style="text-align:center">👥 Group Members</div>
      <div class="sec-rule" style="margin:0 auto 26px"></div>
      <div class="team-wrap">{cards}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── College + project info ──
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="glass-card">
          <div class="sec-head" style="font-size:17px">🏫 Institution</div>
          <div class="sec-rule"></div>
          <table style="font-family:'DM Sans',sans-serif;font-size:13px;
                        color:rgba(180,210,255,.75);line-height:2;width:100%;border-collapse:collapse;">
            <tr><td style="color:#00e5ff;width:40%">College</td><td>Government College Of Engineering, Keonjhar</td></tr>
            <tr><td style="color:#00e5ff">Department</td><td>CSE / IT</td></tr>
            <tr><td style="color:#00e5ff">Year</td><td>3rd Year</td></tr>
            <tr><td style="color:#00e5ff">Batch</td><td>2023 – 2027</td></tr>
            <tr><td style="color:#00e5ff">Guide</td><td>Mr. Santosh Ku. Meher · Ms. Sushmita Pradhan</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="glass-card">
          <div class="sec-head" style="font-size:17px">📁 Project Details</div>
          <div class="sec-rule"></div>
          <table style="font-family:'DM Sans',sans-serif;font-size:13px;
                        color:rgba(180,210,255,.75);line-height:2;width:100%;border-collapse:collapse;">
            <tr><td style="color:#69ff47;width:40%">Project</td><td>Medical Data Visualizer</td></tr>
            <tr><td style="color:#69ff47">Type</td><td>Minor Project</td></tr>
            <tr><td style="color:#69ff47">Domain</td><td>Healthcare + Data Science</td></tr>
            <tr><td style="color:#69ff47">Dataset</td><td>70,000 Patient Records</td></tr>
            <tr><td style="color:#69ff47">Tools</td><td>Python · Streamlit · Seaborn · Scipy · Pandas · Numpy</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    # ── Tech stack progress ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-head">⚙️ Tech Stack Proficiency</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-rule"></div>', unsafe_allow_html=True)

    techs = {
        "🐍 Python & Pandas — Data Processing":        92,
        "📊 Matplotlib & Seaborn — Visualization":     87,
        "🌐 Streamlit — Interactive Web Dashboard":     83,
        "📐 Statistical Analysis & Correlation":        78,
        "🎨 UI/UX Design & CSS Styling":                72,
    }
    for label, pct in techs.items():
        st.markdown(f"""
        <div style="font-family:'DM Sans',sans-serif;font-size:13px;
                    color:rgba(180,210,255,.75);margin-bottom:4px;display:flex;
                    justify-content:space-between;">
          <span>{label}</span>
          <span style="font-family:'Space Mono',monospace;font-size:11px;
                       color:#00e5ff;">{pct}%</span>
        </div>""", unsafe_allow_html=True)
        st.progress(pct / 100)
        st.markdown("<div style='margin-bottom:6px'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  PAGE: CATEGORICAL PLOT
# ══════════════════════════════════════════════════════════
elif page == "📊  Categorical Plot":

    st.markdown("""
    <div class="hero" style="padding:36px 40px 30px">
      <div class="hero-eyebrow">VISUALIZATION · CATEGORICAL ANALYSIS</div>
      <div class="hero-title" style="font-size:clamp(24px,3.5vw,46px)">Risk Factor Distribution</div>
      <div class="hero-sub" style="margin-bottom:0">
        How do health indicators differ between patients with and without cardiovascular disease?
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(HEARTBEAT, unsafe_allow_html=True)

    st.markdown('<div class="plot-box">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head">📊 Categorical Feature Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-rule"></div>', unsafe_allow_html=True)

    with st.spinner("🔄 Rendering chart..."):
        try:
            fig = medical_data_visualizer.draw_cat_plot()
            st.pyplot(fig, use_container_width=True)
            st.markdown("""
            <div class="info-box">
              💡 <b>Reading this chart:</b> Each bar group shows the count for a specific
              health attribute, split by cardio outcome — <b>0 = no CVD</b>, <b>1 = CVD positive</b>.
              Taller bars on the right (1) indicate that risk factor is more prevalent in CVD patients.
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Could not generate plot: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Key takeaways ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-head">🔍 Key Findings</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-rule"></div>', unsafe_allow_html=True)

    k1, k2, k3 = st.columns(3)
    for col, icon, title, body, cls in [
        (k1, "🧪", "Cholesterol", "Elevated cholesterol is significantly more common among CVD-positive patients — a primary indicator.", "c1"),
        (k2, "🏃", "Physical Activity", "Lower physical activity correlates strongly with cardiovascular disease presence in the dataset.", "c2"),
        (k3, "🚬", "Smoking & Alcohol", "While present, smoking and alcohol show moderate correlation — suggesting multi-factor causation.", "c3"),
    ]:
        col.markdown(f"""
        <div class="m-card {cls}" style="padding:22px 18px;text-align:left;height:100%">
          <span class="bar"></span>
          <div style="font-size:26px;margin-bottom:10px">{icon}</div>
          <div style="font-family:'Rajdhani',sans-serif;font-size:17px;
                      font-weight:700;color:#fff;margin-bottom:8px">{title}</div>
          <div style="font-family:'DM Sans',sans-serif;font-size:13px;
                      color:rgba(180,210,255,.7);line-height:1.6">{body}</div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  PAGE: HEAT MAP
# ══════════════════════════════════════════════════════════
elif page == "🌡️  Heat Map":

    st.markdown("""
    <div class="hero" style="padding:36px 40px 30px">
      <div class="hero-eyebrow">VISUALIZATION · CORRELATION ANALYSIS</div>
      <div class="hero-title" style="font-size:clamp(24px,3.5vw,46px)">Correlation Heat Map</div>
      <div class="hero-sub" style="margin-bottom:0">
        Pearson correlation across all health features after outlier removal.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(HEARTBEAT, unsafe_allow_html=True)

    st.markdown('<div class="plot-box">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head">🌡️ Feature Correlation Matrix</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-rule"></div>', unsafe_allow_html=True)

    with st.spinner("🔄 Computing correlations..."):
        try:
            fig = medical_data_visualizer.draw_heat_map()
            st.pyplot(fig, use_container_width=True)
            st.markdown("""
            <div class="info-box">
              💡 <b>How to read this:</b> Values close to <b>+1</b> (warm colors) mean strong
              positive correlation. Values close to <b>-1</b> (cool colors) mean inverse
              correlation. Data was cleaned to remove impossible blood pressure readings
              and extreme height/weight outliers before computation.
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Could not generate heat map: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Correlation quick-facts ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-head">📐 What the Numbers Tell Us</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-rule"></div>', unsafe_allow_html=True)

    f1, f2 = st.columns(2)
    f1.markdown("""
    <div class="glass-card">
      <div style="font-family:'DM Sans',sans-serif;font-size:13px;
                  color:rgba(180,210,255,.75);line-height:1.9">
        <b style="color:#00e5ff">Weight ↔ Height:</b> Moderate positive correlation — taller patients tend to weigh more (expected).<br><br>
        <b style="color:#69ff47">Cholesterol ↔ Glucose:</b> Mild positive link — metabolic factors often co-occur.<br><br>
        <b style="color:#ffd166">ap_hi ↔ ap_lo:</b> Strong positive — systolic and diastolic pressure move together.
      </div>
    </div>
    """, unsafe_allow_html=True)
    f2.markdown("""
    <div class="glass-card">
      <div style="font-family:'DM Sans',sans-serif;font-size:13px;
                  color:rgba(180,210,255,.75);line-height:1.9">
        <b style="color:#ff2d78">Cardio ↔ Age:</b> Notable positive correlation — older patients have higher CVD rates.<br><br>
        <b style="color:#69ff47">Active ↔ Cardio:</b> Slight negative — physically active patients less likely to have CVD.<br><br>
        <b style="color:#ffd166">Smoke/Alco ↔ Cardio:</b> Weak direct link — suggests indirect multi-variable effects.
      </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  PAGE: DATA EXPLORER
# ══════════════════════════════════════════════════════════
elif page == "🔬  Data Explorer":

    st.markdown("""
    <div class="hero" style="padding:36px 40px 30px">
      <div class="hero-eyebrow">🔬 INTERACTIVE · DATA EXPLORER</div>
      <div class="hero-title" style="font-size:clamp(24px,3.5vw,46px)">Explore the Dataset</div>
      <div class="hero-sub" style="margin-bottom:0">
        Filter by health attributes and explore the raw patient records interactively.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(HEARTBEAT, unsafe_allow_html=True)

    # ── Filters ──
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head" style="font-size:18px">🎛 Filters</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-rule"></div>', unsafe_allow_html=True)

    fc1, fc2, fc3, fc4 = st.columns(4)

    with fc1:
        cardio_f = st.selectbox("🫀 Cardio Status", ["All", "CVD Positive", "CVD Negative"])
    with fc2:
        chol_opts = st.multiselect("🧪 Cholesterol Level", [1, 2, 3],
                                   default=[1, 2, 3],
                                   format_func=lambda x: {1:"Normal", 2:"Above Normal", 3:"Well Above"}[x])
    with fc3:
        smoke_f = st.selectbox("🚬 Smoker", ["All", "Yes", "No"])
    with fc4:
        active_f = st.selectbox("🏃 Physically Active", ["All", "Yes", "No"])

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Apply filters ──
    filtered = df.copy()

    if cardio_f == "CVD Positive" and 'cardio' in df.columns:
        filtered = filtered[filtered['cardio'] == 1]
    elif cardio_f == "CVD Negative" and 'cardio' in df.columns:
        filtered = filtered[filtered['cardio'] == 0]

    if 'cholesterol' in df.columns and chol_opts:
        filtered = filtered[filtered['cholesterol'].isin(chol_opts)]

    if smoke_f == "Yes" and 'smoke' in df.columns:
        filtered = filtered[filtered['smoke'] == 1]
    elif smoke_f == "No" and 'smoke' in df.columns:
        filtered = filtered[filtered['smoke'] == 0]

    if active_f == "Yes" and 'active' in df.columns:
        filtered = filtered[filtered['active'] == 1]
    elif active_f == "No" and 'active' in df.columns:
        filtered = filtered[filtered['active'] == 0]

    shown_pct = round(len(filtered) / total_patients * 100, 1)

    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace;font-size:12px;
                color:#69ff47;margin:14px 0 8px;
                text-shadow:0 0 10px rgba(105,255,71,.35);">
      ✔ {len(filtered):,} records matched &nbsp;/&nbsp; {total_patients:,} total
      &nbsp;·&nbsp; {shown_pct}% of dataset
    </div>
    """, unsafe_allow_html=True)

    # ── Filtered data table ──
    st.dataframe(filtered, use_container_width=True, height=380)

    st.markdown("<br>", unsafe_allow_html=True)
    ea, eb = st.columns(2)

    with ea:
        st.markdown('<div class="sec-head" style="font-size:16px">📐 Numeric Summary</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-rule"></div>', unsafe_allow_html=True)
        st.dataframe(filtered.describe().round(2), use_container_width=True)

    with eb:
        st.markdown('<div class="sec-head" style="font-size:16px">🫀 Cardio Split</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-rule"></div>', unsafe_allow_html=True)
        if 'cardio' in filtered.columns and len(filtered):
            dist = filtered['cardio'].value_counts().reset_index()
            dist.columns = ['Status', 'Count']
            dist['%'] = (dist['Count'] / len(filtered) * 100).round(1)
            dist['Status'] = dist['Status'].map({0: '✅ No CVD', 1: '⚠️ CVD Positive'})
            st.dataframe(dist, use_container_width=True)
        else:
            st.info("No data to display.")


# ══════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════
st.markdown("""
<div style="text-align:center;padding:44px 0 20px;
            font-family:'Space Mono',monospace;font-size:9px;
            color:rgba(180,210,255,.2);letter-spacing:2px;line-height:2.4;">
  🫀 MEDIVIZ &nbsp;·&nbsp; MINOR PROJECT 2025<br>
  BUILT WITH PYTHON &amp; STREAMLIT &nbsp;·&nbsp; CSE / IT DEPT.<br>
  <span style="color:rgba(0,229,255,.2);">── ── ── ── ── ── ── ── ──</span>
</div>
""", unsafe_allow_html=True)


