# Project 1

My project is a book review website called the "The Book Worm".

This project uses a remote PostGreSQL database that resides on heroku.com. The database houses 3 tables (w/ data columns) for project1: "book_info" (id, isbn, title, author, and year) - This table (containing 500 entries) was constucted from the "books.csv" file (provide with the project1) and INSERTED via db.execute into the database using a python program named "import.py". The next table is named "book_users" (id, user_name, password) and it holds the user names and encryped passwords (encryppted using the "passlib.hash" library) for all users who have registered for my site. The final table is named "book_reviews" (id, isbn, reviewer_name, review, rating) and it holds all the book reviews with a 1 - 5 rating that were written and submitted by users of "The Book Worm" website.

When you first come to the website and go to the route "/" you will be taken to my "home page" which is rendered from the  file "book_home.html". From the home page there are three links: Sign_in, Register and Sign_out. 

The "Register" link takes you to "register.html" where users enter a user_name and password. The route checks the user_name against all the registered users (stored in the "book_users" database table) and informs the user if their selected user_name is all ready being used and if they need to come up with another user_name. Once a user successfully registers then they are taken to the login_in page and asked to login. When they login the route will start a "flask session" which holds the user name throughout the time they are signed_in.

After a successful registration/login or login the user is taken to the "search page" where they can search my database (db) table "book_info" by isbn, book title or author to find books they are interested in. After a search of the db the user is next taken to the "search results" page which displays all the books that were found from the search. The list of books found from the search are all "clickable" (linked) which, after you click on a book, then takes you to a "book page" with more information about a single book. The book information also includes the # of reviews and the average rating of the book pulled from the "Goodreads" website. 

From the "book page" the user is given the opportunity to submit a review with a 1 - 5 rating for the particular book that they received information about. The website checks to insure that the user from session["username"] has not submitted a review for the particular book information that they are viewing - "one book review per book per user".

You also have the opportunity to "Sign-out" which "pops" the session["username"] and removes the users ability to use the backspace and make book review submissions, etc.

Finally, I have implemented the route "/api/<isbn #> which uses the "GET" method to allow anyone on the website to search for book information from the "book_info" database. The user must provide the full isbn *. This route "throws" a 404 error if no book with the isbn is found.

Project1 files:

application.py --> my flask/python file that includes all the website "routes"
requirements.txt --> all packages that need to be loaded to successfully run this website
README.md --> THIS FILE.
books.csv --> 5000 entry comma seperated book date. This file is used by import.py to INSERT these 5000 entries into a remote database "housed" on "heroku.com"
import.py --> Python program that reads the books.csv file and INSERTs the book data into a remote database "housed" on "heroku.com"

templates/:
    book_page.html --> rendered after a book search and a resulting book is "clicked on"
    book_search.html --> rendered after a book seach show all results (the results are each "clickable" links)
    books_home.html --> home webpage (links: Sign_in, Register, Sign_out)
    index.html --> the /api/<isbn #> renders this file
    login.html --> rendered when a register user logs in
    output.html --> this file is rendered to supply  user_messages which can contain errors or other user information.
    register.html --> rendered when a new user registers on the webpage
    submit_review.html --> rendered when submitting a book review
static/:
    my_books.scss --> sass configuration file that generates the books.css file
    my_books.css --> Style sheet for the entire website.




