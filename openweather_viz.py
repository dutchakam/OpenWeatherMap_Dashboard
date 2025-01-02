import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from SQLite database
conn = sqlite3.connect("weather_data.db")
df = pd.read_sql_query("SELECT * FROM weather", conn)
conn.close()

# Ensure timestamp column is in datetime format
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Plot temperature by city
plt.figure(figsize=(10, 6))
sns.barplot(x="city", y="temperature", data=df, palette="coolwarm")
plt.title("Current Temperature by City")
plt.ylabel("Temperature (°C)")
plt.xlabel("City")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("temperature_by_city.png")
plt.show()

# Plot humidity levels by city
plt.figure(figsize=(10, 6))
sns.barplot(x="city", y="humidity", data=df, palette="Blues")
plt.title("Current Humidity by City")
plt.ylabel("Humidity (%)")
plt.xlabel("City")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("humidity_by_city.png")
plt.show()
