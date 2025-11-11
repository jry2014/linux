from flask import Flask, render_template, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def get_db_time():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="ubuntu",
            password="1234",
            database="test1"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT NOW();")
        row = cursor.fetchone()
        return str(row[0])
    except Error as e:
        return f"DB error: {e}"
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/")
def index():
    db_time = get_db_time()
    return render_template("index.html", db_time=db_time)

@app.route("/time")
def time_api():
    db_time = get_db_time()
    return jsonify({"ok": True, "time": db_time})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
