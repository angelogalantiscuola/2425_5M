from dataclasses import dataclass
from datetime import date
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


@dataclass
class Allenatore:
    id: int
    nome: str
    cognome: str


@dataclass
class Giocatore:
    id: int
    nome: str
    cognome: str
    ruolo: str
    allenatore_id: int


@dataclass
class Partita:
    id: int
    data: date
    squadra_casa: str
    squadra_ospite: str


@dataclass
class GiocatorePartita:
    partita_id: int
    giocatore_id: int
    ha_segnato: bool


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


# @ is a decorator
@app.route("/raw_giocatori")
def raw_giocatori():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM GIOCATORE")
    rows = cursor.fetchall()
    cursor.close()

    giocatori = [
        Giocatore(
            id=row["id"],
            nome=row["nome"],
            cognome=row["cognome"],
            ruolo=row["ruolo"],
            allenatore_id=row["allenatore_id"],
        )
        for row in rows
    ]

    return jsonify([{"nome": g.nome, "cognome": g.cognome} for g in giocatori])


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
    SELECT g.*
    FROM GIOCATORE g
    JOIN GIOCATORE_PARTITA gp ON g.id = gp.giocatore_id
    WHERE gp.partita_id = ?
    """,
        (partita["partita_id"],),
    )
    rows: list[Giocatore] = cursor.fetchall()
    cursor.close()

    giocatori_python: list[Giocatore] = [
        Giocatore(
            id=row["id"],
            nome=row["nome"],
            cognome=row["cognome"],
            ruolo=row["ruolo"],
            allenatore_id=row["allenatore_id"],
        )
        for row in rows
    ]

    return render_template(
        "giocatori_partita.html",
        giocatori_er=giocatori_python,
        squadra_casa=squadra_casa,
        squadra_ospite=squadra_ospite,
        partita=partita["partita_id"],
    )


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
    rows = cursor.fetchall()
    cursor.close()

    giocatori = [
        Giocatore(
            id=row["id"],
            nome=row["nome"],
            cognome=row["cognome"],
            ruolo=row["ruolo"],
            allenatore_id=row["allenatore_id"],
        )
        for row in rows
    ]
    return render_template("giocatori.html", entries=giocatori)


if __name__ == "__main__":
    # check if the file database exists
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True, port=50849)
