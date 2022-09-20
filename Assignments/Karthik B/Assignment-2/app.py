from flask import Flask , render_template
app = Flask(__name__)

@app.route('/')
def root():
    return render_template("index.html");

@app.route('/signup')
def signup():
    return render_template("Signup.html");

@app.route('/signin')
def signin():
    return render_template("Signin.html");

@app.route('/about')
def about():
    return render_template("Aboutus.html");

app.run(debug=True);