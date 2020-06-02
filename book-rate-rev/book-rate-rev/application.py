import os

from flask import Flask, session, flash, redirect, render_template, request, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
import requests
from sys import exit

app = Flask(__name__)

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://suqhwpwqlslrrd:2c01148507baa7f8d8ae4222bad7e432370d1f7c6891b13248f3620f96f97073@ec2-54-157-78-113.compute-1.amazonaws.com:5432/db29idikr84nuv")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        password = request.form.get("password")
        username = request.form.get("username")

        # Ensure username was submitted
        if not username:
            return render_template("error.html", message="You must provide a 'Username'!")

        # Ensure password was submitted
        elif not password:
            return render_template("error.html", message="You must provide a 'Password'!")


        # Ensure password and confirmation match
        elif not password == request.form.get("confirmation"):
            return render_template("error.html", message="Password do not match!")

        # Checking if username already exists or not
        names_db = db.execute("SELECT username FROM users WHERE username = :username",
                              {"username": username}).fetchone()
        if names_db != None:
            return render_template("error.html", message="Username taken")

        # hash the password and insert a new user in the database
        hash = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash);",
                                 {"username":username, "hash":hash})
        db.commit()

        # Redirect user to home page
        return redirect(url_for("index"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    if request.method == "POST":
        password = request.form.get("password")
        username = request.form.get("username")
        user = db.execute("SELECT username FROM users").fetchall()

        # Ensure username/password was submitted
        if not request.form.get("username"):
            return render_template("error.html", message="You must provide a 'Username'!")

        elif not request.form.get("password"):
            return render_template("error.html", message="You must provide a password!")
        # Ensure username exists
        else:
            ls = []
            for i in user:
                for j in i:
                    ls.append(j)
            if username not in ls:
                return render_template("error.html", message="Invalid username!")


        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username=:username", {"username":username}).fetchone()

        # Ensure username exists and password is correct
        if not check_password_hash(rows["hash"], password) or not rows[1] == username:
            return render_template("error.html", message="Invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]
        # Redirect user to home page
        return redirect(url_for("home"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return render_template("index.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
            return render_template("search.html")
    else:
        return render_template("home.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        # Taking users input and searching in db
        isbn = "%" + request.form.get("isbn") + "%"
        title = "%" + request.form.get("title") + "%"
        author = "%" + request.form.get("author") + "%"

        data = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn AND LOWER(title) LIKE LOWER(:title) AND LOWER(author) LIKE LOWER(:author)",
                            {"isbn": isbn, "title": title, "author": author}).fetchall()
        return render_template("search.html", data=data)

@app.route("/review/<int:book_id>", methods=["GET", "POST"])
def review(book_id):
    if request.method == "GET":
        # Checking if user already has review and rating for particular book
        user_id = session["user_id"]
        rt = db.execute("SELECT rating FROM review WHERE user_id=:user_id AND book_id=:book_id",
                        {"user_id":session["user_id"], "book_id":book_id}).fetchall()



        # Selecting title and author to show on review.html
        book = db.execute("SELECT title, author FROM books WHERE book_id = :book_id",
                          {"book_id": book_id}).fetchall()

        # Using isbn and API to show results from GoodReads
        isbn = db.execute("SELECT isbn FROM books WHERE book_id = :book_id",
                          {"book_id": book_id}).fetchall()
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                           params={"key": "CrzCLjarMcy4Wh3dOFiKQ", "isbns": isbn})
        # print(res.json())
        data = res.json()
        ratings_count = data["books"][0]["work_ratings_count"]
        average_rating = data["books"][0]["average_rating"]

        # Selecting users rating and review
        rate = db.execute("SELECT rating, user_review FROM review WHERE user_id=:user_id AND book_id=:book_id",
                          {"user_id":user_id, "book_id":book_id}).fetchall()
        print(rate)
        return render_template("review.html", book=book, rt=rt, ratings_count=ratings_count, average_rating=average_rating, rate=rate)

    elif request.method == "POST":
        user_id = session["user_id"]

        # Selecting title and author to show on review.html
        book = db.execute("SELECT title, author FROM books WHERE book_id = :book_id",
                          {"book_id": book_id}).fetchall()

        # Using isbn and API to show results from GoodReads
        isbn = db.execute("SELECT isbn FROM books WHERE book_id = :book_id",
                          {"book_id": book_id}).fetchall()
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                           params={"key": "CrzCLjarMcy4Wh3dOFiKQ", "isbns": isbn})
        # print(res.json())
        data = res.json()
        ratings_count = data["books"][0]["work_ratings_count"]
        average_rating = data["books"][0]["average_rating"]

        # User has to fill all fields
        rating = request.form.get("star")
        user_review = request.form.get("review")
        if not rating or not user_review:
            return render_template("error.html", message="Rating or/and Review is missing!")

        # Inserting rating and review into DB
        db.execute("INSERT INTO review (user_id, book_id, rating, user_review) VALUES (:user_id, :book_id, :rating, :user_review)",
        {"user_id": user_id, "book_id": book_id, "rating": rating, "user_review": user_review})
        db.commit()
        rt = db.execute("SELECT rating FROM review WHERE user_id=:user_id AND book_id=:book_id",
                        {"user_id": session["user_id"], "book_id": book_id}).fetchall()
        rate = db.execute("SELECT rating, user_review FROM review WHERE user_id=:user_id AND book_id=:book_id",
                          {"user_id": user_id, "book_id": book_id}).fetchall()
        print(rate)
        return render_template("review.html", book=book, rt=rt, rate=rate, ratings_count=ratings_count, average_rating=average_rating)


@app.route("/api/<isbn>")
def book_api(isbn):
    '''Return details about a single book'''

    # Make shure book exist
    # check = db.execute("SELECT book_id FROM books WHERE isbn=:isbn",
                       # {"isbn":isbn}).fetchall()
    # print(check[0][0])

        # exit(404)
    book = db.execute("SELECT book_id, title, author, year, isbn FROM books WHERE isbn=:isbn",
                      {"isbn":isbn}).fetchall()
    if book == []:
        return jsonify({"error": "Invalid isbn"}), 404
    book_info = []
    for b in book:
        book_info.append(b)
    # if book_info[0][0] is None:


    # Getting ratings for single book
    book_id = book_info[0][0]
    count = db.execute("SELECT rating from review WHERE book_id=:book_id",
                              {"book_id":book_id})
    review_count = []
    for r in count:
        review_count.append(r)

    # Counting average of ratings
    sum_ = 0
    for i in review_count:
        for j in i:
            j = int(j)
            sum_ += j
    average_score = sum_ / len(review_count)

    return jsonify({
        "title": book_info[0][1],
        "auhtor": book_info[0][2],
        "year": book_info[0][3],
        "isbn": isbn,
        "review_count": len(review_count),
        "average_score": average_score
    })
