# Global Weather Dashboard

An automated weather data dashboard that fetches real-time weather data from OpenWeatherMap API, creates beautiful visualizations, and displays everything in a modern web interface.

## Features

- Real-time Weather Data - Fetches current weather for 11 major cities worldwide
- Data Visualizations - Automatically generates 5 different charts:
  - Temperature Comparison
  - Humidity Levels
  - Weather Conditions Distribution
  - Temperature vs Wind Speed
  - Weather Data Heatmap
- HTML Report - Generates a shareable report with all data and charts
- SQLite Database - Stores historical weather data
- Auto-refresh - Dashboard updates every 5 minutes

## Technologies Used

- Python 3.10+ - Core programming language
- Flask - Web framework for the dashboard
- Pandas - Data manipulation and analysis
- Matplotlib & Seaborn - Data visualization
- Requests - API calls to OpenWeatherMap
- SQLite - Local database storage

## Prerequisites

- Python 3.10 or higher installed on your system
- OpenWeatherMap API key (free)

## Installation & Setup

### 1. Clone or Download the Project
```bash
git clone https://github.com/dabkser/weather-dashboard.git
cd weather-dashboard

### 2. Create Virtual Environment
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac / Linux
python3 -m venv .venv
source .venv/bin/activate

### 3. Install Dependencies 
pip install -r requirements.txt

### 4. Get Your OpenWeatherMap API Key
1. Go to OpenWeatherMap website
2. Sign up for a free account
3. Go to API Keys section
4. Copy your API key

### 5. Configure API Key
Open config.json and replace with your actual API key:
{"api_key": "your_actual_api_key_here"}

## How to Run

### Step 1: Fetch Weather Data
python data_fetcher.py

This will:
- Fetch current weather for all 11 cities
- Save data to weather_data.csv
- Store in SQLite database

### Step 2: Generate Visualizations
python visualizer.py

This will:
- Create 5 charts in the samples folder
- Generate an HTML report

### Step 3: Start the Dashboard
python app.py

Then open your browser and go to: http://localhost:5000

## Dashboard Features

- Update Weather Data - Fetches latest weather from API
- Generate Charts - Creates all 5 visualizations
- View Full Report - Opens complete HTML report
- Check API Status - Verifies API key configuration


## Troubleshooting

### API Key Required Warning
- Make sure config.json has your actual API key
- Wait 10 minutes after creating your API key for it to activate
- Check your internet connection

### Charts Not Showing
Run these commands:
python visualizer.py
copy samples\*.png static\   (Windows)
cp samples/*.png static/     (Mac/Linux)
Refresh the dashboard

### Flask Won't Start
- Check if port 5000 is in use
- Make sure all dependencies are installed
- Try changing port to 5001 in app.py

### No Data Shows
python data_fetcher.py
Then refresh dashboard

## Author

Sarsenova Daliya
GitHub: @dabkser
Project Link: https://github.com/dabkser/weather-dashboard

## Acknowledgments

- Weather data provided by OpenWeatherMap
- Built with Python and Flask