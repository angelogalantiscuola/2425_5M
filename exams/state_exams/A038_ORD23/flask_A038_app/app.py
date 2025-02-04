from flask import Flask, render_template, g, jsonify
import sqlite3
import os
from queries.queries import QUERIES

app = Flask(__name__)
app.jinja_env.globals.update(enumerate=enumerate)

# Configurazione del database
DATABASE = "educational_games.db"


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
    with app.open_resource("queries/schema.sql") as f:
        db.executescript(f.read().decode("utf8"))
    # Load sample data from queries folder
    with app.open_resource("queries/data.sql") as f:
        db.executescript(f.read().decode("utf8"))
    db.commit()


@app.route("/")
def index():
    """Pagina principale"""
    db = get_db()
    giochi = db.execute(QUERIES.get("Get all games")).fetchall()
    return render_template("giochi.html", giochi=giochi)


@app.route("/giochi")
def lista_giochi():
    """Lista di tutti i giochi disponibili"""
    db = get_db()
    giochi = db.execute(QUERIES.get("Get all games")).fetchall()
    return render_template("giochi.html", giochi=giochi)


@app.route("/giochi/raw")
def lista_giochi_raw():
    """Lista di tutti i giochi disponibili in formato JSON"""
    db = get_db()
    giochi = db.execute(QUERIES.get("Get all games")).fetchall()
    return jsonify([dict(gioco) for gioco in giochi])


@app.route("/gioco/<int:id>")
def dettaglio_gioco(id):
    """Dettagli di un gioco specifico"""
    db = get_db()
    gioco = db.execute(QUERIES.get("Get game details"), [id]).fetchone()
    classifica = db.execute(QUERIES.get("Get game leaderboard"), [id]).fetchall()
    return render_template("gioco.html", gioco=gioco, classifica=classifica)


@app.route("/gioco/<int:id>/raw")
def dettaglio_gioco_raw(id):
    """Dettagli di un gioco specifico in formato JSON"""
    db = get_db()
    gioco = db.execute(QUERIES.get("Get game details"), [id]).fetchone()
    classifica = db.execute(QUERIES.get("Get game leaderboard"), [id]).fetchall()
    return jsonify(
        {
            "gioco": dict(gioco) if gioco else None,
            "classifica": [dict(score) for score in classifica],
        }
    )


# Registra la funzione di chiusura del database
app.teardown_appcontext(close_db)

if __name__ == "__main__":
    # Se il database non esiste, lo crea e lo inizializza
    if not os.path.exists(os.path.join(os.path.dirname(__file__), DATABASE)):
        with app.app_context():
            init_db()
    app.run(debug=True)
