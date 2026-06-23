import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Uber Drives 2016 · Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

/* ── Base ── */
html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
.stApp                       { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }

/* ── Force ALL text white so nothing is invisible ── */
.stApp, .stApp p, .stApp span, .stApp div,
.stApp label, .stApp li, .stApp td, .stApp th {
    color: #e2e8f0 !important;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 16px !important;
    padding: 20px 24px !important;
    backdrop-filter: blur(10px);
    transition: transform 0.2s;
}
[data-testid="metric-container"]:hover { transform: translateY(-3px); }

/* Metric label */
[data-testid="metric-container"] [data-testid="stMetricLabel"],
[data-testid="metric-container"] [data-testid="stMetricLabel"] p,
[data-testid="metric-container"] [data-testid="stMetricLabel"] span,
[data-testid="metric-container"] label {
    color: #94a3b8 !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
}

/* Metric value */
[data-testid="metric-container"] [data-testid="stMetricValue"],
[data-testid="metric-container"] [data-testid="stMetricValue"] *  {
    color: #ffffff !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Metric delta */
[data-testid="metric-container"] [data-testid="stMetricDelta"],
[data-testid="metric-container"] [data-testid="stMetricDelta"] * {
    color: #68d391 !important;
    -webkit-text-fill-color: #68d391 !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(10, 8, 35, 0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.1) !important;
}
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] p {
    color: #e2e8f0 !important;
}
/* Sidebar select boxes & sliders */
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stSlider {
    color: #ffffff !important;
}

