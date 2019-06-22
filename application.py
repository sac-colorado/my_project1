from flask import Flask, render_template, request

import os
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# 'engine' is an object that manages connections to the SQL database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Home page of My_Books_Club -- Register, Sign-in, etc.

@app.route("/bookworm", methods=["GET"])
def home_page():
    return render_template("books_home.html")

@app.route("/Sign_in", methods=["GET"])
def goto_login():
    return render_template("login.html")

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

#To register a new user --> need to check the user name is available    
@app.route("/save_user_info", methods=["POST"])
def save_user_info():
    book_user = request.form.get("user_name")
    password = request.form.get("password")
    user_data = db.execute("SELECT * FROM book_users WHERE user_name=(:book_user)",{"book_user": book_user}).fetchall()
    if user_data ==[]:       #New user is not in the database so add them.
        db.execute("INSERT INTO book_users (user_name, password) VALUES (:user_name, :password)", {"user_name": book_user, "password": password})
        db.commit()
        return render_template("test.html", user_name="Thank you, " + book_user + " -- Welcome to The Book Worm!")
    else:             #That user name already exists in the database -- try again.
        return render_template("test.html", user_name="That user name is all ready taken please try to register with a different user_name")


""" @app.route("/output_user_info", methods=["POST"])
def output_user_info():
    book_user = request.form.get("user_name")
    password = request.form.get("password")
    user_data = db.execute("SELECT * FROM book_users WHERE user_name=(:book_user)",{"book_user": book_user}).fetchall()
    if user_data ==[]:
        return render_template("test.html", user_name="Not a registered User", password=password)
    else:
        return render_template("test.html", user_name=user_data[0][1], password=password) """