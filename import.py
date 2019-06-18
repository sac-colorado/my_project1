import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    my_file = open("books.csv")
    reader = csv.reader(my_file)
    for isbn, title, author, year in reader:
        year =  int(year)           # Convert year string to an integer
        db.execute("INSERT INTO book_info (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Adding book info to Heroku database - isbn: {isbn} title: {title} author: {author} year_published: {year}")
    db.commit()

if __name__ == "__main__":
    main()