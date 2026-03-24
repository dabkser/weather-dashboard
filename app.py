from flask import Flask, render_template, send_file, jsonify
import pandas as pd
from datetime import datetime
import os
import json

app = Flask(__name__)

# Try to load API key from config
API_KEY = None
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
        API_KEY = config.get('api_key')
except:
    pass

@app.route('/')
def weather_dashboard():
    """
    Main weather dashboard page
    """
    try:
        # Try to load the data
        df = pd.read_csv('weather_data.csv')
        last_update = df['timestamp'].iloc[-1] if 'timestamp' in df.columns else "Unknown"
        data = df.to_dict('records')
        
        # Calculate some stats
        avg_temp = df['temperature'].mean()
        max_temp = df['temperature'].max()
        min_temp = df['temperature'].min()
        hottest_city = df.loc[df['temperature'].idxmax(), 'city']
        coldest_city = df.loc[df['temperature'].idxmin(), 'city']
        
        # Check if images exist
        images_exist = os.path.exists('samples/temperatures.png')
        
        return render_template('weather_dashboard.html', 
                             data=data, 
                             last_update=last_update,
                             images_exist=images_exist,
                             now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             avg_temp=f"{avg_temp:.1f}",
                             max_temp=f"{max_temp:.1f}",
                             min_temp=f"{min_temp:.1f}",
                             hottest_city=hottest_city,
                             coldest_city=coldest_city,
                             has_api_key=API_KEY is not None and API_KEY != "YOUR_API_KEY_HERE")
    except Exception as e:
        print(f"Error loading data: {e}")
        # If no data exists yet
        return render_template('weather_dashboard.html', 
                             data=None, 
                             last_update="No data yet",
                             images_exist=False,
                             now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             avg_temp="--",
                             max_temp="--",
                             min_temp="--",
                             hottest_city="--",
                             coldest_city="--",
                             has_api_key=API_KEY is not None and API_KEY != "YOUR_API_KEY_HERE")
    
