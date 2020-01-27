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

# if table books doesn't exist, create it
if not engine.dialect.has_table(engine, "books"):
    db.execute('CREATE TABLE "books" ('
               'isbn Integer NOT NULL,'
               'title VARCHAR NOT NULL,'
               'author VARCHAR NOT NULL,'
               'year INTEGER NOT NULL,'
               'PRIMARY KEY (isbn));')
    db.commit()
# if table users doesn't exist, crate it
if not engine.dialect.has_table(engine, "users"):
    db.execute('CREATE TABLE "users" ('
               'username VARCHAR PRIMARY KEY,'
               'password VARCHAR NOT NULL);'
               )
    db.commit()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form.get("new_username")
    password = request.form.get("new_password")
    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
               {"username": username, "password": password})
    db.commit()
    return render_template("register.html")


@app.route("/thanks", methods=["GET", "POST"])
def thanks():
    if request.method == "GET":
        return render_template("error.html", message="Please register or login first")

    username = request.form.get("new_username")
    password = request.form.get("new_password")
    user = db.execute("SELECT username from users "
                      "WHERE username=:username",
                      {"username": username}).fetchone()
    if user is not None:
        return render_template("error.html", message="User already taken")
    else:
        username = request.form.get("username")
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                   {"username": username, "password": password})
        db.commit()
        return render_template("thanks.html", username=username)


@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    if request.method == "GET":
        return render_template("error.html", message="Please login first")
    username = request.form.get("username")
    password = request.form.get("password")
    if db.execute("SELECT username from users "
                  "WHERE username=:username AND password=:password",
                  {"username": username, "password": password}).rowcount == 0:
        return render_template("error.html", message="Invalid login info.")
    return render_template("welcome.html", username=username)


if __name__ == '__main__':
    app.run(debug=True)
