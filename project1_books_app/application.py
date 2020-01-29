import os

from flask import Flask, render_template, request, session, redirect
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
if not engine.dialect.has_table(engine, "books4"):
    db.execute('CREATE TABLE "books4" ('
               'isbn VARCHAR NOT NULL,'
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


@app.route("/test_password")
def test():
    users = db.execute("SELECT username, password FROM users").fetchall()
    return render_template("test.html", users=users)


@app.route("/new", methods=["POST"])
def new():
    """Register a new user."""

    username = request.form.get("new_username")
    password = request.form.get("new_password")

    if db.execute("SELECT * from users WHERE username = :username", {"username": username}).rowcount > 0:
        return render_template("error.html", message="User already exists.")
    try:
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                   {"username": username, "password": password})
        db.commit()
    except ValueError:
        return render_template("error.html", message="Insertion did not work")
    return render_template("thanks.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


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


@app.route("/logout")
def logout():
    """ Log user out """

    # Forget any user ID
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)

"""
Once they log in, they will be able to search for books, leave reviews for individual books, 
and see the reviews made by other people. You’ll also use the a third-party API by Goodreads, 
another book review website, to pull in ratings from a broader audience. 
Finally, users will be able to query for book details and book reviews programmatically via your 
website’s API.

- OK Registration: Users should be able to register for your website, providing (at minimum) 
a username and password.

- OK Login: Users, once registered, should be able to log in to your website with their 
username and password.

- OK (copié d'un exemple): Logout: Logged in users should be able to log out of the site.
Hint: In terms of how to “log a user in,” recall that you can store information inside of the 
session, which can store different values for different users. In particular, if each user has 
an id, then you could store that id in the session (e.g., in session["user_id"]) to keep track 
of which user is currently logged in.

- OK Import: Provided for you in this project is a file called books.csv, which is a spreadsheet 
in CSV format of 5000 different books. Each one has an ISBN number, a title, an author, and a 
publication year. In a Python file called import.py separate from your web application, 
write a program that will take the books and import them into your PostgreSQL database. 
You will first need to decide what table(s) to create, what columns those tables should have, 
and how they should relate to one another. Run this program by running python3 import.py to 
import the books into your database, and submit this program with the rest of your project code.

TO DO:
- One table for reviews

- Search: Once a user has logged in, they should be taken to a page where they can 
search for a book. Users should be able to type in the ISBN number of a book, the title of a book,
 or the author of a book. After performing the search, your website should display a list of 
 possible matching results, or some sort of message if there were no matches. If the user typed
 in only part of a title, ISBN, or author name, your search page should find matches for those as well!
 
- Book Page: When users click on a book from the results of the search page, they should 
be taken to a book page, with details about the book: its title, author, publication year, 
ISBN number, and any reviews that users have left for the book on your website.

- Review Submission: On the book page, users should be able to submit a review: consisting of 
a rating on a scale of 1 to 5, as well as a text component to the review where the user can 
write their opinion about a book. Users should not be able to submit multiple reviews for the 
same book.

- Goodreads Review Data: On your book page, you should also display (if available) the average 
rating and number of ratings the work has received from Goodreads.

- API Access: If users make a GET request to your website’s /api/<isbn> route, where <isbn> is 
an ISBN number, your website should return a JSON response containing the book’s title, author, 
publication date, ISBN number, review count, and average score. The resulting JSON should 
follow the format:
{
    "title": "Memory",
    "author": "Doug Lloyd",
    "year": 2015,
    "isbn": "1632168146",
    "review_count": 28,
    "average_score": 5.0
}
If the requested ISBN number isn’t in your database, your website should return a 404 error.

- You should be using raw SQL commands (as via SQLAlchemy’s execute method) in order to make 
database queries. You should not use the SQLAlchemy ORM (if familiar with it) for this project.

- In README.md, include a short writeup describing your project, what’s contained in each file, 
and (optionally) any other additional information the staff should know about your project.

- If you’ve added any Python packages that need to be installed in order to run your web 
application, be sure to add them to requirements.txt!

"""