from flask import Flask, request, render_template, url_for
import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31498;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=ygs99479;PWD=GOxevDtQbu8EZp0l",'','')

apk = Flask(__name__)

@apk.route('/')
def home():
    return render_template("home.html")

@apk.route('/signin',methods=['POST','GET'])
def signin():
    return render_template("signin.html")

@apk.route('/addsignin',methods=['POST','GET'])
def addsignin():
    if request.method == "POST":
        email = request.form["email"]
        cpass  = request.form["cpass"]
        
        sel_sql = "SELECT * FROM CUSTOMER_CARE WHERE EMAIL_ID =?"
        stmt = ibm_db.prepare(conn,sel_sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)
        fname = ibm_db.result(stmt,'FNAME')

        if acc:
            if(str(cpass)) == str(acc['PASSWORD'].strip()):
                return render_template("home.html",msg="Welcome,",fname = fname)
            else:
                return render_template("signin.html",msg="Invalid E-Mail or Password")

        else:
            return render_template("signup.html",msg="Not a Member First SignUp")

@apk.route('/signup', methods=['POST','GET'])
def signup():
    return render_template("signup.html")

@apk.route('/addsignup', methods=['POST','GET'])
def addsignup():
    if request.method == "POST":
        fname = request.form['fname']
        lname = request.form["lname"]
        email = request.form["email"]
        mnum = request.form["mnum"]
        cpass  = request.form["cpass"]
        ccpass = request.form["ccpass"]

        sel_sql = "SELECT * FROM CUSTOMER_CARE WHERE EMAIL_ID =?"
        stmt = ibm_db.prepare(conn,sel_sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)

        if acc:
            return render_template("signin.html",txt="Your are a Existing User, So Please Sign In")
        
        else:
            ins_sql = "INSERT INTO CUSTOMER_CARE VALUES(?,?,?,?,?,?)"
            pstmt = ibm_db.prepare(conn,ins_sql)
            ibm_db.bind_param(pstmt,1,fname)
            ibm_db.bind_param(pstmt,2,lname)
            ibm_db.bind_param(pstmt,3,email)
            ibm_db.bind_param(pstmt,4,mnum)
            ibm_db.bind_param(pstmt,5,cpass)
            ibm_db.bind_param(pstmt,6,ccpass)

            ibm_db.execute(pstmt)

            return render_template("home.html",msg="Successfully Signed-Up")

apk.run(debug=True)
