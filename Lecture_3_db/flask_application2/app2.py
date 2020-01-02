import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("index2.html", flights=flights)


@app.route("/book", methods=["POST"])
def book():
    """Book a flight"""

    # Get form information.
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:





