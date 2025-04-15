import os
import sqlite3
from flask import Flask, render_template, g

app = Flask(__name__)

# Configurazione del database
DATABASE = "database.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def init_db():
    if not os.path.exists(DATABASE):
        with app.app_context():
            db = get_db()
            with app.open_resource("schema.sql", mode="r") as f:
                db.cursor().executescript(f.read())
            db.commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tornei")
def tornei():
    db = get_db()
    cursor = db.execute("SELECT * FROM TORNEO ORDER BY premio DESC")
    tornei = cursor.fetchall()
    return render_template("tornei.html", tornei=tornei)


@app.route("/teams")
def teams():
    db = get_db()
    cursor = db.execute("SELECT * FROM TEAM ORDER BY nome")
    teams = cursor.fetchall()
    return render_template("teams.html", teams=teams)


@app.route("/torneo/<int:id>")
def torneo(id):
    db = get_db()
    # Recupera informazioni sul torneo
    cursor = db.execute("SELECT * FROM TORNEO WHERE id = ?", (id,))
    torneo = cursor.fetchone()

    # Recupera i giocatori che partecipano al torneo
    cursor = db.execute(
        """
        SELECT g.id, g.username, g.email, g.livello, t.nome as team_nome
        FROM GIOCATORE g
        JOIN GIOCATORE_TORNEO gt ON g.id = gt.giocatore_id
        JOIN TEAM t ON g.team_id = t.id
        WHERE gt.torneo_id = ?
    """,
        (id,),
    )
    giocatori = cursor.fetchall()

    return render_template("torneo.html", torneo=torneo, giocatori=giocatori)


@app.route("/query")
def query():
    db = get_db()

    # 1. Somma dei premi di tutti i tornei
    cursor = db.execute("SELECT SUM(premio) as somma_premi FROM TORNEO")
    somma_premi = cursor.fetchone()["somma_premi"]

    # 2. Numero di giocatori per ogni team
    cursor = db.execute("""
        SELECT t.nome, COUNT(g.id) as num_giocatori
        FROM TEAM t
        LEFT JOIN GIOCATORE g ON t.id = g.team_id
        GROUP BY t.id
        ORDER BY t.nome
    """)
    team_giocatori = cursor.fetchall()

    # 3. Nome del team del giocatore con livello più alto
    cursor = db.execute("""
        SELECT t.nome as team_nome, g.username, g.livello
        FROM GIOCATORE g
        JOIN TEAM t ON g.team_id = t.id
        ORDER BY g.livello DESC
        LIMIT 1
    """)
    top_player_team = cursor.fetchone()

    return render_template(
        "query.html", somma_premi=somma_premi, team_giocatori=team_giocatori, top_player_team=top_player_team
    )


if __name__ == "__main__":
    init_db()  # Initialize database if it doesn't exist
    app.run(debug=True)
