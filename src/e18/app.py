import os
import sqlite3
import configparser
from flask import Flask, render_template, request, redirect, url_for, session, g, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load application configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)

# Configuration settings
app.config["DATABASE"] = config['database']['DATABASE_PATH']
app.config["UPLOAD_FOLDER"] = config['uploads']['UPLOAD_FOLDER']
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
ALLOWED_EXTENSIONS = set(config['uploads']['ALLOWED_EXTENSIONS'].split(','))

# Ensure upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "db"):
        g.db.close()


def init_db():
    if not os.path.exists(app.config["DATABASE"]):
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    files = db.execute(
        "SELECT * FROM files WHERE user_id = ? ORDER BY upload_date DESC", (session["user_id"],)
    ).fetchall()
    return render_template("files.html", files=files)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        if db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone():
            flash("Username already exists.")
            return redirect(url_for("register"))
        password_hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        db.commit()
        flash("Registration successful. Please log in.")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("index"))
        flash("Invalid username or password.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part.")
            return redirect(request.url)
        file = request.files["file"]
        if not file or not file.filename or file.filename.strip() == "":
            flash("No selected file.")
            return redirect(request.url)
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            unique_filename = f"{session['user_id']}_{timestamp}_{filename}"
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], unique_filename))
            db = get_db()
            db.execute(
                "INSERT INTO files (filename, original_name, user_id) VALUES (?, ?, ?)",
                (unique_filename, filename, session["user_id"]),
            )
            db.commit()
            flash("File uploaded successfully.")
            return redirect(url_for("index"))
        else:
            flash("Only PDF files are allowed.")
    return render_template("upload.html")


@app.route("/delete/<int:file_id>", methods=["POST"])
def delete_file(file_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    file = db.execute("SELECT * FROM files WHERE id = ? AND user_id = ?", (file_id, session["user_id"])).fetchone()
    if file:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file["filename"])
        if os.path.exists(file_path):
            os.remove(file_path)
        db.execute("DELETE FROM files WHERE id = ?", (file_id,))
        db.commit()
        flash("File deleted.")
    else:
        flash("File not found or permission denied.")
    return redirect(url_for("index"))


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    file = db.execute(
        "SELECT * FROM files WHERE filename = ? AND user_id = ?", (filename, session["user_id"])
    ).fetchone()
    if file:
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
    else:
        flash("File not found or permission denied.")
        return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=config.getboolean('app', 'DEBUG'))
