import os
import json
import sqlite3
# from flask import Flask, render_template
from flask import Flask, render_template, g, jsonify

app = Flask(__name__)

with open('config.json') as config_file:
    config = json.load(config_file)
    DATABASE = config['DATABASE']
    INITIALIZATION = config['INITIALIZATION']


def get_db():
    """Connessione al database"""
    if "db" not in g:
        g.db = sqlite3.connect(
            os.path.join(os.path.dirname(__file__), DATABASE),
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """Chiude la connessione al database"""
    db = g.pop("db", None)
    if db is not None:
        db.close()



def init_db():
    """Inizializza il database"""
    db = get_db()
    # Load schema from queries folder
    with app.open_resource(INITIALIZATION) as f:
        db.executescript(f.read().decode("utf8"))
    db.commit()


@app.route("/apiari")
def lista_apiari():
    db = get_db()
    apiari = db.execute("""
        SELECT a.*, ap.nome as apicoltore_nome, ap.cognome as apicoltore_cognome,
               m.denominazione as miele_denominazione, tm.nome as tipologia
        FROM Apiario a
        JOIN Apicoltore ap ON a.apicoltore_id = ap.id
        JOIN Miele m ON a.miele_id = m.id
        JOIN TipologiaMiele tm ON m.tipologia_id = tm.id
        ORDER BY a.regione, a.provincia, a.comune
    """).fetchall()
    return render_template("apiari.html", apiari=apiari)

@app.route("/test_raw")
def test_raw():
    db = get_db()
    apiari = db.execute("""
                        SELECT * FROM Apiario
                        """).fetchall()
    # return a json
    return jsonify([dict(apiario) for apiario in apiari])


# Registra la funzione di chiusura del database
app.teardown_appcontext(close_db)

if __name__ == "__main__":
    # Remove the database file if it exists
    if os.path.exists(os.path.join(os.path.dirname(__file__), DATABASE)):
        os.remove(os.path.join(os.path.dirname(__file__), DATABASE))
        print("Removed database file")
    # Se il database non esiste, lo crea e lo inizializza
    if not os.path.exists(os.path.join(os.path.dirname(__file__), DATABASE)):
        with app.app_context():
            init_db()
    app.run(debug=True)
