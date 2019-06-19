import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# 'engine' is an object that manages connections to the SQL database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    book_data = db.execute("SELECT isbn, title, author, year FROM book_info").fetchall()

    # fetchall() returns the data as a list
    for book in book_data:
        print(f"{book.isbn} : {book.title} : {book.author} : {book.year}")

if __name__ == "__main__":
    main()
