from flask import Flask, render_template, request, session, redirect
from flask_session import Session
import time

#-------------------- FOR SENDGRID AND OTP ----------------- 
import sendgrid
import os
from sendgrid.helpers.mail import *
import random



#------------------------ FOR IBM DB ------------------------
import ibm_db
conn = ibm_db.connect("DATABASE=bludb; HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud; PORT=32536; SECURITY=SSL;UID=hhn68702;PWD=JDmq4keRKWs2f0Mi", '', '')




app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



#------------------------  LANDING PAGE   -----------------------

@app.route('/')
def home():
    # session["login_type"] = None
    logintype = session.get("login_type")
    loginemail = session.get("login_email")

    if (logintype==None or loginemail==None) :
        return render_template('index.html',logintype="none",loginemail="none")
    else:
        return render_template('index.html',logintype=logintype,loginemail=loginemail)







#------------------------  LOGIN USER   -----------------------

@app.route('/loginuser')
def loginuser():
    logintype = session.get("login_type")

    if (logintype==None) :
        return render_template('login_user.html',logintype="none")
    else:
        return render_template('login_user.html',logintype=logintype)

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

        if acc:
            if (str(cpass)) == str(acc['PASSWORD'].strip()):
                session["login_type"] = "user"
                session["login_email"] = ""+str(email)
                return redirect("/dashboarduser")
            else:
                return render_template("login_user.html", msg="Invalid E-Mail or Password",user_email=email)

        else:
            return render_template("signup_user.html", msg="Not a Member First SignUp")








#------------------------  LOGIN ADMIN   -----------------------

@app.route('/loginadmin')
def loginadmin():
    logintype = session.get("login_type")

    if (logintype==None) :
        return render_template('login_admin.html',logintype="none")
    else:
        return render_template('login_admin.html',logintype=logintype)

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

        if acc:
            if (str(cpass)) == str(acc['PASSWORD'].strip()):
                session["login_type"] = "admin"
                session["login_email"] = ""+str(email)
                return redirect("/dashboardadmin")
            else:
                return render_template("login_admin.html", msg="Invalid E-Mail or Password")

        else:
            return render_template("signup_admin.html", msg="Not a Member First SignUp")








#------------------------  LOGIN AGENT   -----------------------

@app.route('/loginagent')
def loginagent():
    logintype = session.get("login_type")

    if (logintype==None) :
        return render_template('login_agent.html',logintype="none")
    else:
        return render_template('login_agent.html',logintype=logintype)

@app.route('/addloginagent', methods=['POST', 'GET'])
def addloginagent():
    if request.method == "POST":
        email = request.form["login_admin_email"]
        cpass = request.form["login_admin_password"]

        sel_sql = "SELECT * FROM AGENT WHERE EMAIL=?"
        stmt = ibm_db.prepare(conn, sel_sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)

        if acc:
            if (str(cpass)) == str(acc['PASSWORD'].strip()):
                session["login_type"] = "agent"
                session["login_email"] = ""+str(email)
                return redirect("/dashboardagent")
            else:
                return render_template("login_agent.html", msg="Invalid E-Mail or Password")

        else:
            return render_template("login_agent.html", msg="Not a Member please contact your admin for invite")







#------------------------  SIGNUP USER   -----------------------

@app.route('/signupuser')
def signupuser():
    logintype = session.get("login_type")

    if (logintype==None) :
        return render_template('signup_user.html',logintype="none")
    else:
        return render_template('signup_user.html',logintype=logintype)

