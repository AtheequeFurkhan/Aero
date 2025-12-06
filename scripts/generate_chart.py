import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_charts():
    csv_path = "data/history.csv"
    if not os.path.exists(csv_path):
        return

    df = pd.read_csv(csv_path)
    # Ensure date is datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Setup Style
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="darkgrid")
    
    # Plot Temperature Trends
    sns.lineplot(data=df, x='date', y='temp', hue='city', marker="o")
    
    plt.title("Temperature Trends (Last 30 Days)")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    os.makedirs("data/charts", exist_ok=True)
    plt.savefig("data/charts/temp_trend.png")
    print("Charts generated.")

if __name__ == "__main__":
    generate_charts()