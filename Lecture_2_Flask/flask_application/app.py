from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/hello_2", methods=["POST"])
def hello():
    name = request.form.get("name")
    return render_template("hello_2.html", name=name)


@app.route("/more")
def more():
    return render_template("more.html")








