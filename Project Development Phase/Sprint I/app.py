from flask import Flask, render_template, request

# for otp
import sendgrid
import os
from sendgrid.helpers.mail import *
import random

# for ibm
import ibm_db
conn = ibm_db.connect(
    "DATABASE=bludb; HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud; PORT= 32459; SECURITY =SSL;UID=rmf92833; PWD=klHw5XHWgYzks5ql;", '', '')

# for ibm
# import ibm_db
# conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32536;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=hhn68702;PWD=JDmq4keRKWs2f0Mi", '', '')
# end of ibm

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/loginuser')
def loginuser():
    return render_template('login_user.html')

@app.route('/addloginuser', methods=['POST', 'GET'])
def addloginuser():
    if request.method == "POST":
        email = request.form["login_user_email"]
        cpass = request.form["login_user_password"]

        sel_sql = "SELECT * FROM CUSTOMER WHERE EMAIL=?"
        stmt = ibm_db.prepare(conn, sel_sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)
        fname = ibm_db.result(stmt, 'FULL_NAME')

        if acc:
            if (str(cpass)) == str(acc['PASSWORD'].strip()):
                return render_template("dashboard.html", msg="Welcome,", fname=fname)
            else:
                return render_template("login_user.html", msg="Invalid E-Mail or Password")

        else:
            return render_template("signup_user.html", msg="Not a Member First SignUp")



@app.route('/loginadmin')
def loginadmin():
    return render_template('login_admin.html')

@app.route('/addloginadmin', methods=['POST', 'GET'])
def addloginadmin():
    if request.method == "POST":
        email = request.form["login_admin_email"]
        cpass = request.form["login_admin_password"]

        sel_sql = "SELECT * FROM ADMIN WHERE EMAIL=?"
        stmt = ibm_db.prepare(conn, sel_sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)
        fname = ibm_db.result(stmt, 'FULL_NAME')

        if acc:
            if (str(cpass)) == str(acc['PASSWORD'].strip()):
                return render_template("dashboard.html", msg="Welcome,", fname=fname)
            else:
                return render_template("login_admin.html", msg="Invalid E-Mail or Password")

        else:
            return render_template("signup_admin.html", msg="Not a Member First SignUp")



@app.route('/signupuser')
def signupuser():
    return render_template('signup_user.html')

# Getting the data from the user


@app.route('/addsignupuser', methods=['POST', 'GET'])
def addsignupuser():
    if request.method == "POST":
        global full_name, cemail, phone_number, password, re_password
        full_name = request.form['signup_user_username']
        cemail = request.form["signup_user_email"]
        phone_number = request.form["signup_user_phone_number"]
        password = request.form["signup_user_password"]
        re_password = request.form["signup_user_re_password"]

        sel_sql = "SELECT * FROM CUSTOMER WHERE EMAIL=?"
        stmt = ibm_db.prepare(conn, sel_sql)
        ibm_db.bind_param(stmt, 1, cemail)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)

        # Checking the Account existing user or not
        if acc:
            return render_template("login_user.html", txt="Your are a Existing User so LogIn")
        else:
            # Genertting the OTP
            global rand
            rand = random.randint(10000, 99999)
            from_email = Email("2k19cse038@kiot.ac.in",
                               "CUSTOMER CARE REGISTRY")
            to_email = To(cemail)
            subject = "Verification( USER )"
            content = Content(
                "text/plain", "The verification code is :"+str(rand))
            mail = Mail(from_email, to_email, subject, content)
            sg = sendgrid.SendGridAPIClient('YOUR API KEY')
            response = sg.client.mail.send.post(request_body=mail.get())

    return render_template('otp_user_verify.html', cemail=cemail, full_name=full_name, phone_number=phone_number, password=password, re_password=re_password)


