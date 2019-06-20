from flask import Flask, render_template

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# 'engine' is an object that manages connections to the SQL database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/api/<string:book_isbn>")
def index(book_isbn):
    book_data = db.execute("SELECT isbn, title, author, year FROM book_info WHERE isbn=(:book_isbn)",{"book_isbn": book_isbn}).fetchall()      
    empty_list = []
    empty = False
    if book_data == empty_list:
        empty = True
        #book_data = [False, False, False, False]
        return render_template("index.html", book_data=book_data, query_empty=empty)
    else:
        return render_template("index.html", book_data=book_data, query_empty=empty)
