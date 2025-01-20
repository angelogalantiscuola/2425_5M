import json
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
)
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "your-secret-key-here"  # Change this to a secure secret key


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="x",
        password="x",
        database="albergo",
    )


@app.route("/raw")
def list_entries_raw():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM CAMERA")
    entries = cursor.fetchall()
    cursor.close()
    conn.close()
    return entries

@app.route("/")
def list_entries():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM CAMERA")
    entries = cursor.fetchall()
    cursor.close()
    conn.close()
    # return entries
    return render_template("list.html", entries=entries)

@app.route("/add", methods=("GET", "POST"))
def add_entries():
    if request.method == "POST":
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # TODO controllo che non esista già una camera 
        # con lo stesso numero
        numero = request.form["numero"]
        tipo = request.form["tipo"]
        disponibile = bool(request.form["disponibile"])
        prezzo = request.form["prezzo"]
        numero_posti = request.form["numero_posti"]

        # Create room
        cursor.execute(
            "INSERT INTO CAMERA (numero, tipo, disponibile, prezzo, numero_posti) VALUES (%s, %s, %s, %s, %s)",
            (numero, tipo, disponibile, prezzo, numero_posti),
        )
        conn.commit()    
        cursor.close()
        conn.close()
        return redirect(url_for("list_entries"))
    return render_template("add.html")

if __name__ == "__main__":


    app.run(debug=True)