/* ── Headings ── */
h1, h2, h3, h4 { color: #ffffff !important; }

/* ── Dashboard title (plain white — no webkit clip trick) ── */
.dashboard-title {
    font-size: 2.4rem;
    font-weight: 700;
    color: #ffffff !important;
    text-shadow: 0 0 30px rgba(102,126,234,0.6), 0 0 60px rgba(240,147,251,0.3);
    margin-bottom: 0;
}
.dashboard-subtitle {
    color: #94a3b8 !important;
    font-size: 0.95rem;
    margin-top: 4px;
}

/* ── Section titles ── */
.section-title {
    color: #ffffff !important;
    font-size: 1.0rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 6px 0 14px;
    border-bottom: 2px solid rgba(102,126,234,0.6);
    margin-bottom: 20px;
}

/* ── Dividers ── */
hr { border-color: rgba(255,255,255,0.1) !important; }

/* ── Expander ── */
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span {
    color: #e2e8f0 !important;
    font-weight: 600;
}

/* ── Scrollbar ── */
::-webkit-scrollbar            { width: 6px; }
::-webkit-scrollbar-track      { background: transparent; }
::-webkit-scrollbar-thumb      { background: rgba(255,255,255,0.2); border-radius: 4px; }

/* ── Selectbox text — dropdown fix ── */
.stSelectbox [data-baseweb="select"] *,
.stSelectbox [data-baseweb="select"] span,
.stSelectbox [data-baseweb="select"] div,
div[data-baseweb="select"] > div,
div[data-baseweb="select"] > div > div,
div[data-baseweb="select"] > div span {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background: transparent !important;
}
/* Dropdown popup options */
[data-baseweb="popover"] *,
[data-baseweb="menu"] *,
[role="listbox"] *,
[role="option"] * {
    background-color: #1e1b4b !important;
    color: #e2e8f0 !important;
    -webkit-text-fill-color: #e2e8f0 !important;
}
[role="option"]:hover { background-color: rgba(102,126,234,0.35) !important; }

/* ── Top header toolbar (Deploy bar) ── */
[data-testid="stHeader"],
header[data-testid="stHeader"] {
    background: linear-gradient(135deg, #0f0c29, #302b63) !important;
    border-bottom: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="stHeader"] * {
    color: #e2e8f0 !important;
}
/* Deploy button */
[data-testid="stHeader"] button,
[data-testid="stHeader"] [data-testid="stToolbar"] button {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}
[data-testid="stHeader"] button:hover {
    background: rgba(102,126,234,0.3) !important;
}
/* Toolbar icons */
[data-testid="stToolbar"] svg,
[data-testid="stHeader"] svg {
    fill: #94a3b8 !important;
    stroke: #94a3b8 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Data Loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("My Uber Drives - 2016.csv")
    df = df[df["START_DATE*"] != "Totals"].dropna(subset=["START_DATE*"])
    df["START_DATE*"] = pd.to_datetime(df["START_DATE*"], format="mixed")
    df["END_DATE*"]   = pd.to_datetime(df["END_DATE*"],   format="mixed", errors="coerce")
    df["MILES*"]      = pd.to_numeric(df["MILES*"], errors="coerce")
    df["month_num"]   = df["START_DATE*"].dt.month
    df["month_name"]  = df["START_DATE*"].dt.strftime("%b")
    df["day_name"]    = df["START_DATE*"].dt.day_name()
    df["hour"]        = df["START_DATE*"].dt.hour
    df["duration_min"] = (df["END_DATE*"] - df["START_DATE*"]).dt.total_seconds() / 60
    df["speed_mph"]   = (df["MILES*"] / (df["duration_min"] / 60)).clip(0, 120)
    df["PURPOSE*"]    = df["PURPOSE*"].fillna("Unspecified")
    return df

df_all = load_data()

# ── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ Filters")
    st.markdown("---")

    categories = ["All"] + sorted(df_all["CATEGORY*"].dropna().unique().tolist())
    sel_cat = st.selectbox("Trip Category", categories)

    purposes = ["All"] + sorted(df_all["PURPOSE*"].dropna().unique().tolist())
    sel_purpose = st.selectbox("Trip Purpose", purposes)

    month_range = st.slider("Month Range", 1, 12, (1, 12), format="%d")

    miles_max = float(df_all["MILES*"].quantile(0.99))
    miles_range = st.slider("Trip Distance (miles)", 0.0, miles_max, (0.0, miles_max), step=0.5)

    st.markdown("---")
    st.markdown("<small style='color:#718096'>Data: Uber Drives 2016 · 1,155 trips</small>", unsafe_allow_html=True)

# ── Apply Filters ─────────────────────────────────────────────────────────────
df = df_all.copy()
if sel_cat != "All":
    df = df[df["CATEGORY*"] == sel_cat]
if sel_purpose != "All":
    df = df[df["PURPOSE*"] == sel_purpose]
df = df[(df["month_num"] >= month_range[0]) & (df["month_num"] <= month_range[1])]
df = df[(df["MILES*"] >= miles_range[0]) & (df["MILES*"] <= miles_range[1])]

# ── Plotly theme ──────────────────────────────────────────────────────────────
PLOT_BG   = "rgba(0,0,0,0)"
PAPER_BG  = "rgba(0,0,0,0)"
FONT_CLR  = "#cbd5e0"
GRID_CLR  = "rgba(255,255,255,0.06)"
PALETTE   = ["#667eea", "#f093fb", "#4fd1c5", "#fbd38d", "#fc8181", "#68d391", "#76e4f7", "#b794f4"]

def apply_theme(fig, height=320):
    fig.update_layout(
        height=height,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=FONT_CLR, family="Inter"),
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=FONT_CLR)),
        xaxis=dict(gridcolor=GRID_CLR, zerolinecolor=GRID_CLR, tickfont=dict(color=FONT_CLR)),
        yaxis=dict(gridcolor=GRID_CLR, zerolinecolor=GRID_CLR, tickfont=dict(color=FONT_CLR)),
    )
    return fig

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<p class="dashboard-title">🚗 Uber Drives 2016</p>', unsafe_allow_html=True)
st.markdown('<p class="dashboard-subtitle">Personal trip analytics dashboard · Fort Pierce & beyond</p>', unsafe_allow_html=True)
st.markdown("---")

