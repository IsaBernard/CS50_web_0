import os

from flask import Flask, session, render_template, request
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


@app.route("/", methods=["POST", "GET"])
def index():
    username = request.form.get("username")
    password = request.form.get("password")
    return render_template("index.html", username=username, password=password)


if __name__ == '__main__':
    app.run(debug=True)


"""
To do:
- créer la page pour register et l'envoyer dans Database
- ensuite renvoyer à index.
- dans index essayer pour voir si l'usager est dans la db.
    - sinon: message, please register
    - si oui: page welcome
    
"""