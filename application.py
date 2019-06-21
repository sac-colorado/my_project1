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
    user_name = request.form.get("user_name")
    password = request.form.get("password")
    return render_template("login.html", user_name=user_name, password=password)

@app.route("/register", methods=["GET"])
def register():
    user_name = request.form.get("user_name")
    password = request.form.get("password")
    return render_template("register.html", user_name=user_name, password=password)

@app.route("/output_user_info", methods=["POST"])
def output_user_info():
    book_user = request.form.get("user_name")
    password = request.form.get("password")
    user_data = db.execute("SELECT * FROM book_users WHERE user_name=(:book_user)",{"book_user": book_user}).fetchall()
    if user_data ==[]:
        return render_template("test.html", user_name="Not a registered User", password=password)
    else:
        return render_template("test.html", user_name=user_data[0][1], password=password)
    