@app.route('/userverify', methods=['POST', 'GET'])
def userverify():
    if request.method == "POST":
        aotp = request.form["user_entered_otp"]

        # If otp Correct data will store in db
        if (str(aotp) == str(rand)):
            ins_sql = "INSERT INTO CUSTOMER VALUES(?,?,?,?,?)"
            pstmt = ibm_db.prepare(conn, ins_sql)
            ibm_db.bind_param(pstmt, 1, full_name)
            ibm_db.bind_param(pstmt, 2, cemail)
            ibm_db.bind_param(pstmt, 3, phone_number)
            ibm_db.bind_param(pstmt, 4, password)
            ibm_db.bind_param(pstmt, 5, re_password)

            ibm_db.execute(pstmt)
            return render_template("login_user.html", msg="Welcome", full_name=full_name)

        else:
            return render_template("otp_user_verify.html", otpmsg="Otp is Incorrect", cemail=cemail, full_name=full_name, phone_number=phone_number, password=password, re_password=re_password)


@app.route('/signupadmin')
def signupadmin():
    return render_template('signup_admin.html')

@app.route('/addsignupadmin', methods=['POST', 'GET'])
def addsignupadmin():
    if request.method == "POST":
        global admin_full_name, aemail, admin_phone_number, organization_name, organization_emp, organization_address, passwords, re_passwords
        admin_full_name = request.form['signup_admin_username']
        aemail = request.form["signup_admin_email"]
        admin_phone_number = request.form["signup_admin_phone_number"]
        organization_name = request.form["signup_admin_organization_name"]
        organization_emp = request.form["signup_admin_organization_employee"]
        organization_address = request.form["signup_admin_organization_address"]
        passwords = request.form["signup_admin_password"]
        re_passwords = request.form["signup_admin_re_password"]

        sel_sql = "SELECT * FROM ADMIN WHERE EMAIL=?"
        stmt = ibm_db.prepare(conn, sel_sql)
        ibm_db.bind_param(stmt, 1, aemail)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)

        # Checking the Account existing user or not
        if acc:
            return render_template("login_admin.html", txt="Your are a Existing User so LogIn")
        else:
            # Genertting the OTP
            global rands
            rands = random.randint(10000, 99999)
            from_email = Email("2k19cse038@kiot.ac.in",
                               "CUSTOMER CARE REGISTRY")
            to_email = To(aemail)
            subject = "Verification( ADMIN )"
            content = Content("text/plain", "The verification code is : "+str(rands))
            mail = Mail(from_email, to_email, subject, content)
            sg = sendgrid.SendGridAPIClient('YOUR API KEY')
            response = sg.client.mail.send.post(request_body=mail.get())

    return render_template('otp_admin_verify.html', aemail=aemail, admin_full_name=admin_full_name, admin_phone_number=admin_phone_number, organization_name=organization_name, organization_emp=organization_emp, organization_address=organization_address, passwords=passwords, re_passwords=re_passwords)

# Verify the otp for admin and adding the data in db


@app.route('/adminverify', methods=['POST', 'GET'])
def adminverify():
    if request.method == "POST":
        aotp = request.form["user_entered_otp"]

        # If otp Correct data will store in db
        if (str(aotp) == str(rands)):
            ins_sql = "INSERT INTO ADMIN VALUES(?,?,?,?,?,?,?,?)"
            pstmt = ibm_db.prepare(conn, ins_sql)
            ibm_db.bind_param(pstmt, 1, admin_full_name)
            ibm_db.bind_param(pstmt, 2, aemail)
            ibm_db.bind_param(pstmt, 3, admin_phone_number)
            ibm_db.bind_param(pstmt, 4, organization_name)
            ibm_db.bind_param(pstmt, 5, organization_emp)
            ibm_db.bind_param(pstmt, 6, organization_address)
            ibm_db.bind_param(pstmt, 7, passwords)
            ibm_db.bind_param(pstmt, 8, re_passwords)

            ibm_db.execute(pstmt)
            return render_template("login_admin.html", msg="Welcome", admin_full_name=admin_full_name)

        else:
            return render_template("otp_admin_verify.html", otpmsg="Otp is Incorrect",aemail=aemail, admin_full_name=admin_full_name, admin_phone_number=admin_phone_number, organization_name=organization_name, organization_emp=organization_emp, organization_address=organization_address, passwords=passwords, re_passwords=re_passwords)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