@app.route('/update')
def update_data():
    """
    Route to manually trigger data update
    """
    # Check if API key is set
    if API_KEY == "YOUR_API_KEY_HERE" or API_KEY is None:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>API Key Missing</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #e6e6fa 0%, #dcd0ff 100%);
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin: 0;
                }
                .card {
                    background: white;
                    padding: 40px;
                    border-radius: 8px;
                    text-align: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    max-width: 500px;
                }
                .icon {
                    font-size: 64px;
                    margin-bottom: 20px;
                }
                h1 {
                    color: #e74c3c;
                    margin-bottom: 20px;
                }
                p {
                    color: #666;
                    margin-bottom: 30px;
                    line-height: 1.6;
                }
                .button {
                    background: #8e44ad;
                    color: white;
                    padding: 12px 24px;
                    text-decoration: none;
                    border-radius: 6px;
                    display: inline-block;
                    transition: 0.3s;
                }
                .button:hover {
                    background: #7d3c98;
                    transform: translateY(-2px);
                }
            </style>
        </head>
        <body>
            <div class="card">
                <div class="icon">🔑</div>
                <h1>API Key Required</h1>
                <p>Please set your OpenWeatherMap API key in config.json to fetch live weather data.</p>
                <a href="/" class="button">← Back to Dashboard</a>
            </div>
        </body>
        </html>
        """
    
    #  import and run the data fetcher
    import data_fetcher
    df = data_fetcher.fetch_weather_data()
    
    if df is not None:
        # Create success page with animation
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Update Successful!</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #e6e6fa 0%, #dcd0ff 100%);
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin: 0;
                    animation: fadeIn 0.5s ease-in;
                }}
                @keyframes fadeIn {{
                    from {{ opacity: 0; transform: translateY(20px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}
                .card {{
                    background: white;
                    padding: 40px;
                    border-radius: 8px;
                    text-align: center;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    max-width: 500px;
                }}
                .icon {{
                    font-size: 80px;
                    margin-bottom: 20px;
                    animation: bounce 0.5s ease-in-out;
                }}
                @keyframes bounce {{
                    0%, 100% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.1); }}
                }}
                h1 {{
                    color: #27ae60;
                    margin-bottom: 20px;
                }}
                .stats {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                }}
                .stat-number {{
                    font-size: 36px;
                    font-weight: bold;
                    color: #8e44ad;
                }}
                p {{
                    color: #666;
                    margin: 10px 0;
                }}
                .button {{
                    background: #8e44ad;
                    color: white;
                    padding: 12px 24px;
                    text-decoration: none;
                    border-radius: 6px;
                    display: inline-block;
                    transition: 0.3s;
                    margin-top: 10px;
                }}
                .button:hover {{
                    background: #7d3c98;
                    transform: translateY(-2px);
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="icon">✅</div>
                <h1>Weather Data Updated!</h1>
                <div class="stats">
                    <div class="stat-number">{len(df)}</div>
                    <p>Cities Updated Successfully</p>
                </div>
                <p>Last Update: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                <a href="/" class="button">← Return to Dashboard</a>
            </div>
        </body>
        </html>
        """
    else:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Update Failed</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #e6e6fa 0%, #dcd0ff 100%);
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin: 0;
                }
                .card {
                    background: white;
                    padding: 40px;
                    border-radius: 8px;
                    text-align: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    max-width: 500px;
                }
                .icon {
                    font-size: 64px;
                    margin-bottom: 20px;
                }
                h1 {
                    color: #e74c3c;
                    margin-bottom: 20px;
                }
                p {
                    color: #666;
                    margin-bottom: 30px;
                }
                .button {
                    background: #8e44ad;
                    color: white;
                    padding: 12px 24px;
                    text-decoration: none;
                    border-radius: 6px;
                    display: inline-block;
                }
                .button:hover {
                    background: #7d3c98;
                }
            </style>
        </head>
        <body>
            <div class="card">
                <div class="icon">❌</div>
                <h1>Update Failed</h1>
                <p>Could not fetch weather data. Please check your internet connection and API key.</p>
                <a href="/" class="button">← Back to Dashboard</a>
            </div>
        </body>
        </html>
        """

@app.route('/visualize')
def visualize():
    """
    Route to generate visualizations
    """
    import visualizer
    visualizer.create_weather_visualizations()
    
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Charts Generated!</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #e6e6fa 0%, #dcd0ff 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0;
            }
            .card {
                background: white;
                padding: 40px;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                max-width: 500px;
            }
            .icon {
                font-size: 80px;
                margin-bottom: 20px;
            }
            h1 {
                color: #27ae60;
                margin-bottom: 10px;
            }
            .stats {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
            }
            .stat-number {
                font-size: 36px;
                font-weight: bold;
                color: #8e44ad;
            }
            p {
                color: #666;
                margin: 10px 0;
            }
            .button {
                background: #8e44ad;
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 6px;
                display: inline-block;
                transition: 0.3s;
            }
            .button:hover {
                background: #7d3c98;
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="icon">📊</div>
            <h1>Charts Generated!</h1>
            <div class="stats">
                <div class="stat-number">5 Charts</div>
                <p>Temperature • Humidity • Weather<br>Temp vs Wind • Heatmap</p>
            </div>
            <p>Saved in <strong>samples/</strong> folder</p>
            <a href="/" class="button">← Back to Dashboard</a>
        </div>
    </body>
    </html>
    """

@app.route('/report')
def report():
    """
    Serve the HTML report
    """
    try:
        return send_file('weather_report.html')
    except Exception as e:
        return f"Error: {e}. report file not found. Run python visualizer first"

@app.route('/api-status')
def api_status():
    """
    Check API key status
    """
    if API_KEY == "YOUR_API_KEY_HERE" or API_KEY is None:
        return jsonify({
            'status': 'missing',
            'message': 'API key not set. Get one from OpenWeatherMap.org'
        })
    else:
        return jsonify({
            'status': 'ok',
            'message': 'API key is set'
        })

