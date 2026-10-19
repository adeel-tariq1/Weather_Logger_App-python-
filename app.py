
import streamlit as st
import pandas as pd

from main import get_weather
from database import create_table, get_history


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Weather Logger | Dashboard",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

create_table()


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
    /* Main application background */
    .stApp {
        background: linear-gradient(
            145deg,
            #0b1220 0%,
            #101b30 55%,
            #14243b 100%
        );
        color: #f1f5f9;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0a1020;
        border-right: 1px solid #26364d;
    }

    /* Hero section */
    .hero {
        background: linear-gradient(
            120deg,
            #172d4d,
            #234e70,
            #176b87
        );
        border: 1px solid rgba(148, 197, 230, 0.25);
        padding: 32px;
        border-radius: 22px;
        margin-bottom: 28px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.20);
    }

    .hero-label {
        color: #a9dff5;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .hero-title {
        color: #ffffff;
        font-size: 36px;
        font-weight: 750;
        margin: 10px 0;
    }

    .hero-description {
        color: #d0e3f1;
        font-size: 15px;
        margin-bottom: 0;
    }

    /* Section headings */
    h2, h3 {
        color: #f1f5f9 !important;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #17263b, #142237);
        border: 1px solid #2b405b;
        padding: 20px;
        border-radius: 16px;
        min-height: 125px;
        box-shadow: 0 5px 16px rgba(0, 0, 0, 0.12);
    }

    [data-testid="stMetricLabel"] {
        color: #a9bdd4 !important;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-size: 27px;
    }

    /* Search form */
    [data-testid="stForm"] {
        background-color: #121f33;
        border: 1px solid #2b405b;
        padding: 22px;
        border-radius: 18px;
    }

    /* Buttons */
    .stButton > button,
    [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(90deg, #1687b8, #2563eb);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 650;
        min-height: 43px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] > button:hover {
        border: 1px solid #8bdcff;
        color: white;
        filter: brightness(1.12);
    }

    /* Input fields */
    [data-testid="stTextInput"] input {
        background-color: #0d1728;
        color: #ffffff;
        border: 1px solid #344963;
        border-radius: 10px;
    }

    /* Weather condition panel */
    .condition-panel {
        background: linear-gradient(110deg, #16354a, #172b43);
        border: 1px solid #2b536b;
        border-radius: 16px;
        padding: 22px 24px;
        margin: 16px 0 22px 0;
    }

    .condition-label {
        color: #91cfe9;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.4px;
        text-transform: uppercase;
    }

    .condition-value {
        color: #ffffff;
        font-size: 25px;
        font-weight: 700;
        margin-top: 7px;
    }

    /* General text */
    .muted {
        color: #9fb0c5;
        font-size: 13px;
    }

    hr {
        border-color: #293b52;
        margin-top: 28px;
        margin-bottom: 28px;
    }

    /* History table */
    [data-testid="stDataFrame"] {
        border: 1px solid #2b405b;
        border-radius: 12px;
        overflow: hidden;
    }

    /* Footer */
    .footer {
        color: #8194ab;
        font-size: 12px;
        text-align: center;
        padding-top: 25px;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 10px 0 22px 0;">
            <h2 style="margin-bottom: 6px;">🌦️ Weather Logger</h2>
            <p style="font-size: 14px; color: #b8c7d9; line-height: 1.6;">
                Current conditions, location insights, and your personal
                weather history — all in one place.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    page = st.radio(
        "Navigation",
        ["Weather Dashboard", "Search History"],
        label_visibility="collapsed",
    )



# --------------------------------------------------
# MAIN PAGE
# --------------------------------------------------

if page == "Weather Dashboard":

    # Compact page title
    st.markdown(
        """
        <div style="
            margin: 0 0 22px 0;
            padding: 15px 22px;
            background: linear-gradient(100deg, #172d4d, #1b3b56);
            border: 1px solid #2b405b;
            border-radius: 14px;
            max-width: 100%;
        ">
            <div style="
                color: #ffffff;
                font-size: 25px;
                font-weight: 700;
                margin: 0;
            ">🌦️ Weather Dashboard</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Display the latest weather report
    weather = st.session_state.get("weather_result")

    if isinstance(weather, dict):
        st.markdown(
            f"""
            <div class="condition-panel" style="margin-top:0;">
                <div class="condition-label">CURRENT WEATHER</div>
                <div style="display:flex;
                            justify-content:space-between;
                            align-items:center;
                            flex-wrap:wrap;
                            gap:12px;">
                    <div>
                        <div class="condition-value">
                            {weather["weather_condition"]}
                        </div>
                        <div style="color:#d0e3f1;
                                    font-size:17px;
                                    margin-top:6px;">
                            {weather["city"]}, {weather["country"]}
                        </div>
                    </div>
                    <div style="font-size:42px;
                                font-weight:750;
                                color:white;">
                        {weather["temperature"]:.1f}°C
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Feels Like", f'{weather["feels_like"]:.1f} °C')
        col2.metric("Humidity", f'{weather["humidity"]}%')
        col3.metric("Wind Speed", f'{weather["wind_speed"]:.1f} km/h')
        col4.metric("Elevation", f'{weather["elevation"]:.0f} m')

        st.caption(
            f'📍 Latitude: {weather["latitude"]}°  ·  '
            f'Longitude: {weather["longitude"]}°'
        )

    elif weather is not None:
        st.error(str(weather))
    else:
        st.info("🌤️ Search for a city below to view its weather.")

    # Search form below the weather report
    st.divider()
    st.subheader("🔎 Search Another City")

    with st.form("weather_search", clear_on_submit=False):
        city_name = st.text_input(
            "City name",
            placeholder="e.g. Lahore, Islamabad, London",
        )

        search_button = st.form_submit_button(
            "Get Weather",
            use_container_width=True,
        )

    if search_button:
        if not city_name.strip():
            st.warning("Please enter a city name.")
        else:
            with st.spinner(f"Fetching weather for {city_name.strip()}..."):
                result = get_weather(city_name.strip())
                st.session_state["weather_result"] = result

            st.rerun()


elif page == "Search History":

    st.markdown(
        """
        <div style="
            margin: 0 0 22px 0;
            padding: 15px 22px;
            background: linear-gradient(100deg, #172d4d, #1b3b56);
            border: 1px solid #2b405b;
            border-radius: 14px;
        ">
            <div style="
                color: #ffffff;
                font-size: 25px;
                font-weight: 700;
            ">🗃️ Search History</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="muted">Your most recent saved weather records.</p>',
        unsafe_allow_html=True,
    )

    history = get_history()

    if history:
        columns = [
            "ID",
            "City",
            "Country",
            "Temperature (°C)",
            "Feels Like (°C)",
            "Wind Speed (km/h)",
            "Condition",
            "Latitude",
            "Longitude",
            "Elevation (m)",
            "Humidity (%)",
            "Timestamp (UTC)",
        ]

        history_df = pd.DataFrame(history, columns=columns)

        col1, col2 = st.columns(2)
        col1.metric("Saved records", len(history_df))
        col2.metric("Unique cities", history_df["City"].nunique())

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Temperature (°C)": st.column_config.NumberColumn(
                    format="%.1f °C"
                ),
                "Feels Like (°C)": st.column_config.NumberColumn(
                    format="%.1f °C"
                ),
                "Wind Speed (km/h)": st.column_config.NumberColumn(
                    format="%.1f km/h"
                ),
                "Humidity (%)": st.column_config.NumberColumn(
                    format="%d%%"
                ),
                "Latitude": st.column_config.NumberColumn(
                    format="%.2f°"
                ),
                "Longitude": st.column_config.NumberColumn(
                    format="%.2f°"
                ),
                "Elevation (m)": st.column_config.NumberColumn(
                    format="%.0f m"
                ),
            },
        )

        st.download_button(
            "⬇️ Export History as CSV",
            data=history_df.to_csv(index=False).encode("utf-8"),
            file_name="weather_history.csv",
            mime="text/csv",
            use_container_width=True,
        )

        if st.button("🔄 Refresh History"):
            st.rerun()

    else:
        st.info(
            "No saved records yet. Visit the Weather Dashboard "
            "and search for a city first."
        )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    WEATHER LOGGER &nbsp; • &nbsp; Built with Python, Streamlit,
    SQLite and Open-Meteo
</div>
""", unsafe_allow_html=True)
