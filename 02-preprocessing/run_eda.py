import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = '01-data/TSC_clean.csv'

try:
    print(f"Loading {file_path}...")
    df = pd.read_csv(file_path)
    
    # Convert START_DATE to datetime
    print("Converting START_DATE to datetime...")
    df['START_DATE'] = pd.to_datetime(df['START_DATE'])
    df_sorted = df.sort_values('START_DATE')
    
    # Plotting Time Series
    print("Generating Time Series plot...")
    fig, ax1 = plt.subplots(figsize=(20, 8))

    # Plot Speed
    color_speed = 'tab:blue'
    ax1.set_xlabel('Time (START_DATE)')
    ax1.set_ylabel('Casting Speed (m/min)', color=color_speed)
    ax1.plot(df_sorted['START_DATE'], df_sorted['speed'], color=color_speed, linewidth=0.5, label='Speed')
    ax1.tick_params(axis='y', labelcolor=color_speed)

    # Secondary Axis for Temperature
    ax2 = ax1.twinx()
    color_temp = 'tab:red'
    ax2.set_ylabel('Temperature (°C)', color=color_temp)
    ax2.plot(df_sorted['START_DATE'], df_sorted['temperature'], color=color_temp, linewidth=0.5, alpha=0.5, label='Temperature')
    ax2.tick_params(axis='y', labelcolor=color_temp)

    plt.title('Casting Speed and Temperature over Time')
    plt.tight_layout()
    plt.savefig('time_series.png')
    print("Plot saved to time_series.png")
    
except Exception as e:
    print(f"Error: {e}")
