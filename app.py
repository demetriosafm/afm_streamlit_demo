import math
import random
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="AFM Executive Dashboard Mockup",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0b1020 0%, #111827 35%, #0f172a 100%);
    }
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.92);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }
    .hero {
        padding: 1.35rem 1.5rem;
        border-radius: 22px;
        background: linear-gradient(135deg, rgba(59,130,246,0.18), rgba(168,85,247,0.18));
        border: 1px solid rgba(255,255,255,0.10);
        box-shadow: 0 10px 30px rgba(0,0,0,0.20);
        margin-bottom: 1.25rem;
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.2rem;
    }
    .hero-subtitle {
        font-size: 0.98rem;
        color: #cbd5e1;
    }
    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0.2rem 0 0.8rem 0;
    }
    .metric-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 1rem 1rem 0.9rem 1rem;
        border-radius: 18px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.88rem;
        margin-bottom: 0.3rem;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 1.85rem;
        font-weight: 700;
        line-height: 1.05;
    }
    .metric-delta {
        color: #86efac;
        font-size: 0.88rem;
        margin-top: 0.28rem;
    }
    .panel {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 1rem 1rem 0.5rem 1rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.16);
    }
    div[data-baseweb="select"] > div {
        background-color: rgba(255,255,255,0.04);
    }
</style>
""", unsafe_allow_html=True)

random.seed(7)
np.random.seed(7)

months = pd.date_range("2025-04-01", periods=12, freq="MS")
month_labels = [d.strftime("%b %Y") for d in months]

audience_segments = ["All Audience", "High Value Buyers", "Email Engaged", "Live Event Fans", "Lapsed Customers"]
brands = ["Almost Friday", "Friday Beers", "Friday Sports", "Merch"]

base_revenue = np.array([185, 198, 205, 224, 236, 248, 261, 279, 295, 318, 334, 351]) * 1000
segment_multipliers = {
    "All Audience": 1.00,
    "High Value Buyers": 0.48,
    "Email Engaged": 0.61,
    "Live Event Fans": 0.43,
    "Lapsed Customers": 0.22
}

composition_df = pd.DataFrame({
    "Segment": ["Shopify Purchasers", "Klaviyo Subscribers", "Eventbrite Attendees", "Clubhouse Members"],
    "Count": [41820, 73950, 16440, 12880]
})

cohort_names = ["Gen Z Sports", "Comedy Fans", "Podcast Fans", "NYC Nightlife", "College Audience", "Premium Merch Buyers"]
cohort_df = pd.DataFrame({
    "Cohort": cohort_names,
    "Engagement Rate": [42, 58, 49, 37, 46, 64],
    "Avg Spend": [74, 96, 82, 61, 69, 138],
    "Audience": [9200, 11800, 8700, 6300, 10100, 5200]
})

social_accounts = ["@almostfridaymedia", "@fridaybeers", "@fridaysports", "@afm.events"]
platforms = ["Instagram", "TikTok", "YouTube", "X"]
platform_weights = {
    "@almostfridaymedia": [1.0, 0.95, 0.75, 0.50],
    "@fridaybeers": [1.1, 1.0, 0.8, 0.55],
    "@fridaysports": [0.85, 0.9, 1.05, 0.70],
    "@afm.events": [0.65, 0.55, 0.45, 0.30]
}

city_points = [
    ("Los Angeles", 34.0522, -118.2437, "West", 128000),
    ("New York", 40.7128, -74.0060, "Northeast", 121000),
    ("Chicago", 41.8781, -87.6298, "Midwest", 76000),
    ("Austin", 30.2672, -97.7431, "South", 69000),
    ("Miami", 25.7617, -80.1918, "South", 72000),
    ("Atlanta", 33.7490, -84.3880, "South", 64000),
    ("Phoenix", 33.4484, -112.0740, "West", 52000),
    ("Seattle", 47.6062, -122.3321, "West", 58000),
    ("Denver", 39.7392, -104.9903, "West", 47000),
    ("Nashville", 36.1627, -86.7816, "South", 44000),
    ("Boston", 42.3601, -71.0589, "Northeast", 54000),
    ("Dallas", 32.7767, -96.7970, "South", 61000)
]

trend_rows = []
for account in social_accounts:
    weights = platform_weights[account]
    for platform, mult in zip(platforms, weights):
        base = np.linspace(180, 340, len(month_labels)) * mult
        noise = np.random.normal(0, 12, len(month_labels))
        values = np.maximum(40, base + noise).round().astype(int)
        for m, v in zip(month_labels, values):
            trend_rows.append([account, platform, m, v])
social_trend_df = pd.DataFrame(trend_rows, columns=["Account", "Platform", "Month", "Engagement Index"])

st.markdown("""
<div class="hero">
    <div class="hero-title">AFM Executive Dashboard Mockup</div>
    <div class="hero-subtitle">Screenshot-oriented Streamlit demo with fake Customer 360 and social media data</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## Controls")
    selected_brand = st.selectbox("Brand", brands, index=0)
    selected_segment = st.selectbox("Audience Segment", audience_segments, index=0)
    selected_account = st.selectbox("Social Account", social_accounts, index=1)
    selected_region = st.multiselect("Regions", ["West", "Northeast", "Midwest", "South"], default=["West", "Northeast", "Midwest", "South"])
    selected_platforms = st.multiselect("Platforms", platforms, default=platforms)
    st.markdown("---")
    st.caption(f"Last refreshed: {datetime.now().strftime('%b %d, %Y %I:%M %p')}")

