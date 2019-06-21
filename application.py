from flask import Flask, render_template, request

app = Flask(__name__)

# Home page of My_Books_Club -- Register, Sign-in, etc.
"""@app.route("/")
def index():
    return render_template("index.html")"""

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
    user_name = request.form.get("user_name")
    password = request.form.get("password")
    return render_template("test.html", user_name=user_name, password=password)