@app.route('/addsignupuser', methods=['POST', 'GET'])
def addsignupuser():

    if request.method == "POST":
        global user_fullname, user_email, user_phonenumber, user_password
        user_fullname = request.form["signup_user_username"]
        user_email = request.form["signup_user_email"]
        user_phonenumber = str(request.form["signup_user_phone_number"])
        user_password = request.form["signup_user_password"]

        sel_sql = "SELECT * FROM CUSTOMER WHERE EMAIL=?"
        stmt = ibm_db.prepare(conn, sel_sql)
        ibm_db.bind_param(stmt, 1, user_email)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)

        # Checking the Account existing user or not
        if acc:
            return render_template("login_user.html", msg="Your are already our customer,Please Login!", user_email=user_email)
        else:
            global user_rand
            user_rand = random.randint(10000, 99999)
            from_email = Email("2k19cse038@kiot.ac.in","CUSTOMER CARE REGISTRY")
            to_email = To(user_email)
            subject = "Verification( USER )"
            content = Content("text/plain", "Hi "+user_fullname+" , This is your verification code : "+str(user_rand))
            mail = Mail(from_email, to_email, subject, content)
            sg = sendgrid.SendGridAPIClient('KEY')
            response = sg.client.mail.send.post(request_body=mail.get())

    return render_template('otp_user_verify.html',otpmsg="OTP SENT SUCCESSFULLY !", user_fullname=user_fullname, user_email=user_email, user_phonenumber=user_phonenumber, user_password=user_password)

@app.route('/userverify', methods=['POST', 'GET'])
def userverify():
    if request.method == "POST":
        user_otp = request.form["user_entered_otp"]

        if (str(user_otp) == str(user_rand)):
            ins_sql = "INSERT INTO CUSTOMER VALUES(?,?,?,?)"
            pstmt = ibm_db.prepare(conn, ins_sql)
            ibm_db.bind_param(pstmt, 1, user_fullname)
            ibm_db.bind_param(pstmt, 2, user_email)
            ibm_db.bind_param(pstmt, 3, user_phonenumber)
            ibm_db.bind_param(pstmt, 4, user_password)
            ibm_db.execute(pstmt)
            return render_template("login_user.html", msg="Signup Success! Please Login to enjoy your stay!", user_email=user_email)
        else:
            return render_template("otp_user_verify.html", otpmsg="INCORRECT OTP !", user_fullname=user_fullname, user_email=user_email, user_phonenumber=user_phonenumber, user_password=user_password)







#------------------------  SIGNUP ADMIN   -----------------------

@app.route('/signupadmin')
def signupadmin():
    logintype = session.get("login_type")

    if (logintype==None) :
        return render_template('signup_admin.html',logintype="none")
    else:
        return render_template('signup_admin.html',logintype=logintype)

@app.route('/addsignupadmin', methods=['POST', 'GET'])
def addsignupadmin():
    if request.method == "POST":
        global admin_fullname, admin_email, admin_phonenumber, admin_organization_name, admin_organization_emp, admin_organization_address, admin_password
        admin_fullname = request.form['signup_admin_username']
        admin_email = request.form["signup_admin_email"]
        admin_phonenumber = str(request.form["signup_admin_phone_number"])
        admin_organization_name = request.form["signup_admin_organization_name"]
        admin_organization_emp = str(request.form["signup_admin_organization_employee"])
        admin_organization_address = request.form["signup_admin_organization_address"]
        admin_password = request.form["signup_admin_password"]

        sel_sql = "SELECT * FROM ADMIN WHERE EMAIL=?"
        stmt = ibm_db.prepare(conn, sel_sql)
        ibm_db.bind_param(stmt, 1, admin_email)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)

        if acc:
            return render_template("login_admin.html",msg="Your are already our customer,Please Login!", admin_email=admin_email)
        else:
            global admin_rand
            admin_rand = random.randint(10000, 99999)
            from_email = Email("2k19cse038@kiot.ac.in","CUSTOMER CARE REGISTRY")
            to_email = To(admin_email)
            subject = "Verification( ADMIN )"
            content = Content("text/plain", "Hi "+admin_fullname+" , This is your verification code : "+str(admin_rand))
            mail = Mail(from_email, to_email, subject, content)
            sg = sendgrid.SendGridAPIClient('KEY')
            response = sg.client.mail.send.post(request_body=mail.get())

    return render_template('otp_admin_verify.html',otpmsg="OTP SENT SUCCESSFULLY !", admin_fullname=admin_fullname, admin_email=admin_email, admin_phonenumber=admin_phonenumber, admin_organization_name=admin_organization_name, admin_organization_emp=admin_organization_emp, admin_organization_address=admin_organization_address, admin_password=admin_password)

