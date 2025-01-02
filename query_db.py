import sqlite3
import pandas as pd
from datetime import datetime

# Database file
db_path = "weather_data.db"

try:
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Inspect tables
    print("Tables in the database:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if not tables:
        print("No tables found in the database.")
    else:
        for table in tables:
            print(f"- {table[0]}")

    # Inspect weather table (replace 'weather' with your table name if different)
    print("\nContents of the 'weather' table:")
    # cursor.execute("SELECT * FROM weather;")
    # rows = cursor.fetchall()
    # if not rows:
    #     print("No data found in the 'weather' table.")
    # else:
    #     for row in rows:
    #         print(row)
    df = pd.read_sql_query("SELECT * FROM weather", conn)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    today = pd.Timestamp(datetime.today().date())
    df["is_today"] = df["timestamp"].dt.date == today.date()
    print(df)

except sqlite3.Error as e:
    print(f"Database error: {e}")
finally:
    # Close connection
    if conn:
        conn.close()

