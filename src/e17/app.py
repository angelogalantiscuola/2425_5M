from flask import Flask, render_template, g
import sqlite3
import os

app = Flask(__name__)
DATABASE = "database.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "db"):
        g.db.close()


def init_db():
    if not os.path.exists(DATABASE):
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/telescopi")
def telescopi():
    db = get_db()
    telescopi = db.execute("SELECT * FROM TELESCOPIO ORDER BY apertura DESC").fetchall()
    return render_template("telescopi.html", telescopi=telescopi)


@app.route("/corpi")
def corpi():
    db = get_db()
    corpi = db.execute("SELECT * FROM CORPO_CELESTE ORDER BY distanza_parsec").fetchall()
    return render_template("corpi.html", corpi=corpi)


@app.route("/ricercatore/<int:id>")
def ricercatore(id):
    db = get_db()
    osservazioni = db.execute(
        """
        SELECT O.*, C.nome as corpo_nome, C.categoria
        FROM OSSERVAZIONE O
        JOIN RICERCATORE_OSSERVAZIONE RO ON O.id = RO.osservazione_id
        JOIN CORPO_CELESTE C ON O.corpo_celeste_id = C.id
        WHERE RO.ricercatore_id = ?
        ORDER BY O.timestamp DESC
    """,
        [id],
    ).fetchall()
    ricercatore = db.execute("SELECT * FROM RICERCATORE WHERE id = ?", [id]).fetchone()
    return render_template("ricercatore.html", ricercatore=ricercatore, osservazioni=osservazioni)


@app.route("/statistiche")
def statistiche():
    db = get_db()

    media_osservazioni = db.execute("""
        SELECT AVG(cnt) as media
        FROM (SELECT COUNT(*) as cnt FROM OSSERVAZIONE GROUP BY telescopio_id)
    """).fetchone()

    corpo_frequente = db.execute("""
        SELECT C.nome, COUNT(*) as conteggio
        FROM OSSERVAZIONE O
        JOIN CORPO_CELESTE C ON O.corpo_celeste_id = C.id
        GROUP BY C.id
        ORDER BY conteggio DESC
        LIMIT 1
    """).fetchone()

    return render_template(
        "statistiche.html",
        media_osservazioni=media_osservazioni,
        corpo_frequente=corpo_frequente,
    )


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)
