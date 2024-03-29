from flask import Flask, render_template, request, redirect, url_for, escape, session
from flask_session import Session

import os
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from passlib.hash import sha256_crypt


app = Flask(__name__)
app.secret_key = "Secret Key"

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# 'engine' is an object that manages connections to the SQL database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# Home page of My_Books_Club -- Register, Sign-in, etc.
@app.route("/", methods=["GET"])
def home_page():
    return render_template("books_home.html")

@app.route("/Sign_in", methods=["GET"])
def goto_login():
    return render_template("login.html")

@app.route("/Sign_out")
def sign_out():
    session.pop("username", None)
    return redirect('/')

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

#To Sign-in a user --> need to check that the user name and encryped password match the database   
@app.route("/user_login", methods=["POST"])
def user_login():
    book_user = request.form.get("user_name")
    password = request.form.get("password")
    user_data = db.execute("SELECT * FROM book_users WHERE user_name=(:book_user)",{"book_user": book_user}).fetchall()
    if (user_data != [] and sha256_crypt.verify(request.form.get("password"), user_data[0][2])): 
        session["username"] = book_user
        return render_template("book_search.html", user_name=book_user)
    else:       #That user name already exists in the database -- try again.
        return render_template("output.html", user_message="Not a valid user_name or password --please try again", sign_in = False )

#To register a new user --> need to check that the user name is available a--> then save
# the login and hashed password to the database   
@app.route("/save_user_info", methods=["POST"])
def save_user_info():
    book_user = request.form.get("user_name")
    encryped_password = sha256_crypt.encrypt(request.form.get("password")) # Encrypt the password
    user_data = db.execute("SELECT user_name FROM book_users WHERE user_name=(:book_user)",{"book_user": book_user}).fetchall()
    if user_data == []:       #New user is not in the database so add them.
        db.execute("INSERT INTO book_users (user_name, password) VALUES (:user_name, :password)", {"user_name": book_user, "password": encryped_password})
        db.commit()
        return render_template("output.html", user_message="Thank you, " + book_user + " -- Welcome to The Book Worm! You're now registered. \n Please sign-in!", registration = True)
    else:             #That user name already exists in the database -- try again.
        return render_template("output.html", user_message="That user name is all ready taken please try to register with a different user_name", registration = False)

# A route that makes a GET request to the website and returns a JSON respone containing book 
 # information.                   
@app.route("/Book_search", methods=["GET", "POST"])
def book_search():
    if "username" in session:
        gobacktosearch = False
        gobacktosignin = False
        book_search = False
        find_book =request.form.get("find_book")
        find_book = "%" + find_book + "%"      # add "wildcard characters" % to your query
        book_data = db.execute("SELECT * FROM book_info WHERE isbn ILIKE (:find_book) OR title ILIKE (:find_book) OR author ILIKE (:find_book) ORDER BY title",{"find_book": find_book}).fetchall()
        if book_data == []: #Check if the query found a result or not in your database
            return render_template("output.html", user_message="Check your spelling and try again or the book isn't in the database", gobacktosearch = True)
        else:
            return render_template("output.html", book_data=book_data, user_message="Here are Your Search Results sorted by Book Title", book_search = True)
    else:
        return render_template("output.html", user_message="You have been signed out and need to login again", gobacktosignin=True)

# If you book search failed then send user a message and give them a path ("try again") botton to return
# to return to the book_search page.
@app.route("/go_back_to_search", methods=["GET"])
def go_back_to_search():
    return render_template("book_search.html")

# A route that makes a GET request to the website and returns a JSON response containing book 
 # information.                   
