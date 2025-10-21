import streamlit as st
from datetime import datetime
from utils import UAE_CITIES, fetch_month_calendar

st.set_page_config(page_title="UAE Prayer Times", page_icon="🕌", layout="centered")
st.title("🕌 UAE Prayer Times")

city = st.selectbox("Choose a city", UAE_CITIES, index=0)
now = datetime.now()
col1, col2 = st.columns(2)
month = col1.number_input("Month", 1, 12, now.month)
year = col2.number_input("Year", 2000, 2100, now.year)

if st.button("Load Prayer Times"):
    with st.spinner("Fetching times..."):
        df = fetch_month_calendar(city, int(month), int(year))

    if df.empty:
        st.error("No data returned. Try again.")
    else:
        df["Date"] = df["Date"].dt.strftime("%d-%m-%Y")
        st.success(f"Showing times for {city} – {int(month):02d}/{int(year)}")
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV",
                           data=csv,
                           file_name=f"{city}_{year}-{month:02d}_prayer_times.csv",
                           mime="text/csv")
