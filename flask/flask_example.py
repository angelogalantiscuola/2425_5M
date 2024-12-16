from flask import (
    Flask,
    jsonify,
    render_template,
    send_from_directory,
    request,
    session,
    redirect,
    url_for,
)
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Required for session

# Database connection configuration
db_config = {
    "user": "x",
    "password": "x",
    "host": "localhost",
    "database": "teachers",
}


def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/esempio")
def metodo_ciao():
    return "Ciao"


@app.route("/somma")
def somma():
    return str(4 + 5)


@app.route("/data")
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teacher")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)


@app.route("/hello")
def static_example():
    return send_from_directory("static", "example.html")


@app.route("/user/<username>")
def show_user(username):
    return render_template("user.html", username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # This is a simple example - in real applications, use proper authentication
        if username == "admin" and password == "password":
            session["logged_in"] = True
            session["username"] = username
            # invia l'utente alla pagina della tabella
            # che ha come metodo show_table --> /table
            return redirect(url_for("show_table"))

        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/table")
def show_table():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teacher")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("table.html", rows=rows)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