@app.route("/book_page/<string:book_isbn>", methods=["GET"])
def book_page(book_isbn):
    book_data = db.execute("SELECT isbn, title, author, year FROM book_info WHERE isbn=(:book_isbn)",{"book_isbn": book_isbn}).fetchall()      
    empty = False
    reviews = False
    if book_data == []: #Check if the query found a result or not in your database
        empty = True
        return render_template("book_page.html", book_data=book_data, query_empty=empty, review_isbn=book_isbn)
    else:
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "1v1ZUGkCBeNqhLjfcFeaA", "isbns": book_isbn})
        reviews_count = res.json()['books'][0]['work_ratings_count']
        average_rating = res.json()['books'][0]['average_rating']
        book_reviews =db.execute("SELECT review, rating FROM book_reviews WHERE isbn=(:book_isbn)", {"book_isbn": book_isbn}).fetchall()
        return render_template("book_page.html", book_data=book_data, query_empty=empty, average_rating=average_rating, reviews_count=reviews_count, book_reviews=book_reviews)

@app.route("/Write_review/<string:book_isbn>", methods=["GET"])
def write_review(book_isbn):
    book_data = db.execute("SELECT isbn, reviewer_name FROM book_reviews WHERE isbn=(:book_isbn)",{"book_isbn": book_isbn}).fetchall()
    get_book_info = db.execute("SELECT isbn, title, author FROM book_info WHERE isbn=(:book_isbn)",{"book_isbn": book_isbn}).fetchall()
    for book_info in get_book_info:
        book_title = book_info.title     # Get title of book to pass to submit_review.html to use in forms name
        book_author = book_info.author
    for review in book_data:
         if session["username"] == review.reviewer_name:
            return render_template("output.html", user_message="You have already submitted a review for this book -- only one review per user")
    return render_template("submit_review.html", book_isbn=book_isbn, book_title=book_title, book_author=book_author)

@app.route("/Submit_review", methods=["POST"])
def submit_review():
    book_review = request.form.get("book_review")
    book_isbn = request.form.get("book_isbn")
    review_rating = request.form.get("book_rating")
    reviewer_name = session["username"] 
    # Check again to make sure the user hasn't already submitted a review for the book. This keeps
    # a user from using the "back arrow" to go back and re-submit their review
    book_data = db.execute("SELECT isbn, reviewer_name FROM book_reviews WHERE isbn=(:book_isbn)",{"book_isbn": book_isbn}).fetchall()
    for review in book_data:
        if session["username"] == review.reviewer_name:
            return render_template("output.html", user_message="You have already submitted a review for this book -- only one review per user")
    #db.execute("INSERT INTO test_table (review) VALUES (:review)", {"review": book_review})
    if (review_rating == "1" or review_rating == "2" or review_rating == "3" or review_rating == "4" or review_rating == "5"):
        review_rating = int(review_rating)
        db.execute("INSERT INTO book_reviews (isbn, reviewer_name, review, rating) VALUES (:isbn, :reviewer_name, :review, :rating)", {"isbn": book_isbn, "reviewer_name": reviewer_name, "review": book_review, "rating": review_rating})
        db.commit()
        return render_template("book_search.html")
    else: 
        db.execute("INSERT INTO book_reviews (isbn, reviewer_name, review) VALUES (:isbn, :reviewer_name, :review)", {"isbn": book_isbn, "reviewer_name": reviewer_name, "review": book_review})
        db.commit()
        return render_template("book_search.html")
            
# A route that makes a GET request to the website and returns a JSON response containing book 
 # information.                   
@app.route("/api/<string:book_isbn>", methods=["GET"])
def index(book_isbn):
    book_data = db.execute("SELECT isbn, title, author, year FROM book_info WHERE isbn=(:book_isbn)",{"book_isbn": book_isbn}).fetchall()      
    empty = False
    if book_data == []: #Check if the query found a result or not in your database
        empty = True
        return render_template("index.html", book_data=book_data, query_empty=empty)
    else:
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "1v1ZUGkCBeNqhLjfcFeaA", "isbns": book_isbn})
        reviews_count = res.json()['books'][0]['work_ratings_count']
        average_rating = res.json()['books'][0]['average_rating']
        return render_template("index.html", book_data=book_data, query_empty=empty, average_rating=average_rating, reviews_count=reviews_count)
