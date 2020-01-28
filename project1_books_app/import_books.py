import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


if not engine.dialect.has_table(engine, "books4"):
    db.execute('CREATE TABLE "books4" ('
               'isbn VARCHAR NOT NULL,'
               'title VARCHAR NOT NULL,'
               'author VARCHAR NOT NULL,'
               'year VARCHAR NOT NULL,'
               'PRIMARY KEY (isbn));')
    db.commit()


def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books4 (isbn, title, author, year) "
                   "VALUES (:isbn, :title, :author, :year)",
                   {"isbn": isbn, "title": title, "author": author, "year": year})
    db.commit()


if __name__ == "__main__":
    main()