# Create necessary folders
if not os.path.exists('templates'):
    os.makedirs('templates')

if not os.path.exists('static'):
    os.makedirs('static')


weather_dashboard_html = """<!DOCTYPE html>
<html>
<head>
    <title>Weather Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23ffb7c5" opacity="0.2"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>');
            background-repeat: repeat;
            background-size: 40px 40px;
            background-attachment: fixed;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2.5rem;
            border-radius: 8px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
            text-align: center;
        }
        
        h1 {
            font-size: 2.8rem;
            margin-bottom: 0.5rem;
        }
        
        .header-subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .api-warning {
            background: #fff3cd;
            color: #856404;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #ffc107;
        }
        
        .controls {
            background: white;
            padding: 1.8rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            align-items: center;
        }
        
        .button {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #8e44ad;
            color: white;
            padding: 14px 28px;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(79, 172, 254, 0.2);
        }
        
        .button:hover {
            background: #7d3c98;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(79, 172, 254, 0.3);
        }
        
        .button.secondary {
            background: #6c757d;
        }
        
        .button.secondary:hover {
            background: #5a6268;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: white;
            padding: 1.5rem;
            border-radius: 6px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: bold;
            color: #4b0082;
            margin: 10px 0;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9rem;
        }
        
        .hot { 
            background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
            color: #d63031;
        }
        
        .cold { 
            background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
            color: #0984e3;
        }
        
        .data-table {
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
            margin-bottom: 2rem;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            border-radius: 8px;
        }
        
        th {
            background: #8e44ad;
            color: white;
            padding: 1.2rem;
            text-align: left;
            font-weight: 600;
        }
        
        td {
            padding: 1rem;
            border-bottom: 1px solid #e1e5e9;
        }
        
        tr:hover {
            background-color: #f8f9fa;
        }
        
        .weather-icon {
            font-size: 1.5rem;
            margin-right: 8px;
        }
        
        .visualizations {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .chart-container {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        }
        
        .chart-container img {
            width: 100%;
            height: auto;
            border-radius: 8px;
        }
        
        .timestamp {
            text-align: center;
            color: #2c3e50;
            font-size: 0.9rem;
            margin-top: 1rem;
        }
        
        footer {
            text-align: center;
            padding: 2rem;
            color: #666;
            font-size: 0.9rem;
        }
        
        @media (max-width: 768px) {
            .visualizations {
                grid-template-columns: 1fr;
            }
            
            .controls {
                flex-direction: column;
                align-items: stretch;
            }
            
            .button {
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Global Weather Dashboard</h1>
            <p class="header-subtitle">Real-time weather monitoring across major cities worldwide</p>
            <div class="timestamp">
                <p>Last Updated: {{ last_update }} | Current Time: {{ now }}</p>
            </div>
        </header>
        
        {% if not has_api_key %}
        <div class="api-warning">
            <strong>API Key Required:</strong> Please set your OpenWeatherMap API key in data_fetcher.py to fetch live data.
            <br>Get a free API key from: <a href="https://home.openweathermap.org/api_keys" target="_blank">https://home.openweathermap.org/api_keys</a>
        </div>
        {% endif %}
        
        <div class="controls">
            <a href="/update" class="button">
                🔄 Update Weather Data
            </a>
            <a href="/visualize" class="button">
                📊 Generate Charts
            </a>
            <a href="/report" class="button secondary">
                📄 View Full Report
            </a>
            <a href="/api-status" class="button secondary" target="_blank">
                🔑 Check API Status
            </a>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Average Temperature</div>
                <div class="stat-value">{{ avg_temp }}°C</div>
            </div>
            <div class="stat-card hot">
                <div class="stat-label">Hottest City</div>
                <div class="stat-value">{{ hottest_city }}</div>
                <div class="stat-label">{{ max_temp }}°C</div>
            </div>
            <div class="stat-card cold">
                <div class="stat-label">Coldest City</div>
                <div class="stat-value">{{ coldest_city }}</div>
                <div class="stat-label">{{ min_temp }}°C</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Cities Monitored</div>
                <div class="stat-value">{{ data|length if data else 0 }}</div>
            </div>
        </div>
        
        {% if data %}
        <div class="data-table">
            <table>
                <thead>
                    <tr>
                        <th>City</th>
                        <th>Temperature</th>
                        <th>Feels Like</th>
                        <th>Weather</th>
                        <th>Humidity</th>
                        <th>Wind</th>
                        <th>Sunrise/Sunset</th>
                    </tr>
                </thead>
                <tbody>
                    {% for city in data %}
                    <tr>
                        <td><strong>{{ city.city }}</strong> ({{ city.country }})</td>
                        <td>
                            {% if city.temperature > 20 %}
                            <span style="color: #e74c3c;">{{ "%.1f"|format(city.temperature) }}°C 🔥</span>
                            {% elif city.temperature < 10 %}
                            <span style="color: #3498db;">{{ "%.1f"|format(city.temperature) }}°C ❄️</span>
                            {% else %}
                            {{ "%.1f"|format(city.temperature) }}°C
                            {% endif %}
                        </td>
                        <td>{{ "%.1f"|format(city.feels_like) }}°C</td>
                        <td>
                            {% if city.weather == 'Clear' %}
                            ☀️
                            {% elif city.weather == 'Clouds' %}
                            ☁️
                            {% elif city.weather == 'Rain' %}
                            🌧️
                            {% elif city.weather == 'Snow' %}
                            ❄️
                            {% elif city.weather == 'Thunderstorm' %}
                            ⛈️
                            {% else %}
                            🌤️
                            {% endif %}
                            {{ city.weather_description|title }}
                        </td>
                        <td>{{ city.humidity }}%</td>
                        <td>{{ city.wind_speed }} m/s</td>
                        <td>↑ {{ city.sunrise }} | ↓ {{ city.sunset }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% else %}
        <div class="data-table" style="text-align: center; padding: 3rem;">
            <h3>No weather data available yet</h3>
            <p>Click "Update Weather Data" to fetch the latest weather information.</p>
            {% if not has_api_key %}
            <p style="color: #dc3545; margin-top: 1rem;">
                Remember to set your OpenWeatherMap API key first!
            </p>
            {% endif %}
        </div>
        {% endif %}
        
        {% if images_exist %}
        <h2 style="margin: 2rem 0 1rem 0;">Weather Visualizations</h2>
        <div class="visualizations">
            <div class="chart-container">
                <h3>Temperature Comparison</h3>
                <img src="/static/temperatures.png" alt="Temperature Chart">
            </div>
            <div class="chart-container">
                <h3>Humidity Levels</h3>
                <img src="/static/humidity.png" alt="Humidity Chart">
            </div>
        </div>
        {% endif %}
        
        <footer>
            <p>Data Source: OpenWeatherMap API | Last Update: {{ last_update }}</p>
            <p>Dashboard created by Sarsenova Daliya</p>
            <p>Build with Python, Flask & OpenWeatherMap</p>
        </footer>
    </div>
    
    <script>
        // Auto-refresh data every 5 minutes (300000 milliseconds)
        setTimeout(function() {
            window.location.reload();
        }, 300000);
        
        // Make buttons more interactive
        document.querySelectorAll('.button').forEach(button => {
            button.addEventListener('click', function() {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 200);
            });
        });
        
        // Show loading state for update button
        document.querySelector('a[href="/update"]').addEventListener('click', function(e) {
            this.innerHTML = 'Updating...';
            this.style.opacity = '0.7';
            this.style.pointerEvents = 'none';
        });
    </script>
</body>
</html>"""

# Save the template to file
with open('templates/weather_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(weather_dashboard_html)

# Also create a simple config file if it doesn't exist
if not os.path.exists('config.json'):
    with open('config.json', 'w') as f:
        json.dump({"api_key": "YOUR_API_KEY_HERE"}, f)

if __name__ == '__main__':
    print("Starting Weather Dashboard...")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, port=5000)