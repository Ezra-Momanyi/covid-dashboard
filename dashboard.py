
import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="COVID-19 Global Dashboard", layout="wide")

st.title("🌍 COVID-19 Global Analytics Dashboard")

# ----------------------------
# LOAD DATA (CACHE FOR SPEED)
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("covid19.csv")
    return df

df = load_data()

# Ensure numeric values
df["Central estimate"] = pd.to_numeric(df["Central estimate"], errors="coerce")
df["Confirmed COVID-19 deaths (per 100,000)"] = pd.to_numeric(
    df["Confirmed COVID-19 deaths (per 100,000)"], errors="coerce"
)

# Fix negative values for marker size
df["size"] = df["Central estimate"].abs()

# ----------------------------
# SIDEBAR FILTER
# ----------------------------
st.sidebar.header("Dashboard Filters")

countries = st.sidebar.multiselect(
    "Select Countries",
    df["Entity"].unique(),
    default=df["Entity"].unique()[:8]
)

filtered_df = df[df["Entity"].isin(countries)]

# ----------------------------
# KPI SECTION
# ----------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Central Estimate",
    int(filtered_df["Central estimate"].sum())
)

col2.metric(
    "Average Deaths per 100k",
    round(filtered_df["Confirmed COVID-19 deaths (per 100,000)"].mean(), 2)
)

col3.metric(
    "Countries Selected",
    filtered_df["Entity"].nunique()
)

st.divider()

# ----------------------------
# CHART 1 – CENTRAL ESTIMATE
# ----------------------------
st.subheader("Central Estimate by Country")

fig1 = px.bar(
    filtered_df,
    x="Entity",
    y="Central estimate",
    color="Central estimate",
    height=450,
    title="Central Estimate Distribution"
)

st.plotly_chart(fig1, use_container_width=True)

# ----------------------------
# CHART 2 – TOP 10 COUNTRIES
# ----------------------------
st.subheader("Top 10 Countries by Central Estimate")

top10 = df.sort_values("Central estimate", ascending=False).head(10)

fig2 = px.bar(
    top10,
    x="Central estimate",
    y="Entity",
    orientation="h",
    color="Central estimate",
    title="Top 10 Countries"
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# CHART 3 – SCATTER COMPARISON
# ----------------------------
st.subheader("Deaths per 100k vs Central Estimate")

fig3 = px.scatter(
    df,
    x="Central estimate",
    y="Confirmed COVID-19 deaths (per 100,000)",
    size="size",
    color="Entity",
    hover_name="Entity",
    title="Deaths per 100k vs Central Estimate"
)

st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# CHART 4 – WORLD MAP
# ----------------------------
st.subheader("Global COVID-19 Impact Map")

map_fig = px.choropleth(
    df,
    locations="Entity",
    locationmode="country names",
    color="Central estimate",
    hover_name="Entity",
    color_continuous_scale="Reds",
    title="Global COVID-19 Central Estimates"
)

st.plotly_chart(map_fig, use_container_width=True)

# ----------------------------
# DATASET EXPLORER
# ----------------------------
st.subheader("Dataset Explorer")

st.dataframe(df, use_container_width=True)
