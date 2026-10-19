
import sqlite3


def create_table():
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            country TEXT NOT NULL,
            temperature REAL,
            feels_like REAL,
            wind_speed REAL,
            weather_condition TEXT,
            coordinates_lat REAL,
            coordinates_lon REAL,
            elevation REAL,
            humidity REAL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Add missing columns if the database already exists
    cursor.execute("PRAGMA table_info(weather_history)")
    existing_columns = {row[1] for row in cursor.fetchall()}

    new_columns = {
        "feels_like": "REAL",
        "coordinates_lat": "REAL",
        "coordinates_lon": "REAL",
        "elevation": "REAL",
        "humidity": "REAL",
    }

    for column, data_type in new_columns.items():
        if column not in existing_columns:
            cursor.execute(
                f"ALTER TABLE weather_history ADD COLUMN {column} {data_type}"
            )

    conn.commit()
    conn.close()


def save_weather(weather):
    conn = sqlite3.connect("weather.db")

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM weather_history WHERE LOWER(city) = LOWER(?)",
            (weather["city"],)
        )
        row = cursor.fetchone()

        if row:
            # Update the existing city's weather data
            cursor.execute("""
                UPDATE weather_history
                SET country = ?,
                    temperature = ?,
                    feels_like = ?,
                    wind_speed = ?,
                    weather_condition = ?,
                    coordinates_lat = ?,
                    coordinates_lon = ?,
                    elevation = ?,
                    humidity = ?,
                    timestamp = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (
                weather["country"],
                weather["temperature"],
                weather["feels_like"],
                weather["wind_speed"],
                weather["weather_condition"],
                weather["latitude"],
                weather["longitude"],
                weather["elevation"],
                weather["humidity"],
                row[0]
            ))

        else:
            # Keep at most 10 records
            cursor.execute("SELECT COUNT(*) FROM weather_history")
            count = cursor.fetchone()[0]

            if count >= 10:
                cursor.execute("""
                    DELETE FROM weather_history
                    WHERE id = (
                        SELECT id
                        FROM weather_history
                        ORDER BY timestamp ASC, id ASC
                        LIMIT 1
                    )
                """)

            # Insert a new city's weather data
            cursor.execute("""
                INSERT INTO weather_history (
                    city, country, temperature, feels_like,
                    wind_speed, weather_condition,
                    coordinates_lat, coordinates_lon,
                    elevation, humidity
                )
                VALUES (
                    :city, :country, :temperature, :feels_like,
                    :wind_speed, :weather_condition,
                    :latitude, :longitude, :elevation, :humidity
                )
            """, weather)

        conn.commit()

    except sqlite3.Error as err:
        conn.rollback()
        print(f"Database error: {err}")

    finally:
        conn.close()


def get_history():
    conn = None
    try:
        conn = sqlite3.connect("weather.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM weather_history
            ORDER BY id DESC
            LIMIT 10
        """)
        return cursor.fetchall()
    except sqlite3.Error as err:
        print(f"Database error: {err}")
        return []
    finally:
        if conn is not None:
            conn.close()


def get_cached_weather(city: str):
    conn = None
    try:
        conn = sqlite3.connect("weather.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM weather_history
            WHERE LOWER(city) = LOWER(?)
              AND timestamp >= datetime('now', '-30 minutes')
            ORDER BY timestamp DESC, id DESC
            LIMIT 1
        """, (city.strip(),))
        cached = cursor.fetchone()
        if cached:
            return {
                "city": cached["city"],
                "country": cached["country"],
                "temperature": cached["temperature"],
                "feels_like": cached["feels_like"],
                "wind_speed": cached["wind_speed"],
                "weather_condition": cached["weather_condition"],
                "latitude": cached["coordinates_lat"],
                "longitude": cached["coordinates_lon"],
                "elevation": cached["elevation"],
                "humidity": cached["humidity"],
            }

        return None
    except sqlite3.Error as err:
        print(f"Database error: {err}")
        return None
    finally:
        if conn is not None:
            conn.close()
