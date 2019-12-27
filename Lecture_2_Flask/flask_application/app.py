from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    names = ["Alice", "Bob", "Isa"]
    return render_template("index.html", names=names)


@app.route("/more")
def more():
    return render_template("more.html")








