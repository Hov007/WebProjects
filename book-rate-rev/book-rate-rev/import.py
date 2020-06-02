import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://suqhwpwqlslrrd:2c01148507baa7f8d8ae4222bad7e432370d1f7c6891b13248f3620f96f97073@ec2-54-157-78-113.compute-1.amazonaws.com:5432/db29idikr84nuv")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                   {"isbn":isbn, "title":title, "author":author, "year":year})
    db.commit()

if __name__ == "__main__":
    main()


'''        else:
            if isbn and not title and not author:
                data = db.execute("SELECT isbn, title, author FROM books WHERE isbn=:isbn", {"isbn":isbn}).fetchall()
                for i in data:
                    return render_template("search.html", data=data)
'''

