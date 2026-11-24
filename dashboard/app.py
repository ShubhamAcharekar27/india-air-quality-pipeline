from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).resolve().parents[1] / "warehouse" / "air_quality.duckdb"

QUERY = """
    SELECT
        c.city,
        f.reading_time,
        f.date_day,
        f.pm2_5,
        f.pm10,
        f.ozone,
        f.us_aqi,
        f.aqi_category
    FROM marts.fct_air_quality_hourly f
    JOIN marts.dim_city c ON f.city_key = c.city_key
"""

st.set_page_config(page_title="India Air Quality", layout="wide")


@st.cache_data(ttl=600)
def load_data() -> pd.DataFrame:
    con = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        df = con.execute(QUERY).df()
    finally:
        con.close()
    df["date_day"] = pd.to_datetime(df["date_day"])
    return df


st.title("India Air Quality Dashboard")
st.caption("Hourly readings for major Indian cities, built from the dbt star schema.")

try:
    data = load_data()
except duckdb.Error as exc:
    st.error(
        "Could not read the warehouse. Make sure the pipeline has run and that "
        "no other process (such as a running Airflow task) is writing to the database."
    )
    st.code(str(exc))
    st.stop()

if data.empty:
    st.warning("The fact table is empty. Run the pipeline first.")
    st.stop()

# ---- Sidebar filters ----
st.sidebar.header("Filters")
all_cities = sorted(data["city"].unique())
cities = st.sidebar.multiselect("Cities", all_cities, default=all_cities)

min_day = data["date_day"].min().date()
max_day = data["date_day"].max().date()
date_range = st.sidebar.date_input(
    "Date range", value=(min_day, max_day), min_value=min_day, max_value=max_day
)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_day, end_day = date_range
else:
    start_day, end_day = min_day, max_day

start_ts = pd.Timestamp(start_day)
end_ts = pd.Timestamp(end_day)

filtered = data[
    data["city"].isin(cities)
    & (data["date_day"] >= start_ts)
    & (data["date_day"] <= end_ts)
]

if filtered.empty:
    st.info("No data for the selected filters.")
    st.stop()

# ---- Latest reading per city (ignore future forecast hours and missing values) ----
now_ist = pd.Timestamp.now(tz="Asia/Kolkata").tz_localize(None)
observed = filtered[(filtered["reading_time"] <= now_ist) & filtered["us_aqi"].notna()]
latest = (
    observed.sort_values("reading_time").groupby("city").tail(1).sort_values("us_aqi", ascending=False)
)

st.subheader("Latest AQI by city")
if latest.empty:
    st.info("No past readings in the selected range.")
else:
    columns = st.columns(len(latest))
    for column, (_, row) in zip(columns, latest.iterrows()):
        column.metric(
            label=row["city"],
            value=int(row["us_aqi"]),
            help=f"{row['aqi_category']} (as of {row['reading_time']:%d %b %H:%M})",
        )

# ---- Trend chart ----
st.subheader("PM2.5 over time")
trend = filtered.pivot_table(index="reading_time", columns="city", values="pm2_5")
st.line_chart(trend)

# ---- AQI category breakdown ----
st.subheader("Hours by AQI category")
breakdown = filtered.groupby(["city", "aqi_category"]).size().unstack(fill_value=0)
st.bar_chart(breakdown)

# ---- Data table ----
with st.expander("Show data"):
    st.dataframe(
        filtered.sort_values(["city", "reading_time"]),
        use_container_width=True,
    )