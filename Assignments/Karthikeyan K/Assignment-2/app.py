# from urllib import request
from flask import Flask, render_template, request
# for ibm
import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32536;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=hhn68702;PWD=JDmq4keRKWs2f0Mi", '', '')
# end of ibm

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/retrive', methods=['POST'])
def retrive():
    if request.method == "POST":
        adduseremail = request.form["email"]
        # adduserpass = request.form["password"]

        addquery = "SELECT * FROM USER WHERE USEREMAIL=?"
        stmt = ibm_db.prepare(conn, addquery)

        ibm_db.bind_param(stmt, 1, adduseremail)
        # ibm_db.bind_param(stmt, 2, adduserpass)

        ibm_db.execute(stmt)

        name = ibm_db.fetch_assoc(stmt)

        if name:
            return render_template('index.html', msg='login sucess')
        else:
            return render_template('signup.html', msg='Please signup')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/add', methods=['POST'])
def add():
    if request.method == "POST":
        adduseremail = request.form["email"]
        adduserpass = request.form["password"]

        addquery = "INSERT INTO USER VALUES(?,?)"
        stmt = ibm_db.prepare(conn, addquery)

        ibm_db.bind_param(stmt, 1, adduseremail)
        ibm_db.bind_param(stmt, 2, adduserpass)

        ibm_db.execute(stmt)

        return render_template('index.html', msg='insert sucess')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
