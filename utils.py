from datetime import datetime
import requests
import pandas as pd

# List of UAE cities used by app.py
UAE_CITIES = [
    "Dubai", "Abu Dhabi", "Sharjah", "Ajman",
    "Fujairah", "Ras Al Khaimah", "Umm Al Quwain", "Al Ain"
]

def fetch_month_calendar(city: str, month: int, year: int) -> pd.DataFrame:
    """
    Fetch prayer times for the whole month for a given UAE city.
    Uses Aladhan API: https://api.aladhan.com/v1/calendarByCity
    """
    url = "https://api.aladhan.com/v1/calendarByCity"
    params = {
        "city": city,
        "country": "United Arab Emirates",
        "method": 2,  # University of Islamic Sciences, Karachi
        "month": month,
        "year": year
    }

    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()

    days = []
    for item in data.get("data", []):
        date_greg = item["date"]["gregorian"]["date"]
        timings = item["timings"]
        days.append({
            "Date": date_greg,
            "Fajr": timings["Fajr"].split(" ")[0],
            "Sunrise": timings["Sunrise"].split(" ")[0],
            "Dhuhr": timings["Dhuhr"].split(" ")[0],
            "Asr": timings["Asr"].split(" ")[0],
            "Maghrib": timings["Maghrib"].split(" ")[0],
            "Isha": timings["Isha"].split(" ")[0],
        })

    df = pd.DataFrame(days)
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df = df.sort_values("Date").reset_index(drop=True)
    return df

def today_row(df: pd.DataFrame) -> pd.Series:
    """Return the row for today's date if available."""
    today = pd.Timestamp.today().normalize()
    row = df[df["Date"] == today]
    if row.empty:
        # If today isn't in data (timezone difference), get the closest date
        idx = (df["Date"] - today).abs().idxmin()
        return df.loc[idx]
    return row.iloc[0]
