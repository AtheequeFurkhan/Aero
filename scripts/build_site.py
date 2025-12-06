import pandas as pd
import yaml
import os
from jinja2 import Template

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-white font-sans p-6">
    <div class="max-w-6xl mx-auto">
        <header class="mb-8 text-center">
            <h1 class="text-4xl font-bold mb-2">🌍 Global Weather Dashboard</h1>
            <p class="text-slate-400">Last Updated: {{ last_update }}</p>
        </header>
        
        <!-- AI Summary -->
        <div class="bg-slate-800 p-6 rounded-xl shadow-lg mb-8 border border-slate-700">
            <h2 class="text-2xl font-semibold mb-4 text-blue-400">🤖 AI Daily Brief</h2>
            <p class="text-lg leading-relaxed">{{ ai_summary }}</p>
        </div>

        <!-- Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {% for city in cities %}
            <div class="bg-slate-800 p-6 rounded-xl shadow-lg border-t-4 border-blue-500 hover:scale-105 transition-transform">
                <div class="flex justify-between items-start">
                    <h3 class="text-xl font-bold">{{ city.name }}</h3>
                    <span class="text-3xl">{{ city.icon }}</span>
                </div>
                <div class="mt-4">
                    <p class="text-4xl font-bold">{{ city.temp }}°C</p>
                    <p class="text-slate-400 capitalize">{{ city.condition }}</p>
                </div>
                <div class="mt-4 text-sm text-slate-500">
                    <p>💧 Humidity: {{ city.humidity }}%</p>
                    <p>💨 Wind: {{ city.wind }} m/s</p>
                </div>
            </div>
            {% endfor %}
        </div>

        <!-- Charts -->
        <div class="bg-white p-4 rounded-xl shadow-lg">
            <h2 class="text-2xl font-semibold mb-4 text-slate-900">📈 Temperature Trends</h2>
            <img src="./data/charts/temp_trend.png" alt="Temperature Trend" class="w-full rounded-lg">
        </div>
    </div>
</body>
</html>
"""

def build_website():
    # Load Data
    if not os.path.exists("data/history.csv"): return
    df = pd.read_csv("data/history.csv")
    
    # Get latest data per city
    latest_date = df['timestamp'].max()
    latest_df = df.sort_values('timestamp').groupby('city').tail(1)
    
    # Prepare data for template
    cities_data = []
    condition_emojis = {
        "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️", "Snow": "❄️", "Thunderstorm": "⛈️", "Drizzle": "🌦️"
    }
    
    for _, row in latest_df.iterrows():
        icon = condition_emojis.get(row['condition'], "🌫️")
        cities_data.append({
            "name": row['city'],
            "temp": row['temp'],
            "condition": row['description'],
            "humidity": row['humidity'],
            "wind": row['wind_speed'],
            "icon": icon
        })
        
    # Get AI Summary (Read from a temp file or import logic)
    # For simplicity, we just put a placeholder or call the script.
    # In production, save AI output to a text file to read here.
    from ai_summary import generate_ai_summary
    ai_text = generate_ai_summary()

    # Render
    template = Template(HTML_TEMPLATE)
    html_out = template.render(
        last_update=latest_date,
        cities=cities_data,
        ai_summary=ai_text
    )
    
    os.makedirs("public", exist_ok=True)
    with open("public/index.html", "w", encoding='utf-8') as f:
        f.write(html_out)
    
    # Copy charts to public if needed, or link relatively
    # For GitHub pages from root, we might need to adjust paths. 
    # Let's assume we deploy the root to GH pages for simplicity.

if __name__ == "__main__":
    build_website()