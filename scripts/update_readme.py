import pandas as pd
from datetime import datetime

# Function to generate a text-based progress bar
def create_progress_bar(value, total=100, length=10):
    filled_length = int(length * value // total)
    bar = '🟦' * filled_length + '⬜' * (length - filled_length)
    return bar

def update_readme():
    csv_path = "data/history.csv"
    try:
        df = pd.read_csv(csv_path)
    except:
        print("No data found to update README.")
        return

    # Get the latest data for every city
    latest_df = df.sort_values('timestamp').groupby('city').tail(1)
    
    # 1. CALCULATE EXTREMES (Hottest & Coldest)
    hottest_row = latest_df.loc[latest_df['temp'].idxmax()]
    coldest_row = latest_df.loc[latest_df['temp'].idxmin()]
    
    # 2. GENERATE BADGES
    badges_md = ""
    for _, row in latest_df.iterrows():
        # Color logic
        color = "red" if row['temp'] > 30 else "orange" if row['temp'] > 25 else "green" if row['temp'] > 15 else "blue"
        
        # FIX: Encode spaces in city names for URLs (New York -> New%20York)
        city_url_name = row['city'].replace(" ", "%20")
        
        badges_md += f"![{row['city']}](https://img.shields.io/badge/{city_url_name}-{row['temp']}°C-{color}) "

    # 3. GENERATE TABLE
    table_md = "| 🌍 City | 🌡️ Temp | 🌤️ Condition | 💧 Humidity | 🌬️ Wind |\n|---|---|---|---|---|\n"
    
    for _, row in latest_df.iterrows():
        humidity_bar = create_progress_bar(row['humidity'], 100, 5)
        table_md += f"| **{row['city']}** | {row['temp']}°C | {row['description']} | {humidity_bar} {row['humidity']}% | {row['wind_speed']} m/s |\n"

    # 4. AI/STATS SUMMARY SECTION
    # FIX: No indentation here, otherwise Markdown treats it as a code block
    stats_md = f"""<div align="center">
  <h3>🏆 Weather Records (Live)</h3>
  <table>
    <tr>
        <td align="center">🔥 <b>Hottest City</b></td>
        <td align="center">❄️ <b>Coldest City</b></td>
    </tr>
    <tr>
        <td align="center"><b>{hottest_row['city']}</b><br>{hottest_row['temp']}°C</td>
        <td align="center"><b>{coldest_row['city']}</b><br>{coldest_row['temp']}°C</td>
    </tr>
  </table>
</div>"""

    # 5. COMPILE FINAL README
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    
    readme_content = f"""
# 🌦️ Aero: Automated Weather Insight Log

> **Auto-updates every 30 minutes** with real-time data for Sri Lanka 🇱🇰 and the World 🌍.

[![Daily Weather Update](https://github.com/AtheequeFurkhan/Aero/actions/workflows/weather.yml/badge.svg)](https://github.com/AtheequeFurkhan/Aero/actions/workflows/weather.yml)
[👉 **View Full Web Dashboard**](https://AtheequeFurkhan.github.io/Aero/)

---

## ⚡ Live Status (Updated: {date_now})
{badges_md}

{stats_md}

## 📊 Global Overview
{table_md}

## 📈 Temperature Trends
> Visualizing how temperature changes over the last 24 hours.
![Temperature Trend](data/charts/temp_trend.png)

---
*Built with ❤️ by [AtheequeFurkhan](https://github.com/AtheequeFurkhan) using Python & GitHub Actions.*
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("README updated successfully.")

if __name__ == "__main__":
    update_readme()