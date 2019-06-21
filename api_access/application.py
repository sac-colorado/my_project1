from flask import Flask, render_template

import os
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# 'engine' is an object that manages connections to the SQL database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/api/<string:book_isbn>")
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

