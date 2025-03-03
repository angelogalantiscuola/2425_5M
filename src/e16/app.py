import json
import sqlite3
from flask import Flask, g, jsonify, render_template
import os


app = Flask(__name__)
app.secret_key = "your-secret-key-here"

with open("config.json") as config_file:
    config = json.load(config_file)
    DATABASE = config["DATABASE"]
    INITIALIZATION = config["INITIALIZATION"]


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
            db.executescript(f.read().decode("utf8"))
        db.commit()


@app.teardown_appcontext
def close_db(error):
    """Chiude la connessione al database"""
    if hasattr(g, "db"):
        g.db.close()


@app.route("/raw_giocatori")
def raw_giocatori():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM GIOCATORE")
    entries = cursor.fetchall()
    cursor.close()
    return jsonify([dict(row) for row in entries])


@app.route("/raw_giocatori_partita")
def raw_giocatori_partita():
    dato_inserito_squadra_casa = "Real Madrid"
    dato_inserito_squadra_ospite = "Manchester City"
    db = get_db()
    cursor = db.cursor()
    # selezionare l'id della partita date che come informazioni
    # la squdra di casa e la squadra ospite
    cursor.execute(
        """
    SELECT p.id as partita_id
    FROM PARTITA p
    WHERE p.squadra_casa = ? AND p.squadra_ospite = ?
    """,
        (dato_inserito_squadra_casa, dato_inserito_squadra_ospite),
    )
    partita = cursor.fetchone()
    if partita is None:
        return jsonify([])

    # selezionare i giocatori che hanno partecipato alla partita
    cursor.execute(
        """
    SELECT g.nome, g.cognome, g.ruolo
    FROM GIOCATORE g
    JOIN GIOCATORE_PARTITA gp ON g.id = gp.giocatore_id
    WHERE gp.partita_id = ?
    """,
        (partita["partita_id"],),
    )
    entries = cursor.fetchall()
    cursor.close()
    # return jsonify(dict(partita))
    return jsonify([dict(row) for row in entries])


@app.route("/giocatori_partita")
def giocatori_partita():
    squadra_casa = "Real Madrid"
    squadra_ospite = "Manchester City"
    db = get_db()
    cursor = db.cursor()
    # selezionare l'id della partita date che come informazioni
    # la squdra di casa e la squadra ospite
    cursor.execute(
        """
    SELECT p.id as partita_id
    FROM PARTITA p
    WHERE p.squadra_casa = ? AND p.squadra_ospite = ?
    """,
        (squadra_casa, squadra_ospite),
    )
    partita = cursor.fetchone()
    if partita is None:
        return jsonify([])

    # selezionare i giocatori che hanno partecipato alla partita
    cursor.execute(
        """
    SELECT g.nome, g.cognome, g.ruolo
    FROM GIOCATORE g
    JOIN GIOCATORE_PARTITA gp ON g.id = gp.giocatore_id
    WHERE gp.partita_id = ?
    """,
        (partita["partita_id"],),
    )
    righe_della_tabella = cursor.fetchall()
    cursor.close()
    # return render_template("giocatori_partita.html")
    return render_template("giocatori_partita.html", giocatori=righe_della_tabella, squadra_casa=squadra_casa)


@app.route("/")  # Add default route
@app.route("/giocatori")
def giocatori():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT g.*, a.nome as allenatore_nome, a.cognome as allenatore_cognome 
        FROM GIOCATORE g 
        LEFT JOIN ALLENATORE a ON g.allenatore_id = a.id
    """)
    entries = cursor.fetchall()
    cursor.close()
    return render_template("giocatori.html", entries=entries)


if __name__ == "__main__":
    # check if the file database exists
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True, port=50849)
