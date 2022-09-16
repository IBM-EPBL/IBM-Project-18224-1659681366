from distutils.log import debug
from flask import Flask,render_template

app=Flask(__name__)
@app.route("/")
def root():
    return render_template("home.html")
@app.route("/home")
def home():
    return render_template("home.html")
@app.route("/signup")
def signup():
    return render_template("signup.html")
@app.route("/signin")
def signin():
    return render_template("signin.html")
@app.route("/about")
def about():
    return render_template("home.html")
app.run(debug=True)