import json
import re
import sqlite3
from flask import (
    Flask,
    g,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
)
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "your-secret-key-here"

with open('config.json') as config_file:
    config = json.load(config_file)
    DATABASE = config['DATABASE']
    INITIALIZATION = config['INITIALIZATION']

def get_db():
    """Connessione al database"""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    """Inizializza il database"""
    with app.app_context():
        db = get_db()
        # Load schema from queries folder
        with app.open_resource(INITIALIZATION) as f:
            db.executescript(f.read().decode('utf8'))
        db.commit()

@app.teardown_appcontext
def close_db(error):
    """Chiude la connessione al database"""
    if hasattr(g, 'db'):
        g.db.close()


@app.route("/raw_squadre")
def raw_squadre():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM SQUADRA")
    entries = cursor.fetchall()
    cursor.close()
    return jsonify([dict(row) for row in entries])

@app.route("/squadre")
def squadre():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM SQUADRA")
    entries = cursor.fetchall()
    cursor.close()
    return render_template("squadre.html", entries=entries)


if __name__ == "__main__":
    # check if the file DATABASE exists
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True, port=50849)