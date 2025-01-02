import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Load data from SQLite database
conn = sqlite3.connect("weather_data.db")
df = pd.read_sql_query("SELECT * FROM weather", conn)
conn.close()

# Change dates in df to datetime and show if it is today's date
df["timestamp"] = pd.to_datetime(df["timestamp"])
today = pd.Timestamp(datetime.today().date())
df["is_today"] = df["timestamp"].dt.date == today.date()

# Sidebar Filters
cities = st.sidebar.multiselect("Select Cities", df["city"].unique(), default=df["city"].unique())

# Filter data based on sidebar input
filtered_df = df[df["city"].isin(cities)]
todays_df = filtered_df[filtered_df["is_today"] == True]

# Dashboard Title
st.title("Real-Time Weather Dashboard")
st.write("Visualize the latest weather data from OpenWeatherMap.")

# Display Data Table
st.subheader("Weather Data")
st.dataframe(filtered_df)

# Visualization: Temperature and Humidity Side-by-Side
st.subheader("Temperature and Humidity Comparison")

# Plotting
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(todays_df["city"]))  # the label locations
width = 0.35  # the width of the bars

# Bar plots
ax.bar(x - width/2, todays_df["temperature"], width, label="Temperature (°C)", color="orange")
ax.bar(x + width/2, todays_df["humidity"], width, label="Humidity (%)", color="blue")

# Add labels, title, and legend
ax.set_xlabel("City")
ax.set_ylabel("Value")
ax.set_title("Temperature and Humidity by City")
ax.set_xticks(x)
ax.set_xticklabels(todays_df["city"], rotation=45)
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)
