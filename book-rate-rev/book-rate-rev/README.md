# Project 1

Web Programming with Python and JavaScript

# application.py
In application.py is stored all backend data of the website, all routes with their structure, 
begins with index wich routes you to login and registration page.After registration you can login wich will save your data in database
users table, with your yousername and hashed password, and in login part i used session["user_id"] to remember the logined user.

@app.route("/search", methods=["GET", "POST"]) 
This route takes you to search.html where you can search the book with isbn, title or author, after typing you click search code 
goes and search your input in books table, if there is no book it will redirect you to error.html, if there is book in db
will brings you a table with book info, and if you click it will take you to review.html.

@app.route("/review/<int:book_id>", methods=["GET", "POST"])
this will show you title and author, and also information from goodreads, wich I set with their API,

if you don't have any review and rating for the book it will let you to rate and write some review and submit, after submitting it will store your review in
review table in db. you can give rating and review only one time for particular book.

@app.route("/api/<isbn>")
this route will show you json info for book with given isbn, if there is no isbn in db, it will show you 404 error

# templates
This folder keeps all html files that the webapplicaton needs.
error.html - that will show you what is wrong
index.html - shows login and registration
home.html - shows you the homepage where you can search a book
search.html - shows you your result for a book
review.html - shows you info for book, and if request is post it will let you give a rating and review, 
              if request is get will show your rating and review

# static
This folder contains all css files for all html files              