# ── KPI Row ───────────────────────────────────────────────────────────────────
total_trips  = len(df)
total_miles  = df["MILES*"].sum()
avg_miles    = df["MILES*"].mean()
avg_duration = df["duration_min"].median()
biz_pct      = (df["CATEGORY*"] == "Business").mean() * 100

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("🗺️ Total Trips",    f"{total_trips:,}",         f"{total_trips/df_all.__len__()*100:.0f}% of all")
c2.metric("📏 Total Miles",    f"{total_miles:,.0f} mi",   f"avg {avg_miles:.1f} mi/trip")
c3.metric("⏱️ Median Duration", f"{avg_duration:.0f} min")
c4.metric("💼 Business Trips", f"{biz_pct:.0f}%")
c5.metric("📍 Unique Routes",  f"{df[['START*','STOP*']].drop_duplicates().__len__():,}")

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Monthly + Category Donut ──────────────────────────────────────────
st.markdown('<p class="section-title">📅 Temporal Patterns</p>', unsafe_allow_html=True)
col_a, col_b = st.columns([3, 1])

with col_a:
    month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    monthly = (
        df.groupby("month_name")
          .agg(Trips=("MILES*","count"), Miles=("MILES*","sum"))
          .reindex(month_order).dropna()
          .reset_index()
    )
    fig_monthly = make_subplots(specs=[[{"secondary_y": True}]])
    fig_monthly.add_trace(
        go.Bar(x=monthly["month_name"], y=monthly["Trips"],
               name="Trips", marker_color="#667eea", opacity=0.85),
        secondary_y=False
    )
    fig_monthly.add_trace(
        go.Scatter(x=monthly["month_name"], y=monthly["Miles"],
                   name="Miles", mode="lines+markers",
                   line=dict(color="#f093fb", width=2.5),
                   marker=dict(size=7, color="#f093fb")),
        secondary_y=True
    )
    fig_monthly.update_yaxes(title_text="Trips", secondary_y=False,
                              gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR))
    fig_monthly.update_yaxes(title_text="Miles", secondary_y=True,
                              gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR))
    fig_monthly.update_layout(
        title=dict(text="Monthly Trips & Miles", font=dict(color=FONT_CLR, size=14)),
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=FONT_CLR, family="Inter"),
        height=340, margin=dict(l=10,r=10,t=40,b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.12),
        barmode="group"
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

with col_b:
    cat_counts = df["CATEGORY*"].value_counts()
    fig_donut = go.Figure(go.Pie(
        labels=cat_counts.index, values=cat_counts.values,
        hole=0.62, marker_colors=["#667eea","#f093fb"],
        textfont=dict(color=FONT_CLR),
    ))
    fig_donut.update_layout(
        title=dict(text="Category Split", font=dict(color=FONT_CLR, size=14)),
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=FONT_CLR, family="Inter"),
        height=340, margin=dict(l=10,r=10,t=40,b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=FONT_CLR)),
        annotations=[dict(text=f"{total_trips}", x=0.5, y=0.5,
                          font=dict(size=22, color="white", family="Inter"), showarrow=False)]
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# ── Row 2: Day of week heatmap + Hour distribution ───────────────────────────
st.markdown('<p class="section-title">🕐 Activity Heatmap</p>', unsafe_allow_html=True)
col_c, col_d = st.columns([1, 1])