segment_multiplier = segment_multipliers[selected_segment]
adj_revenue = (base_revenue * segment_multiplier).round(0)
audience_total = int(composition_df["Count"].sum() * segment_multiplier)
email_engagement = round(38.4 * (0.85 + segment_multiplier / 4), 1)
repeat_rate = round(24.1 * (0.80 + segment_multiplier / 3), 1)
ltv = int(112 * (0.78 + segment_multiplier / 2))

st.markdown('<div class="section-title">Customer 360 Overview</div>', unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Unified Audience</div>
        <div class="metric-value">{audience_total:,}</div>
        <div class="metric-delta">↑ 8.7% vs prior quarter</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Email Engagement Rate</div>
        <div class="metric-value">{email_engagement}%</div>
        <div class="metric-delta">↑ 2.1 pts month over month</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Repeat Purchase Rate</div>
        <div class="metric-value">{repeat_rate}%</div>
        <div class="metric-delta">↑ 1.4 pts vs last month</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Estimated LTV</div>
        <div class="metric-value">${ltv}</div>
        <div class="metric-delta">↑ 11.2% year over year</div>
    </div>
    """, unsafe_allow_html=True)

c1, c2 = st.columns([1.65, 1])

with c1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    revenue_df = pd.DataFrame({
        "Month": month_labels,
        "Revenue": adj_revenue
    })
    fig_rev = px.area(
        revenue_df,
        x="Month",
        y="Revenue",
        title=f"{selected_brand} Revenue Trend",
        markers=True
    )
    fig_rev.update_layout(
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"),
        title_font=dict(size=20),
        margin=dict(l=10, r=10, t=55, b=10),
        xaxis_title="",
        yaxis_title="Revenue"
    )
    fig_rev.update_traces(line=dict(width=3))
    st.plotly_chart(fig_rev, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    comp = composition_df.copy()
    comp["Count"] = (comp["Count"] * segment_multiplier).round(0).astype(int)
    fig_comp = px.pie(
        comp,
        names="Segment",
        values="Count",
        title="Audience Composition",
        hole=0.58
    )
    fig_comp.update_layout(
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"),
        title_font=dict(size=20),
        margin=dict(l=10, r=10, t=55, b=10),
        legend_title=""
    )
    st.plotly_chart(fig_comp, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

c3, c4 = st.columns([1.15, 1.5])

with c3:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    fig_scatter = px.scatter(
        cohort_df,
        x="Engagement Rate",
        y="Avg Spend",
        size="Audience",
        text="Cohort",
        title="Audience Cohort Quality",
        size_max=48
    )
    fig_scatter.update_traces(textposition="top center")
    fig_scatter.update_layout(
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"),
        title_font=dict(size=20),
        margin=dict(l=10, r=10, t=55, b=10)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    heatmap_rows = []
    for channel in ["Email", "SMS", "Paid Social", "Organic Social", "Live Events"]:
        vals = np.random.randint(22, 96, size=5)
        for i, bucket in enumerate(["18-24", "25-34", "35-44", "45-54", "55+"]):
            heatmap_rows.append([channel, bucket, vals[i]])
    heatmap_df = pd.DataFrame(heatmap_rows, columns=["Channel", "Age Band", "Index"])
    heatmap_matrix = heatmap_df.pivot(index="Channel", columns="Age Band", values="Index")
    fig_heat = go.Figure(data=go.Heatmap(
        z=heatmap_matrix.values,
        x=heatmap_matrix.columns,
        y=heatmap_matrix.index,
        text=heatmap_matrix.values,
        texttemplate="%{text}",
        hoverongaps=False
    ))
    fig_heat.update_layout(
        title="Engagement Index by Channel and Age Band",
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"),
        title_font=dict(size=20),
        margin=dict(l=10, r=10, t=55, b=10),
        xaxis_title="",
        yaxis_title=""
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")
st.markdown('<div class="section-title">Social Media Performance</div>', unsafe_allow_html=True)

account_factor = {
    "@almostfridaymedia": 1.00,
    "@fridaybeers": 1.18,
    "@fridaysports": 0.92,
    "@afm.events": 0.72
}[selected_account]

social_reach = int(3_240_000 * account_factor)
engagements = int(286_000 * account_factor)
video_views = int(5_820_000 * account_factor)
followers = int(912_000 * account_factor)

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Reach</div>
        <div class="metric-value">{social_reach:,}</div>
        <div class="metric-delta">↑ 13.4% in last 30 days</div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Engagements</div>
        <div class="metric-value">{engagements:,}</div>
        <div class="metric-delta">↑ 7.8% vs prior period</div>
    </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Video Views</div>
        <div class="metric-value">{video_views:,}</div>
        <div class="metric-delta">↑ 16.1% month over month</div>
    </div>
    """, unsafe_allow_html=True)

