"""
Example of call to a database, but for now, no database to create_engine doesn't work

"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# if working on a database on the internet, DATABASE_URL would be an url
engine = create_engine(os.getenv("DATABASE_URL"))
# to create different sessions for different users:
db = scoped_session(sessionmaker(bind=engine))


def main():
    # possible to insert SQL in db.execute. .fetchall() = get me all of the results
    flights = db.execute("SELECT origin, destination, duration FROM flights").fetchall()
    for flight in flights:
        print(f'{flight.origin} to {flight.destination}, {flight.duration} minutes.')


if __name__ == "__main__":
    main()