with col_c:
    day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    day_trips = df["day_name"].value_counts().reindex(day_order).fillna(0)
    colors = ["#667eea" if d in ["Saturday","Sunday"] else "#4fd1c5" for d in day_order]
    fig_day = go.Figure(go.Bar(
        x=day_order, y=day_trips.values,
        marker=dict(color=colors, line=dict(color="rgba(0,0,0,0)")),
        text=day_trips.values.astype(int), textposition="outside",
        textfont=dict(color=FONT_CLR, size=11),
    ))
    fig_day.update_layout(
        title=dict(text="Trips by Day of Week", font=dict(color=FONT_CLR, size=14)),
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=FONT_CLR, family="Inter"),
        height=320, margin=dict(l=10,r=10,t=40,b=10),
        xaxis=dict(gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR)),
        yaxis=dict(gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR)),
    )
    st.plotly_chart(fig_day, use_container_width=True)

with col_d:
    hour_trips = df["hour"].value_counts().sort_index()
    all_hours  = pd.Series(0, index=range(24))
    all_hours.update(hour_trips)
    hour_colors = ["#f093fb" if h in [7,8,9,16,17,18] else "#667eea" for h in range(24)]
    fig_hour = go.Figure(go.Bar(
        x=list(range(24)), y=all_hours.values,
        marker=dict(color=hour_colors),
        hovertemplate="Hour %{x}:00 · %{y} trips<extra></extra>",
    ))
    fig_hour.update_layout(
        title=dict(text="Trips by Hour (pink = rush hours)", font=dict(color=FONT_CLR, size=14)),
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=FONT_CLR, family="Inter"),
        height=320, margin=dict(l=10,r=10,t=40,b=10),
        xaxis=dict(gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR),
                   tickvals=list(range(0,24,3)),
                   ticktext=[f"{h:02d}:00" for h in range(0,24,3)]),
        yaxis=dict(gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR)),
    )
    st.plotly_chart(fig_hour, use_container_width=True)

# ── Row 3: Purpose breakdown + Distance histogram ─────────────────────────────
st.markdown('<p class="section-title">🎯 Purpose & Distance</p>', unsafe_allow_html=True)
col_e, col_f = st.columns([1, 1])

with col_e:
    purpose_data = (
        df[df["PURPOSE*"] != "Unspecified"]
          .groupby("PURPOSE*")
          .agg(Trips=("MILES*","count"), Miles=("MILES*","sum"))
          .sort_values("Trips", ascending=True)
    )
    fig_purpose = go.Figure(go.Bar(
        y=purpose_data.index,
        x=purpose_data["Trips"],
        orientation="h",
        marker=dict(
            color=purpose_data["Trips"],
            colorscale=[[0,"#302b63"],[0.5,"#667eea"],[1,"#f093fb"]],
            showscale=False,
        ),
        text=purpose_data["Trips"], textposition="outside",
        textfont=dict(color=FONT_CLR),
    ))
    fig_purpose.update_layout(
        title=dict(text="Trips by Purpose", font=dict(color=FONT_CLR, size=14)),
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=FONT_CLR, family="Inter"),
        height=340, margin=dict(l=10,r=10,t=40,b=10),
        xaxis=dict(gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR)),
        yaxis=dict(gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR)),
    )
    st.plotly_chart(fig_purpose, use_container_width=True)

with col_f:
    miles_clipped = df[df["MILES*"] <= 80]["MILES*"]
    fig_hist = go.Figure(go.Histogram(
        x=miles_clipped, nbinsx=40,
        marker=dict(
            color="#667eea",
            line=dict(color="#302b63", width=0.5),
        ),
        opacity=0.85,
        hovertemplate="Miles: %{x:.1f} · Count: %{y}<extra></extra>",
    ))
    fig_hist.add_vline(x=miles_clipped.median(), line_color="#f093fb", line_dash="dash",
                       annotation_text=f"Median {miles_clipped.median():.1f} mi",
                       annotation_font_color="#f093fb")
    fig_hist.update_layout(
        title=dict(text="Distance Distribution (≤80 mi)", font=dict(color=FONT_CLR, size=14)),
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=FONT_CLR, family="Inter"),
        height=340, margin=dict(l=10,r=10,t=40,b=10),
        xaxis=dict(title="Miles", gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR)),
        yaxis=dict(title="Trips", gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR)),
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# ── Row 4: Top locations + Miles by purpose ───────────────────────────────────
st.markdown('<p class="section-title">📍 Locations & Miles</p>', unsafe_allow_html=True)
col_g, col_h = st.columns([1, 1])

