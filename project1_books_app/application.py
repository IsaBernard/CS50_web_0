import os

from flask import Flask, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

DATABASE_URL = os.getenv('DATABASE_URL')

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    username = request.form.get("username")
    password = request.form.get("password")
    user = db.execute("SELECT username from users "
                      "WHERE username=:username AND password=:password",
                      {"username": username, "password": password}).fetchone()
    db.commit()
    if user is None:
        return "Invalid login"
    else:
        return render_template("index.html", username=username, password=password)


@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    if request.method == "GET":
        return "Please login first."
    else:
        username = request.form.get("username")
        return render_template("welcome.html", username=username)


@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form.get("username")
    password = request.form.ger("password")
    user = db.execute("SELECT username from users "
                      "WHERE username=:username",
                      {"username": username}).fetchone()
    db.commit()
    if user is None:
        return render_template("register.html")
    else:
        return "username already taken"


@app.route("/thanks", methods=["GET", "POST"])
def thanks():
    if request.method == "GET":
        return "Please register or login first."
    else:
        username = request.form.get("username")
        return render_template("thanks.html", username=username)


if __name__ == '__main__':
    app.run(debug=True)


"""
To do:
- créer les tables users et books.
- plutôt que de return Please register or login, créer un template error.html
- changer la variable message du template.
- 1:25:49
    
"""