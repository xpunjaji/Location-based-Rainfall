#### Rainfall Prediction and Visualization 🌧️

This project provides an interactive web application for rainfall prediction and data visualization, helping users analyze and forecast rainfall patterns in different locations. Built with **Streamlit**, **Meteostat API**, **SARIMA**, and **Plotly**, this tool allows users to visualize historical rainfall data, detect monsoon seasons, and predict future rainfall.

Key features include:
- **Location-based Rainfall Data**: Get rainfall data by entering a location (city or region).
- **Interactive Data Visualization**: Visualize daily rainfall data with zoom, pan, and hover effects.
- **Monsoon Detection**: Automatically identify the months with the highest rainfall, and highlight them as monsoon months.
- **Rainfall Forecasting with SARIMA**: Forecast future rainfall for up to 10 years based on historical data.
- **Monsoon vs Non-Monsoon Forecasting**: Visualize forecasts separately for monsoon and non-monsoon periods.
- **Downloadable Forecasts**: Export forecasted rainfall data as a CSV file for offline use.

### Features:
- **Location Input** 🌍: Convert location to coordinates and display on an interactive map using **Folium**.
- **Date Range Selection** 📅: Choose custom date ranges to analyze historical rainfall data.
- **Rainfall Data Visualization** 📊: Interactive line charts to visualize rainfall over time using **Plotly**.
- **Monsoon Detection** 🌧️: Auto-detects the top 4 monsoon months based on rainfall data.
- **Forecasting** 🔮: Use the **SARIMA** model for time-series rainfall predictions up to 10 years.
- **Download Forecast Data** 💾: Easily download rainfall forecast data as a CSV file.

### Tech Stack:
- **Python**: The core language for the app development.
- **Streamlit**: For building the interactive web interface.
- **Meteostat API**: For retrieving historical weather data.
- **SARIMAX (SARIMA)**: For performing time-series forecasting.
- **Plotly**: For creating interactive data visualizations.
- **Geopy**: For geocoding and location-based functionalities.
- **Folium**: For displaying the location map with interactive markers.
- **Scikit-learn**: For preprocessing data (like scaling with **MinMaxScaler**).
- **Pandas**: For data manipulation and analysis.
- **NumPy**: For numerical operations.
- **Jupyter Notebooks**: For exploratory data analysis and additional tasks.

---

### Folder Structure:
- **Data/**: Contains raw and processed rainfall data.
    - **rainfall_data.csv**: Raw and processed rainfall data for different regions.
  
- **notebooks/**: Jupyter notebooks for data analysis and web scraping.
    - **rainfall.ipynb**: Data analysis and rainfall forecasting using **SARIMA** model.
    - **webscraping.ipynb**: Scraping rainfall data from external sources (e.g., websites, APIs).

- **app.py**: The core **Streamlit** application file that integrates all features, including data fetching, forecasting, and visualization.

- **requirements.txt**: Lists all required Python packages and dependencies (e.g., **Streamlit**, **Meteostat**, **Plotly**, **Geopy**, **SARIMA**).

---

### Interactive Features Added:
1. **Dynamic Charts** 📊:
   - **Plotly** allows for zooming, panning, and hover effects on the rainfall visualization, offering an engaging way to explore data.
   - Users can dynamically select and compare different data points or time ranges, making the app more interactive.

2. **Date Range Slider** 📅:
   - A slider can be added to let users interactively adjust the start and end date for rainfall data analysis.

3. **Forecast Duration Slider** 🔮:
   - A slider for adjusting the forecast period (in years), with a dynamic chart that updates as the user changes the forecast duration.

4. **Monsoon/Non-Monsoon Toggle** 🌞🌧️:
   - A toggle button or dropdown allows users to select between viewing monsoon or non-monsoon period forecasts.

5. **Download Button** 💾:
   - A download button appears once the user generates forecast data, with a progress indicator showing the download status.

---
# 👨‍💻 Developer
     This Project Was Developed And Built By Punjaji Karhale🚀