with col_g:
    top_starts = (
        df[df["START*"] != "Unknown Location"]["START*"]
          .value_counts().head(10).sort_values()
    )
    fig_loc = go.Figure(go.Bar(
        y=top_starts.index, x=top_starts.values,
        orientation="h",
        marker=dict(color="#4fd1c5"),
        text=top_starts.values, textposition="outside",
        textfont=dict(color=FONT_CLR),
    ))
    fig_loc.update_layout(
        title=dict(text="Top 10 Start Locations", font=dict(color=FONT_CLR, size=14)),
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=FONT_CLR, family="Inter"),
        height=360, margin=dict(l=10,r=10,t=40,b=10),
        xaxis=dict(gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR)),
        yaxis=dict(gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR)),
    )
    st.plotly_chart(fig_loc, use_container_width=True)

with col_h:
    miles_purpose = (
        df[df["PURPOSE*"] != "Unspecified"]
          .groupby("PURPOSE*")["MILES*"].sum()
          .sort_values(ascending=False).head(8)
    )
    fig_miles_p = go.Figure(go.Pie(
        labels=miles_purpose.index, values=miles_purpose.values,
        hole=0.45, marker_colors=PALETTE,
        textfont=dict(color="#ffffff", size=11),
    ))
    fig_miles_p.update_layout(
        title=dict(text="Total Miles by Purpose", font=dict(color=FONT_CLR, size=14)),
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=FONT_CLR, family="Inter"),
        height=360, margin=dict(l=10,r=10,t=40,b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=FONT_CLR, size=10)),
    )
    st.plotly_chart(fig_miles_p, use_container_width=True)

# ── Row 5: Cumulative miles line ──────────────────────────────────────────────
st.markdown('<p class="section-title">📈 Cumulative Miles Over Time</p>', unsafe_allow_html=True)
cum_df = df.sort_values("START_DATE*").copy()
cum_df["cumulative_miles"] = cum_df["MILES*"].cumsum()
fig_cum = go.Figure()
fig_cum.add_trace(go.Scatter(
    x=cum_df["START_DATE*"], y=cum_df["cumulative_miles"],
    mode="lines",
    line=dict(color="#667eea", width=2.5),
    fill="tozeroy",
    fillcolor="rgba(102,126,234,0.12)",
    hovertemplate="%{x|%b %d} · %{y:,.0f} total miles<extra></extra>",
))
fig_cum.update_layout(
    paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
    font=dict(color=FONT_CLR, family="Inter"),
    height=280, margin=dict(l=10,r=10,t=20,b=10),
    xaxis=dict(gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR)),
    yaxis=dict(gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR), title="Cumulative Miles"),
)
st.plotly_chart(fig_cum, use_container_width=True)

# ── Footer raw data ───────────────────────────────────────────────────────────
with st.expander("🔍 View Raw Data"):
    st.dataframe(
        df[["START_DATE*","CATEGORY*","START*","STOP*","MILES*","PURPOSE*","duration_min"]]
          .rename(columns={
              "START_DATE*":"Date","CATEGORY*":"Category",
              "START*":"From","STOP*":"To","MILES*":"Miles",
              "PURPOSE*":"Purpose","duration_min":"Duration (min)"
          })
          .sort_values("Date", ascending=False)
          .style.background_gradient(subset=["Miles"], cmap="Purples"),
        height=350,
        use_container_width=True,
    )

st.markdown("---")
st.markdown(
    "<center><small style='color:#4a5568'>Built with Streamlit & Plotly · Uber Drives 2016 Dataset</small></center>",
    unsafe_allow_html=True
)
#python -m streamlit run app.py