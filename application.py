from flask import Flask, render_template, request, redirect, url_for, escape, session
from flask_session import Session

import os
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from passlib.hash import sha256_crypt



app = Flask(__name__)

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

@app.route('/sign_out')
def sign_out():
    session.pop('username', None)
    return redirect('/')

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

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

#To Sign-in a user --> need to check that the user name and encryped password match the database   
@app.route("/user_login", methods=["POST"])
def user_login():
    if request.method == 'POST':
        app.secret_key = 'My super secret key'
        session['username'] = request.form['user_name']

    book_user = request.form.get("user_name")
    password = request.form.get("password")
    user_data = db.execute("SELECT * FROM book_users WHERE user_name=(:book_user)",{"book_user": book_user}).fetchall()
    if (user_data != [] and sha256_crypt.verify(request.form.get("password"), user_data[0][2])):      
        return render_template("book_search.html", user_name=book_user)
    else:       #That user name already exists in the database -- try again.
        return render_template("output.html", user_message="Not a valid user_name or password --please try again", sign_in = False )

# A route that makes a GET request to the website and returns a JSON respone containing book 
 # information.                   
@app.route("/book_search", methods=["POST"])
def book_search():
    find_book =request.form.get("find_book")
    find_book = "%" + find_book + "%"
    book_data = db.execute("SELECT * FROM book_info WHERE isbn ILIKE (:find_book) OR title ILIKE (:find_book) OR author ILIKE (:find_book) ORDER BY title",{"find_book": find_book}).fetchall()
    #book_data = db.execute("SELECT isbn, title, author FROM book_info WHERE isbn=(:book_isbn)", {"book_isbn": find_book}).fetchall()
    if book_data == []: #Check if the query found a result or not in your database
        return render_template("output.html", user_message="Check your spelling and try again or the book isn't in the database")
    else:
        return render_template("output.html", book_data=book_data, book_search=True)

 # A route that makes a GET request to the website and returns a JSON respone containing book 
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


