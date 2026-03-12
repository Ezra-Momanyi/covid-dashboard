
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")

st.title("🌍 COVID-19 Global Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("covid19.csv")
    return df

df = load_data()

df["Central estimate"] = pd.to_numeric(df["Central estimate"], errors="coerce")
df["Confirmed COVID-19 deaths (per 100,000)"] = pd.to_numeric(
    df["Confirmed COVID-19 deaths (per 100,000)"], errors="coerce"
)

df["Size"] = df["Central estimate"].abs()

st.sidebar.header("Filters")

countries = st.sidebar.multiselect(
    "Select Countries",
    df["Entity"].unique(),
    default=df["Entity"].unique()[:8]
)

filtered_df = df[df["Entity"].isin(countries)]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Estimated Deaths",
    int(filtered_df["Central estimate"].sum())
)

col2.metric(
    "Average Deaths per 100k",
    round(filtered_df["Confirmed COVID-19 deaths (per 100,000)"].mean(),2)
)

col3.metric(
    "Countries Selected",
    filtered_df["Entity"].nunique()
)

st.markdown("---")

st.subheader("Estimated COVID-19 Deaths by Country")

fig_bar = px.bar(
    filtered_df,
    x="Entity",
    y="Central estimate",
    color="Central estimate",
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig_bar, width="stretch")

st.subheader("Top 10 Countries by Estimated Deaths")

top10 = df.nlargest(10,"Central estimate")

fig_top = px.bar(
    top10,
    x="Central estimate",
    y="Entity",
    orientation="h",
    color="Central estimate",
    color_continuous_scale="Plasma"
)

st.plotly_chart(fig_top, width="stretch")

st.subheader("Deaths per 100k vs Estimated Deaths")

fig_scatter = px.scatter(
    filtered_df,
    x="Confirmed COVID-19 deaths (per 100,000)",
    y="Central estimate",
    size="Size",
    color="Entity"
)

st.plotly_chart(fig_scatter, width="stretch")

st.subheader("Global COVID-19 Map")

fig_map = px.choropleth(
    df,
    locations="Code",
    color="Central estimate",
    hover_name="Entity",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig_map, width="stretch")

st.subheader("Dataset Explorer")

st.dataframe(filtered_df)
