import streamlit as st
import mysql.connector

# Yhdistä MySQL:ään
conn = mysql.connector.connect(
    host="localhost",
    user="ubuntu",
    password="1234",
    database="test1"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM people")
data = cursor.fetchall()

st.title("Data Analysis App")
st.write("MySQL-tietokannasta haettu data:")
st.dataframe(data)