with s4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Followers</div>
        <div class="metric-value">{followers:,}</div>
        <div class="metric-delta">↑ 4.2% net growth</div>
    </div>
    """, unsafe_allow_html=True)

map_df = pd.DataFrame(city_points, columns=["City", "Lat", "Lon", "Region", "BaseReach"])
map_df["Reach"] = (map_df["BaseReach"] * account_factor * np.random.uniform(0.9, 1.1, len(map_df))).round(0).astype(int)
map_df["Engagement Rate"] = np.round(np.random.uniform(3.8, 8.9, len(map_df)), 1)
map_df["Posts"] = np.random.randint(8, 28, len(map_df))
map_df = map_df[map_df["Region"].isin(selected_region)].copy()
map_df["BubbleSize"] = map_df["Reach"] / 2500

trend_filtered = social_trend_df[
    (social_trend_df["Account"] == selected_account) &
    (social_trend_df["Platform"].isin(selected_platforms))
].copy()

m1, m2 = st.columns([1.5, 1.1])

with m1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    fig_map = px.scatter_mapbox(
        map_df,
        lat="Lat",
        lon="Lon",
        size="BubbleSize",
        color="Engagement Rate",
        hover_name="City",
        hover_data={
            "Lat": False,
            "Lon": False,
            "BubbleSize": False,
            "Reach": True,
            "Engagement Rate": True,
            "Posts": True,
            "Region": True
        },
        zoom=2.8,
        height=500,
        title=f"{selected_account} Audience Reach by City"
    )
    fig_map.update_layout(
        mapbox_style="carto-darkmatter",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"),
        title_font=dict(size=20),
        margin=dict(l=10, r=10, t=55, b=10)
    )
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with m2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    fig_trend = px.line(
        trend_filtered,
        x="Month",
        y="Engagement Index",
        color="Platform",
        markers=True,
        title="Platform Trend"
    )
    fig_trend.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"),
        title_font=dict(size=20),
        margin=dict(l=10, r=10, t=55, b=10),
        xaxis_title="",
        yaxis_title="Engagement Index",
        legend_title=""
    )
    fig_trend.update_traces(line=dict(width=3))
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="panel">', unsafe_allow_html=True)
top_cities = map_df.sort_values("Reach", ascending=False)[["City", "Region", "Reach", "Engagement Rate", "Posts"]].reset_index(drop=True)
top_cities.index = top_cities.index + 1
st.dataframe(top_cities, use_container_width=True, height=320)
st.markdown('</div>', unsafe_allow_html=True)