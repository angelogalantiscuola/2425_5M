from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from database import get_eventi_gia_svolti, get_membri_senza_commenti, get_voto_medio_per_evento, get_utente_con_piu_eventi

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chiave_segreta_per_la_sessione'
app.config['DATABASE'] = 'eventi_community.db'

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def close_db_connection(e=None):
    db = get_db_connection()
    if db:
        db.close()

import os

def init_db():
    db_path = app.config['DATABASE']
    if os.path.exists(db_path):
        os.remove(db_path)
    db = get_db_connection()
    with open('eventi_community.sql', 'r') as f:
        sql = f.read()
    db.cursor().executescript(sql)
    db.commit()
    close_db_connection()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/eventi_gia_svolti')
def eventi_gia_svolti():
    eventi = get_eventi_gia_svolti()
    return render_template('eventi_gia_svolti.html', eventi=eventi)

@app.route('/membri_senza_commenti')
def membri_senza_commenti():
    membri = get_membri_senza_commenti()
    return render_template('membri_senza_commenti.html', membri=membri)

@app.route('/voto_medio_per_evento')
def voto_medio_per_evento():
    eventi = get_voto_medio_per_evento()
    return render_template('voto_medio_per_evento.html', eventi=eventi)

@app.route('/utente_con_piu_eventi')
def utente_con_piu_eventi():
    utente = get_utente_con_piu_eventi()
    return render_template('utente_con_piu_eventi.html', utente=utente)

if __name__ == '__main__':
    # Check if the database exists
    if not os.path.exists(app.config['DATABASE']):
        print("Database does not exist. Creating and initializing...")
        with app.app_context():
            init_db()
    app.run(debug=True)