@app.route('/adminverify', methods=['POST', 'GET'])
def adminverify():
    if request.method == "POST":
        admin_otp = request.form["user_entered_otp"]

        # If otp Correct data will store in db
        if (str(admin_otp) == str(admin_rand)):
            ins_sql = "INSERT INTO ADMIN VALUES(?,?,?,?,?,?,?)"
            pstmt = ibm_db.prepare(conn, ins_sql)
            ibm_db.bind_param(pstmt, 1, admin_fullname)
            ibm_db.bind_param(pstmt, 2, admin_email)
            ibm_db.bind_param(pstmt, 3, admin_phonenumber)
            ibm_db.bind_param(pstmt, 4, admin_organization_name)
            ibm_db.bind_param(pstmt, 5, admin_organization_emp)
            ibm_db.bind_param(pstmt, 6, admin_organization_address)
            ibm_db.bind_param(pstmt, 7, admin_password)

            ibm_db.execute(pstmt)
            return render_template("login_admin.html", msg="Signup Success! Please Login to enjoy your stay!", admin_email=admin_email)

        else:
            return render_template("otp_admin_verify.html", otpmsg="INCORRECT OTP !",admin_fullname=admin_fullname, admin_email=admin_email, admin_phonenumber=admin_phonenumber, admin_organization_name=admin_organization_name, admin_organization_emp=admin_organization_emp, admin_organization_address=admin_organization_address, admin_password=admin_password)









#------------------------  DASHBOARD USER  -----------------------

@app.route('/dashboarduser')
def dashboarduser():

    logintype = session.get("login_type")
    loginemail = session.get("login_email")

    if (logintype==None or loginemail==None) :
        return render_template('dashboard_user.html',logintype="none",loginemail="none")
    else:
        
        return render_template('dashboard_user.html',logintype=logintype,loginemail=loginemail)


#------------------------  RETRIVE PROBLEM AND FETCH-----------------------

@app.route('/retriveproblem')
def retriveproblem():

    logintype = session.get("login_type")
    loginemail = session.get("login_email")

    if (logintype==None or loginemail==None) :
        return render_template('retrive_problem.html',logintype="none",loginemail="none")
    else:
        list = []
        prb_sql = "SELECT PROBLEM FROM SPECIAL "
        stmt = ibm_db.prepare(conn,prb_sql)
        ibm_db.execute(stmt)
        prb = ibm_db.fetch_both(stmt)
        while prb:
            list.append(prb)
            prb = ibm_db.fetch_both(stmt)

        if list:
            return render_template('retrive_problem.html',logintype=logintype,loginemail=loginemail,list=list)

        return render_template('retrive_problem.html',logintype=logintype,loginemail=loginemail)


#------------------------  RAISE TICKET PAGE WITH AGENT EMAIL -----------------------

@app.route('/raiseticket',methods=['POST','GET'])
def raiseticket():

    logintype = session.get("login_type")
    loginemail = session.get("login_email")


    if (logintype==None or loginemail==None) :
        return render_template('raise_ticket.html',logintype="none",loginemail="none")
    else:
        if request.method == "POST":
            problem = request.form['special']

            selsql = "SELECT EMAIL FROM SPECIAL WHERE PROBLEM=?"
            stmt = ibm_db.prepare(conn,selsql)
            ibm_db.bind_param(stmt,1,problem)
            ibm_db.execute(stmt)
            getemail = ibm_db.fetch_both(stmt)
            if getemail:
                return render_template('raise_ticket.html',logintype=logintype,loginemail=loginemail,agentemail=getemail)
            else:
                return "Agent not assigned"

        return render_template('raise_ticket.html',logintype=logintype,loginemail=loginemail)


#------------------------  RAISE TICKET FINAL DB INSERT-----------------------

