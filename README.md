<<<<<<< HEAD
# 🌦️ Weather Logger

A Python-based weather tracking application that retrieves current weather conditions using the Open-Meteo API and stores search history in SQLite. It features a Streamlit dashboard for exploring weather data and reviewing previous searches.

## ✨ Features

- **Live Weather Data:** Retrieve current conditions for a selected city.
- **Weather Dashboard:** View temperature, feels-like temperature, humidity, wind speed, elevation, and coordinates.
- **City Geocoding:** Resolve city names into geographic coordinates.
- **SQLite History:** Save and review recent weather searches.
- **Caching:** Reuse recent weather results to reduce unnecessary API requests.
- **Search History:** Browse saved records and export them as CSV.
- **Interactive UI:** Use a styled Streamlit dashboard with persistent city search.

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- SQLite
- Open-Meteo API
- Requests and Requests Cache

## 📁 Project Structure

```text
weather_logger/
├── app.py
├── main.py
├── city_coord.py
├── database.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/weather_logger.git
cd weather_logger
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

Streamlit will provide a local URL to open the dashboard in your browser.

## 🌐 Weather Data

This project uses the free [Open-Meteo API](https://open-meteo.com/) for geocoding and weather data. Check the provider's current terms and usage limits before deploying the application publicly.

## 💡 What I Learned

- Working with external REST APIs
- Handling API responses and errors
- Organizing Python code into modules
- Persisting application data using SQLite
- Implementing caching for repeated requests
- Building interactive dashboards with Streamlit
- Exporting tabular data to CSV
- Managing project dependencies and version control

## 📌 Future Improvements

- Weather forecasts for upcoming days
- Historical weather visualizations
- Automated testing
- Public deployment
- Improved search and filtering
