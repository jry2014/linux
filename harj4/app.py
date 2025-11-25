import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Säädata", layout="wide")
st.title("Säädata oulusta")

def run_query(sql):
    conn = None
    try:
        conn = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"]
        )
        return pd.read_sql(sql, conn)
    finally:
        if conn and conn.is_connected():
            conn.close()


st.sidebar.header("Asetukset")
row_limit = st.sidebar.slider("Kuinka monta riviä näytetään?", 10, 500, 50)

sql = f"""
    SELECT *
    FROM weather_data
    ORDER BY timestamp DESC
    LIMIT {row_limit}
"""

try:
    df = run_query(sql)
    st.success("Data ladattu!")
    st.dataframe(df, use_container_width=True)

    # --- Plotly-graafi ---
    if not df.empty:
        fig = px.line(
            df.sort_values("timestamp"),  # varmista että aikajärjestys on oikea
            x="timestamp",
            y="temperature",
            labels={"timestamp": "Aikaleima", "temperature": "Lämpötila (°C)"},
            title="Lämpötila aikakehityksenä"
        )
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Virhe tietokantayhteydessä: {e}")
