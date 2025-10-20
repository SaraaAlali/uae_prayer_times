from datetime import datetime
from utils import UAE_CITIES, fetch_month_calendar, today_row

def choose_city():
    print("Available UAE cities:")
    print(", ".join(UAE_CITIES))
    city = input("Select a city: ").strip()
    mapping = {
        "rak": "Ras Al Khaimah",
        "ras al khaimah": "Ras Al Khaimah",
        "um al qwain": "Umm Al Quwain",
        "umm al qwain": "Umm Al Quwain",
        "al ain": "Al Ain",
    }
    low = city.lower()
    return mapping.get(low, city.title())

def choose_mode():
    mode = input("Show (T)oday or (M)onth? [T/M]: ").strip().lower()
    return "month" if mode.startswith("m") else "today"

def main():
    print("=== UAE Prayer Times ===")
    city = choose_city()
    now = datetime.now()
    month, year = now.month, now.year

    try:
        df = fetch_month_calendar(city, month, year)
    except Exception as e:
        print("Error fetching data:", e)
        return

    if df.empty:
        print("No data returned. Please retry or check city spelling.")
        return

    mode = choose_mode()
    if mode == "today":
        row = today_row(df)
        print(f"\nPrayer times for {city} — {row['Date'].strftime('%d %b %Y')}")
        for col in ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]:
            print(f"{col:8}: {row[col]}")
    else:
        print(f"\nMonthly prayer times for {city} — {now.strftime('%B %Y')}")
        print(df.to_string(index=False, formatters={'Date': lambda d: d.strftime('%d-%m-%Y')}))

if __name__ == "__main__":
    main()
