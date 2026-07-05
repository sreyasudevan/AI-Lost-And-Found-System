from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def calculate_similarity(text1, text2):

    if text1 == "" or text2 == "":
        return 0

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([text1, text2])

    similarity = cosine_similarity(
        vectors[0],
        vectors[1]
    )[0][0]

    return round(similarity * 100, 2)


def init_db():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS lost_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        contact TEXT,
        item_name TEXT,
        description TEXT,
        location TEXT,
        date TEXT,
        image TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS found_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT,
        description TEXT,
        location TEXT,
        date TEXT,
        contact TEXT,
        image TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS matches(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lost_id INTEGER,
        found_item TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM lost_items")
    lost_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM found_items")
    found_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM matches")
    match_count = cur.fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        lost_count=lost_count,
        found_count=found_count,
        match_count=match_count
    )


@app.route("/lost", methods=["GET", "POST"])
def lost():

    if request.method == "POST":

        image = request.files["image"]

        filename = ""

        if image.filename != "":
            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        name = request.form["name"]
        contact = request.form["contact"]
        item = request.form["item"]
        description = request.form["description"]
        location = request.form["location"]
        date = request.form["date"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO lost_items
        (name,contact,item_name,description,location,date,image)
        VALUES (?,?,?,?,?,?,?)
        """,
        (
            name,
            contact,
            item,
            description,
            location,
            date,
            filename
        ))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("lost.html")


@app.route("/found", methods=["GET", "POST"])
def found():

    match = None
    score = 0

    if request.method == "POST":

        image = request.files["image"]

        filename = ""

        if image.filename != "":
            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        item = request.form["item"]
        description = request.form["description"]
        location = request.form["location"]
        date = request.form["date"]
        contact = request.form["contact"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO found_items
        (item_name,description,location,date,contact,image)
        VALUES (?,?,?,?,?,?)
        """,
        (
            item,
            description,
            location,
            date,
            contact,
            filename
        ))

        conn.commit()

        cur.execute("SELECT * FROM lost_items")

        lost_items = cur.fetchall()

        best_match = None
        best_score = 0

        for lost in lost_items:

            similarity = calculate_similarity(
                description.lower(),
                lost[4].lower()
            )

            if similarity > best_score:
                best_score = similarity
                best_match = lost

        if best_score >= 40:

            match = best_match
            score = best_score

            cur.execute("""
            INSERT INTO matches
            (lost_id, found_item)
            VALUES (?,?)
            """,
            (
                match[0],
                item
            ))

            conn.commit()

        conn.close()

        return render_template(
            "found.html",
            match=match,
            score=score
        )

    return render_template(
        "found.html",
        match=None,
        score=0
    )


@app.route("/search", methods=["GET", "POST"])
def search():

    lost = []
    found = []

    if request.method == "POST":

        item = request.form["item"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM lost_items WHERE item_name LIKE ?",
            ('%' + item + '%',)
        )

        lost = cur.fetchall()

        cur.execute(
            "SELECT * FROM found_items WHERE item_name LIKE ?",
            ('%' + item + '%',)
        )

        found = cur.fetchall()

        conn.close()

    return render_template(
        "search.html",
        lost=lost,
        found=found
    )


@app.route("/admin")
def admin():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM lost_items")
    lost = cur.fetchall()

    cur.execute("SELECT * FROM found_items")
    found = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM matches")
    matches = cur.fetchone()[0]

    conn.close()

    return render_template(
        "admin.html",
        lost=lost,
        found=found,
        matches=matches
    )


if __name__ == "__main__":
    app.run(debug=True)