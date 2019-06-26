# Project 1

My project is a book review website called the "The Book Worm".

This project uses a remote PostGreSQL database that resides on heroku.com. The database houses 3 tables (w/ data columns) for project1: "book_info" (id, isbn, title, author, and year) - This table (containing 500 entries) was constucted from the "books.csv" file (provide with the project1) and INSERTED via db.execute into the database using a python program named "import.py". The next table is named "book_users" (id, user_name, password) and it holds the user names and encryped passwords (encryppted using the "passlib.hash" library) for all users who have registered for my site. The final table is named "book_reviews" (id, isbn, reviewer_name, review, rating) and it holds all the book reviews with a 1 - 5 rating that were written and submitted by users of "The Book Worm" website.

When you first come to the website and go to the route "/" you will be taken to my "home page" which is rendered from the  file "book_home.html". From the home page there are three links: Sign_in, Register and Sign_out. 

The "Register" link takes you to "register.html" where users enter a user_name and password. The route checks the user_name against all the registered users (stored in the "book_users" database table) and informs the user if their selected user_name is all ready being used and if they need to come up with another user_name. Once a user successfully registers then they are taken to the login_in page and asked to login. When they login the route will start a "flask session" which holds the user name throughout the time they are signed_in.

After a successful registration/login or login the user is taken to the "search page" where they can search my database (db) table "book_info" by isbn, book title or author to find books they are interested in. After a search of the db the user is next taken to the "search results" page which displays all the books that were found from the search. The list of books found from the search are all "clickable" (linked) which, after you click on a book, then takes you to a "book page" with more information about a single book. The book information also includes the # of reviews and the average rating of the book pulled from the "Goodreads" website. 

From the "book page" the user is given the opportunity to submit a review with a 1 - 5 rating for the particular book that they received information about. The website checks to insure that the user from session["username"] has not submitted a review for the particular book information that they are viewing - "one book review per user"

