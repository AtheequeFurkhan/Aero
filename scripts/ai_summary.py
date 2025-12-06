import os
import pandas as pd
from openai import OpenAI
from datetime import datetime

def generate_ai_summary():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "AI Summary unavailable (Missing API Key)."

    client = OpenAI(api_key=api_key)
    
    csv_path = "data/history.csv"
    if not os.path.exists(csv_path):
        return "No data available."

    df = pd.read_csv(csv_path)
    today = datetime.now().strftime("%Y-%m-%d")
    today_data = df[df['date'] == today]
    
    if today_data.empty:
        return "No data collected for today yet."

    summary_text = today_data.to_string(index=False)
    
    prompt = f"""
    Here is today's weather data for multiple cities:
    {summary_text}
    
    Write a short, fun, and witty daily weather report (max 100 words). 
    Highlight the hottest city and any extreme weather. 
    Use emojis.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Generation Failed: {e}"

if __name__ == "__main__":
    print(generate_ai_summary())