import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import numpy as np

# Make the charts look nicer
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def create_weather_visualizations():
    """
    Create charts and graphs from the weather data
    """
    print("Creating weather visualizations...")
    
    try:
        # Read the data
        df = pd.read_csv('weather_data.csv')
        
        # Create output folder if it doesn't exist
        if not os.path.exists('samples'):
            os.makedirs('samples')
        
        # Sort by temperature (coldest to hottest)
        df = df.sort_values('temperature')
        
        # 1. Temperature Comparison Bar Chart
        plt.figure(figsize=(14, 8))
        bars = plt.barh(df['city'], df['temperature'], 
                       color=plt.cm.coolwarm(np.linspace(0, 1, len(df))))
        
        plt.xlabel('Temperature (°C)')
        plt.title('Current Temperature by City')
        plt.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
        
        # Add temperature labels on bars
        for bar in bars:
            width = bar.get_width()
            temp_text = f'{width:.1f}°C'
            plt.text(width, bar.get_y() + bar.get_height()/2, 
                    temp_text, ha='left' if width >= 0 else 'right', 
                    va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('samples/temperatures.png', dpi=100, bbox_inches='tight')
        plt.close()
        
        # 2. Humidity Chart
        plt.figure(figsize=(14, 8))
        
        # Create color gradient based on humidity
        colors = plt.cm.Blues(df['humidity'] / 100)
        
        bars = plt.barh(df['city'], df['humidity'], color=colors)
        plt.xlabel('Humidity (%)')
        plt.title('Humidity Levels by City')
        
        # Add humidity labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2, 
                    f'{width:.0f}%', ha='left', va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('samples/humidity.png', dpi=100, bbox_inches='tight')
        plt.close()
        
        # 3. Weather Conditions Pie Chart
        plt.figure(figsize=(10, 10))
        weather_counts = df['weather'].value_counts()
        colors = plt.cm.Set3(np.arange(len(weather_counts)))
        
        plt.pie(weather_counts.values, labels=weather_counts.index, 
                autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Weather Conditions Distribution')
        plt.savefig('samples/weather_conditions.png', dpi=100, bbox_inches='tight')
        plt.close()
        
        # 4. Wind Speed vs Temperature Scatter Plot
        plt.figure(figsize=(12, 8))
        
        # Size of dots based on humidity
        sizes = df['humidity'] * 2
        
        scatter = plt.scatter(df['temperature'], df['wind_speed'], 
                             s=sizes, alpha=0.7, 
                             c=df['humidity'], cmap='viridis')
        
        plt.colorbar(scatter, label='Humidity (%)')
        plt.xlabel('Temperature (°C)')
        plt.ylabel('Wind Speed (m/s)')
        plt.title('Temperature vs Wind Speed (Bubble size = Humidity)')
        
        # Add city labels
        for i, row in df.iterrows():
            plt.annotate(row['city'], 
                        (row['temperature'], row['wind_speed']),
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=9)
        
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('samples/temp_vs_wind.png', dpi=100, bbox_inches='tight')
        plt.close()
        
        # 5. Create a Heatmap-style table
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Select numerical data for heatmap
        heatmap_data = df[['temperature', 'humidity', 'wind_speed', 'pressure']]
        heatmap_data.index = df['city']
        
        # Normalize data for better color representation
        normalized_data = (heatmap_data - heatmap_data.min()) / (heatmap_data.max() - heatmap_data.min())
        
        im = ax.imshow(normalized_data.T, cmap='YlOrRd', aspect='auto')
        
        # Set labels
        ax.set_xticks(np.arange(len(df)))
        ax.set_yticks(np.arange(4))
        ax.set_xticklabels(df['city'])
        ax.set_yticklabels(['Temp (°C)', 'Humidity (%)', 'Wind (m/s)', 'Pressure (hPa)'])
        
        # Rotate city labels
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Add text annotations
        for i in range(len(df)):
            for j in range(4):
                text = ax.text(i, j, f'{heatmap_data.iloc[i, j]:.1f}',
                             ha="center", va="center", color="black", fontweight='bold')
        
        ax.set_title("Weather Data Comparison Heatmap")
        plt.tight_layout()
        plt.savefig('samples/weather_heatmap.png', dpi=100, bbox_inches='tight')
        plt.close()
        
        print("✅ 5 visualizations saved in 'samples' folder!")
        
        # Create HTML report
        create_weather_html_report(df)
        
    except Exception as e:
        print(f"Error creating visualizations: {e}")
        import traceback
        traceback.print_exc()

def create_weather_html_report(df):
    """
    Create a simple HTML report with the weather visualizations
    """
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Weather Dashboard Report</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #e6e6fa 0%, #dcd0ff 100%);
            min-height: 100vh;
        }}
        
        .header {{ 
            text-align: center; 
            padding: 30px; 
            background: #8e44ad;
            color: white;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        
        .stats {{ 
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 6px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #8e44ad;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 30px 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        th {{
            background: #8e44ad;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        
        td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }}
        
        tr:hover {{
            background-color: #f5f5f5;
        }}
        
        .charts {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .chart {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        
        img {{
            max-width: 100%;
            border-radius: 8px;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
        }}
    </style>
    </head>
    <body>
        <div class="header">
            <h1>Global Weather Dashboard Report</h1>
            <p>Real-time weather data from cities around the world</p>
            <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{df['temperature'].mean():.1f}°C</div>
                <div class="stat-label">Average Temperature</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{df['humidity'].mean():.0f}%</div>
                <div class="stat-label">Average Humidity</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{df['wind_speed'].mean():.1f} m/s</div>
                <div class="stat-label">Average Wind Speed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(df)}</div>
                <div class="stat-label">Cities Monitored</div>
            </div>
        </div>
        
        <h2>Weather Data by City</h2>
        <table>
            <thead>
                <tr>
                    <th>City</th>
                    <th>Temperature</th>
                    <th>Feels Like</th>
                    <th>Weather</th>
                    <th>Humidity</th>
                    <th>Wind Speed</th>
                </tr>
            </thead>
            <tbody>
"""
    
    # Add table rows
    for _, row in df.iterrows():
        temp_class = "hot" if row['temperature'] > 20 else "cold"
        html_content += f"""
                <tr>
                    <td><strong>{row['city']}</strong></td>
                    <td class="{temp_class}">{row['temperature']:.1f}°C</td>
                    <td>{row['feels_like']:.1f}°C</td>
                    <td>{row['weather']} ({row['weather_description']})</td>
                    <td>{row['humidity']}%</td>
                    <td>{row['wind_speed']} m/s</td>
                </tr>
        """
    
    html_content += f"""
            </tbody>
        </table>
        
        <h2>Weather Visualizations</h2>
        <div class="charts">
            <div class="chart">
                <h3>Temperature Comparison</h3>
                <img src="/static/temperatures.png" alt="Temperatures">
            </div>
            <div class="chart">
                <h3>Humidity Levels</h3>
                <img src="/static/humidity.png" alt="Humidity">
            </div>
            <div class="chart">
                <h3>Weather Conditions</h3>
                <img src="/static/weather_conditions.png" alt="Weather Conditions">
            </div>
            <div class="chart">
                <h3>Temperature vs Wind Speed</h3>
                <img src="/static/temp_vs_wind.png" alt="Temp vs Wind">
            </div>
            <div class="chart">
                <h3>Weather Data Heatmap</h3>
                <img src="/static/weather_heatmap.png" alt="Weather Heatmap">
            </div>
        </div>
        
        <div class="footer">
            <p>Data Source: OpenWeatherMap API | Last Update: {{ last_update }}</p>
            <p>Dashboard created by Sarsenova Daliya</p>
            <p>Build with Python, Flask & OpenWeatherMap</p>
        </div>
    </body>
    </html>
    """
    
    with open('weather_report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("HTML report created: weather_report.html")

if __name__ == "__main__":
    create_weather_visualizations()