@app.route('/addticket',methods=['POST','GET'])
def addticket():
    
    if request.method == "POST":
        global agentemail
        cusemail = request.form['cusemail']
        agentemail = request.form['getemail']
        query = request.form['query']
        name = request.form['name']
        ticket  = random.randint(100000,999999)
        status = 'pending'
        
        #Storing the data in the Table CUSTOMERQUERIES
        ins_sql = "INSERT INTO CUSTOMERQUERIES VALUES(?,?,?,?,?,?)"
        pstmt = ibm_db.prepare(conn,ins_sql)
        ibm_db.bind_param(pstmt,1,cusemail)
        ibm_db.bind_param(pstmt,2,query)
        ibm_db.bind_param(pstmt,3,name)
        ibm_db.bind_param(pstmt,4,ticket)
        ibm_db.bind_param(pstmt,5,agentemail)
        ibm_db.bind_param(pstmt,6,status)
        ibm_db.execute(pstmt)

        #Storing the data in the Admin Dashboard
        das_sql = "INSERT INTO ADMINQUERIES VALUES(?)"
        stm = ibm_db.prepare(conn,das_sql)
        ibm_db.bind_param(stm,1,ticket)

        ibm_db.execute(stm)

        #Sending the Email to the Customer change the api key to 'YOUR_API_ KEY'
        from_email = Email("2k19cse038@kiot.ac.in","Customer Care Registry")
        to_email = To(cusemail)
        subject = "Requester  #"+str(ticket)
        if agentemail == "NotAssign":
            content = Content("text/plain", "Hi "+name+ ",\n\nGreetings.\n\nThanks for contacting Customer care  Support for your query. We strive to provide excellent service, and will respond to your request as soon as possible.\n\n---------DETAILS---------\nTicket-id:  "+str(ticket)+"\nTicket Status :  "+status+"\nAgent Status :  Not Assigned\nRequested Query :  "+query+"\n\n\nRegards,\n\nCustomer Care Registery.")
        else:
            content = Content("text/plain", "Hi "+name+ ",\n\nGreetings.\n\nThanks for contacting Customer care  Support for your query. We strive to provide excellent service, and will respond to your request as soon as possible.\n\n---------DETAILS---------\nTicket-id:  "+str(ticket)+"\nTicket Status :  "+status+"\nAgent Status :  Assigned\nRequested Query :  "+query+"\n\n\nRegards,\n\nCustomer Care Registery.")

        mail = Mail(from_email, to_email, subject, content)
        sg = sendgrid.SendGridAPIClient('KEY')
        response = sg.client.mail.send.post(request_body=mail.get())

        return "Query is Updated"
    return "NULL"








#------------------------  DASHBOARD ADMIN  -----------------------

@app.route('/dashboardadmin')
def dashboardadmin():
    logintype = session.get("login_type")
    loginemail = session.get("login_email")

    if (logintype==None or loginemail==None) :
        return render_template('ticketstohandle.html',logintype="none",loginemail="none")
    else:
        return render_template('ticketstohandle.html',logintype=logintype,loginemail=loginemail)









#------------------------  DASHBOARD AGENT  -----------------------

@app.route('/dashboardagent')
def dashboardagent():
    logintype = session.get("login_type")
    loginemail = session.get("login_email")

    if (logintype==None or loginemail==None) :
        return render_template('dashboard_agent.html',logintype="none",loginemail="none")
    else:
        return render_template('dashboard_agent.html',logintype=logintype,loginemail=loginemail)






#------------------------  LOGOUT -----------------------
@app.route('/logout')
def logout():
    logintype = session.get("login_type")
    loginemail = session.get("login_email")

    if (logintype==None or loginemail==None) :
        return render_template('logout.html',logintype="none",loginemail="none")
    else:
        return render_template('logout.html',logintype=logintype,loginemail=loginemail)

@app.route('/logoutdata')
def logoutdata():
    session["login_type"] = None
    session["login_email"] = None
    time.sleep(2.0)
    return redirect("/")

    





if __name__ == '__main__':
    app.run(debug=True)
