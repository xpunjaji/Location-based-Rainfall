import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import time
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from meteostat import Point, Daily
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.statespace.sarimax import SARIMAX


# Initialize Streamlit App
st.title("Rainfall Prediction and Visualization")
st.write("Enter a location, choose dates, and visualize or predict rainfall.")

# Function for geocoding with retry mechanism
def geocode_with_retry(location_input, retries=3, delay=5):
    geolocator = Nominatim(user_agent="rainfall_app")
    for attempt in range(retries):
        try:
            location = geolocator.geocode(location_input, timeout=10)
            return location
        except GeocoderUnavailable:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                st.error("Unable to connect to the geolocation service after multiple attempts.")
                return None
    return None

# Location Input
st.subheader("1. Input your location")
location_input = st.text_input("Enter location (e.g., Mumbai)", "Mumbai")

location = geocode_with_retry(location_input)

if location:
    selected_lat = location.latitude
    selected_lon = location.longitude
    st.write(f"Selected Location: {location.address}")

    # Display map with location
    m = folium.Map(location=[selected_lat, selected_lon], zoom_start=10)
    folium.Marker([selected_lat, selected_lon], popup=location_input).add_to(m)
    folium_static(m)

    # Date Range Selection
    st.subheader("2. Select a date range")
    start_date = st.date_input("Start Date", datetime.date(2015, 1, 1))
    end_date = st.date_input("End Date", datetime.date.today())

    # Convert dates to datetime format
    start_date = pd.to_datetime(start_date).date()
    end_date = pd.to_datetime(end_date).date()

    # Function to fetch Meteostat data
    def get_meteostat_data(lat, lon, start_date, end_date):
        start = datetime.datetime(start_date.year, start_date.month, start_date.day)
        end = datetime.datetime(end_date.year, end_date.month, end_date.day)
        location = Point(lat, lon)
        data = Daily(location, start, end).fetch()
        return data[['prcp']]  # Extracting precipitation data

    # Fetch weather data
    st.subheader("3. Rainfall Data from Meteostat")
    meteostat_df = get_meteostat_data(selected_lat, selected_lon, start_date, end_date)

    if meteostat_df.empty:
        st.warning("No rainfall data available for the selected date range.")
    else:
        meteostat_df.columns = ['Rainfall (mm)']
        meteostat_df.index = pd.to_datetime(meteostat_df.index)
        st.write(meteostat_df)

        # Clean data: Remove None or 0 values
        meteostat_df = meteostat_df[meteostat_df['Rainfall (mm)'] > 0]
        st.write("Cleaned Data (No zeros or None values):")
        st.write(meteostat_df)

        # Visualization of raw data
        st.subheader("4. Rainfall Data Visualization")
        fig = px.line(meteostat_df, x=meteostat_df.index, y='Rainfall (mm)', 
                      title='Daily Rainfall Data', labels={'Rainfall (mm)': 'Rainfall (mm)', 'index': 'Date'})
        st.plotly_chart(fig)

        # Detecting monsoon season (top 4 months with highest average rainfall)
        def detect_monsoon_season(df):
            monthly_avg = df.resample('M').sum()
            monsoon_months = monthly_avg.groupby(monthly_avg.index.month).mean().nlargest(4, 'Rainfall (mm)').index
            return monsoon_months

        monsoon_months_auto = detect_monsoon_season(meteostat_df)
        st.write("Automatically Detected Monsoon Months based on rainfall data:", monsoon_months_auto.tolist())

        # User input for forecast duration (in years)
        years_input = st.number_input("Forecast for the next (years)", min_value=1, max_value=10, value=1)
        forecast_days = years_input * 365  # Convert years to days

        # Train SARIMA model for forecasting
        st.subheader("5. Rainfall Prediction with SARIMA")

        # Scale the rainfall data
        scaler = MinMaxScaler()
        scaled_rainfall = scaler.fit_transform(meteostat_df[['Rainfall (mm)']])

        # Use a larger training window (80% of the data for training, 20% for testing)
        train_size = int(len(scaled_rainfall) * 0.8)
        train_data = scaled_rainfall[:train_size]
        test_data = scaled_rainfall[train_size:]

        # Fit SARIMA model with seasonal components
        # Seasonal SARIMA configuration (p, d, q, seasonal_order)
        # Here, seasonal_order=(1, 1, 1, 12) is an example; 12 is the seasonality period (monthly seasonality)
        model = SARIMAX(train_data, order=(5, 1, 0), seasonal_order=(1, 1, 1, 12))
        model_fit = model.fit()

        # Forecast for the specified number of years (in days)
        forecast_scaled = model_fit.forecast(steps=forecast_days)

        # Inverse scaling of the forecasted values
        forecast_original = scaler.inverse_transform(forecast_scaled.reshape(-1, 1))

        # Generate future dates for the forecast
        future_dates = pd.date_range(start=end_date, periods=forecast_days, freq='D')
        forecast_df = pd.DataFrame({'Date': future_dates, 'Forecasted Rainfall': forecast_original.flatten()})

        st.write(f"Rainfall Prediction Data for the next {years_input} year(s):")
        st.dataframe(forecast_df)

        # Monsoon season forecast
        monsoon_forecast = forecast_df[forecast_df['Date'].dt.month.isin(monsoon_months_auto)]
        non_monsoon_forecast = forecast_df[~forecast_df['Date'].dt.month.isin(monsoon_months_auto)]

        st.write("Monsoon Season Forecast Data:")
        st.dataframe(monsoon_forecast)

        st.write("Non-Monsoon Season Forecast Data:")
        st.dataframe(non_monsoon_forecast)

        # Visualization of forecasted data
        st.subheader(f"6. Forecasted Rainfall for the Next {years_input} Year(s)")

        # Overall Forecast Visualization
        fig = px.line(forecast_df, x='Date', y='Forecasted Rainfall', 
                      title=f'Forecasted Rainfall Over the Next {years_input} Year(s)', 
                      labels={'Forecasted Rainfall': 'Rainfall (mm)', 'Date': 'Date'},
                      color_discrete_sequence=['purple'])
        st.plotly_chart(fig)

        # Monsoon Season Forecast Visualization
        fig = px.line(monsoon_forecast, x='Date', y='Forecasted Rainfall', 
                      title='Monsoon Season Forecasted Rainfall', 
                      color_discrete_sequence=['red'])
        st.plotly_chart(fig)

        # Non-Monsoon Season Forecast Visualization
        fig = px.line(non_monsoon_forecast, x='Date', y='Forecasted Rainfall', 
                      title='Non-Monsoon Season Forecasted Rainfall', 
                      color_discrete_sequence=['orange'])
        st.plotly_chart(fig)

        # Add download button for forecast data
        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')

        csv = convert_df(forecast_df)
        st.download_button(
            label=f"Download Forecasted Data for the Next {years_input} Year(s)",
            data=csv,
            file_name=f"rainfall_forecast_{years_input}_years.csv",
            mime="text/csv"
        )
# Footer
st.markdown("------")
st.caption("👨‍💻 Developer >>>> This Project Was Developed And Built By Punjaji Karhale🚀")