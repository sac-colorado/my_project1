# Project 1

My project is a book review website called the "The Book Worm".

This project uses a remote PostGreSQL database that resides on heroku.com. The database houses 3 tables (w/ data columns): "book_info" (id, isbn, title, author, and year) - This table was constucted from the "books.csv" file (provide with the project) and INSERTED via db.execute into the database using a python program named "import.py". The next table is call "book_users" (id, user_name, password) and it holds the user names and encryped passwords for all users who have registered for my site. The final table is called "book_reviews" (id, isbn, reviewer_name, review, rating) and it holds all the book reviews with a 1 - 5 rating that were written and submitted by users of "The Book Worm" website.

When you first come to the website and go to the route "/" you will be taken to my
home page which is rendered from the  file "book_home.html". From the home page there are three links: Sign_in, Register and Sign_out. 

The "Register" link takes you to "register.html" where users enter a user_name and password. The route checks the user_name against all the registered users (stored in the "book_users" database table) and informs the user if thier selected user_name is in use and if they need to come up with another user_name. Once a user successfully  registers then they are taken to the login_in page and asked to login. When they login the route will start a flask session 
