import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():

    # List book with a particular isbn
    book_review = db.execute("SELECT id, isbn, title, author, year FROM book_info WHERE isbn='0142002038'").fetchall()
    for book in book_review:        
        print(f"{book.id} isbn: {book.isbn} title: {book.title} author: {book.author}, year: {book.year}")

    # Prompt user to choose a flight. You will want to make the input an integer
    choose_book = int(input("\nchoose book number: "))
    get_book = db.execute("SELECT review FROM book_reviews WHERE isbn = ":isbn", {"id": choose_book}).fetchone()

    # Make sure flight is valid.
    """ if flight is None:
        print("Error: No such flight.")
        return
    
    passengers = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",
                            {"flight_id": flight_id}).fetchall()
    print("\nPassengers:")
    for passenger in passengers:
        print(passenger.name)
    if len(passengers) == 0:
        print("No passengers.") """

if __name__ == "__main__":
    main()
