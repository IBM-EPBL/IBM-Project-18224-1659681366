from flask import Flask, render_template, request, session, redirect
from flask_session import Session
import time

#-------------------- FOR SENDGRID AND OTP ----------------- 
import sendgrid
import os
from sendgrid.helpers.mail import *
import random

import datetime


#-------------------- FOR matplot chart----------------- 
import numpy as np
import matplotlib.pyplot as plt
import mpld3

import string

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
    else:
        return render_template("single_page.html",message="Error occured")







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
    else:
        return render_template("single_page.html",message="Error occured")








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
    else:
        return render_template("single_page.html",message="Error occured")







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
            sg = sendgrid.SendGridAPIClient('YOUR-SENDGRID-API-KEY')
            response = sg.client.mail.send.post(request_body=mail.get())
            return render_template('otp_user_verify.html',otpmsg="OTP SENT SUCCESSFULLY !", user_fullname=user_fullname, user_email=user_email, user_phonenumber=user_phonenumber, user_password=user_password)
    else:
        return render_template("single_page.html",message="Error occured")

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
    else:
        return render_template("single_page.html",message="Error occured")








#------------------------  SIGNUP ADMIN   -----------------------

@app.route('/signupadmin')
def signupadmin():
    logintype = session.get("login_type")

    if (logintype==None) :
        return render_template('signup_admin.html',logintype="none")
    else:
        return render_template('signup_admin.html',logintype=logintype)

#------------------------  SIGNUP ADMIN   -----------------------
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
            sg = sendgrid.SendGridAPIClient('YOUR-SENDGRID-API-KEY')
            response = sg.client.mail.send.post(request_body=mail.get())
            return render_template('otp_admin_verify.html',otpmsg="OTP SENT SUCCESSFULLY !", admin_fullname=admin_fullname, admin_email=admin_email, admin_phonenumber=admin_phonenumber, admin_organization_name=admin_organization_name, admin_organization_emp=admin_organization_emp, admin_organization_address=admin_organization_address, admin_password=admin_password)
    else:
        return render_template("single_page.html",message="Error occured")

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
    else:
        return render_template("single_page.html",message="Error occured")









#------------------------  DASHBOARD USER  -----------------------

@app.route('/dashboarduser')
def dashboarduser():

    logintype = session.get("login_type")
    loginemail = session.get("login_email")

    if (logintype==None or loginemail==None) :
        return render_template('dashboard_user.html',logintype="none",loginemail="none")
    else:
        return render_template('dashboard_user.html',logintype=logintype,loginemail=loginemail)


#------------------------  DASHBOARD KNOWLEDGE BASE  -----------------------

@app.route('/knowledge')
def knowledge():
    logintype = session.get("login_type")
    loginemail = session.get("login_email")
    if (logintype==None or loginemail==None) :
        return render_template('knowledge.html',logintype="none",loginemail="none")
    else:
        return render_template('knowledge.html',logintype=logintype,loginemail=loginemail)


#------------------------  DASHBOARD PROFILE  -----------------------

@app.route('/userprofile')
def userprofile():
    logintype = session.get("login_type")
    loginemail = session.get("login_email")
    if (logintype==None or loginemail==None) :
        return render_template('userprofile.html',logintype="none",loginemail="none")
    else:
        list = []
        cus_sql = "SELECT FULLNAME,EMAIL FROM CUSTOMER WHERE EMAIL=? "
        stmt = ibm_db.prepare(conn,cus_sql)
        ibm_db.bind_param(stmt,1,loginemail)
        ibm_db.execute(stmt)
        cus = ibm_db.fetch_tuple(stmt)
        while cus:
            list.append(cus)
            cus = ibm_db.fetch_tuple(stmt)

        ticklist = []
        tick_sql = "SELECT TICKET_ID,STATUS FROM CUSTOMERQUERIES WHERE EMAIL=? "
        stmtT = ibm_db.prepare(conn,tick_sql)
        ibm_db.bind_param(stmtT,1,loginemail)
        ibm_db.execute(stmtT)
        tick = ibm_db.fetch_tuple(stmtT)
        while tick:
            ticklist.append(tick)
            tick = ibm_db.fetch_tuple(stmtT)

        if list:
            if ticklist:
                return render_template('userprofile.html',logintype=logintype,loginemail=loginemail,list=list,ticklist=ticklist)
            else:
                return render_template('userprofile.html',logintype=logintype,loginemail=loginemail,list=list,msg="No ticket Available!")

        return render_template('userprofile.html',logintype=logintype,loginemail=loginemail)


#------------------------  DASHBOARD USER TICKET IN PROFILE   -----------------------

@app.route('/userprofileticket',methods=['POST','GET'])
def userprofileticket():

    logintype = session.get("login_type")
    loginemail = session.get("login_email")

    if (logintype==None or loginemail==None) :
        return render_template('user_profile_ticket.html',logintype="none",loginemail="none")
    else:
        if request.method =='POST':
            qlist = []
            global userticket
            userticket = request.form['ticket']
            whois = "customer"

            sel_sql = "SELECT RESPONSE FROM ALLRESQUE WHERE TICKET_ID=? AND WHO=?"
            stmt = ibm_db.prepare(conn,sel_sql)
            ibm_db.bind_param(stmt,1,userticket)
            ibm_db.bind_param(stmt,2,whois)
            ibm_db.execute(stmt)
            query = ibm_db.fetch_both(stmt)

            while query:
                qlist.append(query)
                query = ibm_db.fetch_both(stmt)


            # Getting the Agent email for Name
            ema_sql = "SELECT AGENT_EMAIL FROM CUSTOMERQUERIES WHERE TICKET_ID=? "
            emt = ibm_db.prepare(conn,ema_sql)
            ibm_db.bind_param(emt,1,userticket)
            ibm_db.execute(emt)
            email = ibm_db.fetch_both(emt)
            newemail = email[0]

            # Show the Name oof the Agent
            nam_sql = "SELECT FULLNAME FROM AGENT WHERE EMAIL=?"
            nmt = ibm_db.prepare(conn,nam_sql)
            ibm_db.bind_param(nmt,1,newemail)
            ibm_db.execute(nmt)
            agentname = ibm_db.fetch_both(nmt)

            dat_sql = "SELECT DATE FROM ALLRESQUE WHERE TICKET_ID=?"
            stmtdate = ibm_db.prepare(conn,dat_sql)
            ibm_db.bind_param(stmtdate,1,userticket)
            ibm_db.execute(stmtdate)
            querydate = ibm_db.fetch_both(stmtdate)

            tim_sql = "SELECT TIME FROM ALLRESQUE WHERE TICKET_ID=?"
            stmttime = ibm_db.prepare(conn,tim_sql)
            ibm_db.bind_param(stmttime,1,userticket)
            ibm_db.execute(stmttime)
            querytime = ibm_db.fetch_both(stmttime)


            if qlist :
                return render_template("user_profile_ticket.html",ticket = userticket,qlist=qlist,agentname=agentname,querydate=querydate,querytime=querytime)
            else:
                return render_template("single_page.html",message="Error occured")
        else:
            return render_template("single_page.html",message="Error occured")


#------------------------  DASHBOARD Again getting the Query   -----------------------
@app.route('/againquery',methods=['POST','GET'])
def againquery():
    if request.method == "POST":
        againreply = request.form["againquery"]
        status  = 'pending'
        whois = 'customer'
        # Updating the CUSTOMERQUERIES Table in db
        # Just Update the Last Query and Status
        up_sql = "UPDATE CUSTOMERQUERIES SET STATUS = ? , QUERIES =? WHERE TICKET_ID = ?;"
        upstmst = ibm_db.prepare(conn,up_sql)
        ibm_db.bind_param(upstmst,1,status)
        ibm_db.bind_param(upstmst,2,againreply)
        ibm_db.bind_param(upstmst,3,userticket)
        ibm_db.execute(upstmst)

        x = datetime.datetime.now()
        date = x.strftime("%x")
        time = x.strftime("%X")

        allresq_sql = "INSERT INTO ALLRESQUE(TICKET_ID,RESPONSE,WHO,DATE,TIME) VALUES(?,?,?,?,?)"
        stmp = ibm_db.prepare(conn,allresq_sql)
        ibm_db.bind_param(stmp,1,userticket)
        ibm_db.bind_param(stmp,2,againreply)
        ibm_db.bind_param(stmp,3,whois)
        ibm_db.bind_param(stmp,4,date)
        ibm_db.bind_param(stmp,5,time)

        ibm_db.execute(stmp)

        return render_template("single_page.html",message="Query updated")
    else:
        return render_template("single_page.html",message="Error occured")


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
        else:
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
                return render_template("single_page.html",message="agent not available")
        else:
            return render_template("single_page.html",message="Error occured")


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
        whois = 'customer'
        
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


        x = datetime.datetime.now()
        date = x.strftime("%x")
        time = x.strftime("%X")

        allresq_sql = "INSERT INTO ALLRESQUE(TICKET_ID,RESPONSE,WHO,DATE,TIME) VALUES(?,?,?,?,?)"
        stmp = ibm_db.prepare(conn,allresq_sql)
        ibm_db.bind_param(stmp,1,ticket)
        ibm_db.bind_param(stmp,2,query)
        ibm_db.bind_param(stmp,3,whois)
        ibm_db.bind_param(stmp,4,date)
        ibm_db.bind_param(stmp,5,time)

        ibm_db.execute(stmp)

        # Sending the Email to the Customer change the api key to 'YOUR_API_ KEY'
        from_email = Email("2k19cse038@kiot.ac.in","Customer Care Registry")
        to_email = To(cusemail)
        subject = "Requester  #"+str(ticket)
        if agentemail == "NotAssign":
            content = Content("text/plain", "Hi "+name+ ",\n\nGreetings.\n\nThanks for contacting Customer care  Support for your query. We strive to provide excellent service, and will respond to your request as soon as possible.\n\n---------DETAILS---------\nTicket-id:  "+str(ticket)+"\nTicket Status :  "+status+"\nAgent Status :  Not Assigned\nRequested Query :  "+query+"\n\n\nRegards,\n\nCustomer Care Registery.")
        else:
            content = Content("text/plain", "Hi "+name+ ",\n\nGreetings.\n\nThanks for contacting Customer care  Support for your query. We strive to provide excellent service, and will respond to your request as soon as possible.\n\n---------DETAILS---------\nTicket-id:  "+str(ticket)+"\nTicket Status :  "+status+"\nAgent Status :  Assigned\nRequested Query :  "+query+"\n\n\nRegards,\n\nCustomer Care Registery.")

        mail = Mail(from_email, to_email, subject, content)
        sg = sendgrid.SendGridAPIClient('YOUR-SENDGRID-API-KEY')
        response = sg.client.mail.send.post(request_body=mail.get())
        return render_template("single_page.html",message="Query is Updated")
    else:
        return render_template("single_page.html",message="Error occured")















#------------------------  DASHBOARD ADMIN  -----------------------

@app.route('/dashboardadmin')
def dashboardadmin():
    logintype = session.get("login_type")
    loginemail = session.get("login_email")
    global messages

    if (logintype==None or loginemail==None) :
        return render_template('admin_allticket.html',logintype="none",loginemail="none")
    else:
        messages = "allticket"
        list =[]
        #Display all tickets from the Db
        all_sql = "SELECT * FROM CUSTOMERQUERIES "
        allmt = ibm_db.prepare(conn,all_sql)
        ibm_db.execute(allmt)
        alltable = ibm_db.fetch_both(allmt)

        #Looping the All Table
        while alltable:
            list.append(alltable)
            alltable = ibm_db.fetch_both(allmt)

        if list:
            return render_template("admin_allticket.html",list=list,logintype=logintype,loginemail=loginemail)
        else:
            return render_template('admin_allticket.html',logintype=logintype,loginemail=loginemail)


@app.route('/adminsinglepage',methods=['POST','GET'])
def adminsinglepage():
    logintype = session.get("login_type")
    loginemail = session.get("login_email")
    global messages

    if (logintype==None or loginemail==None) :
        return render_template('admin_single_page.html',logintype="none",loginemail="none")
    else:
        if request.method == "POST":
            adminkey = request.form['getsinglemsg']
            if(adminkey=="handle"):
                messages = "NotAssign"
                all_sql = "SELECT * FROM CUSTOMERQUERIES WHERE AGENT_EMAIL=?"
            if(adminkey=="open" or adminkey=="pending" or adminkey=="solved" or adminkey=="closed"):
                messages = adminkey
                all_sql = "SELECT * FROM CUSTOMERQUERIES WHERE STATUS=?"
            
            list =[]

            allmt = ibm_db.prepare(conn,all_sql)
            ibm_db.bind_param(allmt, 1, messages)
            ibm_db.execute(allmt)
            alltable = ibm_db.fetch_both(allmt)

            #Looping the All Table
            while alltable:
                list.append(alltable)
                alltable = ibm_db.fetch_both(allmt)

            if list:
                return render_template("admin_single_page.html",msg=messages,list=list,logintype=logintype,loginemail=loginemail)
            else:
                return render_template('admin_single_page.html',msg=messages,logintype=logintype,loginemail=loginemail)
        else:
            return render_template("single_page.html",message="Error occured")


@app.route('/adminlistchat',methods=['POST','GET'])
def adminlistchat():
    if request.method =='POST':
        qlist = []
        global getticket
        getticket = request.form['ticket']

        stat_sql = "SELECT STATUS FROM CUSTOMERQUERIES WHERE TICKET_ID=?"
        st = ibm_db.prepare(conn,stat_sql)
        ibm_db.bind_param(st,1,getticket)
        ibm_db.execute(st)
        status = ibm_db.fetch_both(st)

        sel_sql = "SELECT RESPONSE,WHO FROM ALLRESQUE WHERE TICKET_ID=?"
        stmt = ibm_db.prepare(conn,sel_sql)
        ibm_db.bind_param(stmt,1,getticket)
        ibm_db.execute(stmt)
        query = ibm_db.fetch_both(stmt)

        while query:
            qlist.append(query)
            query = ibm_db.fetch_both(stmt)

        dat_sql = "SELECT DATE FROM ALLRESQUE WHERE TICKET_ID=?"
        stmtdate = ibm_db.prepare(conn,dat_sql)
        ibm_db.bind_param(stmtdate,1,getticket)
        ibm_db.execute(stmtdate)
        querydate = ibm_db.fetch_both(stmtdate)

        tim_sql = "SELECT TIME FROM ALLRESQUE WHERE TICKET_ID=?"
        stmttime = ibm_db.prepare(conn,tim_sql)
        ibm_db.bind_param(stmttime,1,getticket)
        ibm_db.execute(stmttime)
        querytime = ibm_db.fetch_both(stmttime)




        listemail = []
        notassign = 'NotAssign'
        prb_sql = "SELECT EMAIL FROM SPECIAL WHERE NOT EMAIL = ?"
        stmtt = ibm_db.prepare(conn,prb_sql)
        ibm_db.bind_param(stmtt,1,notassign)
        ibm_db.execute(stmtt)
        prb = ibm_db.fetch_both(stmtt)
        while prb:
            listemail.append(prb)
            prb = ibm_db.fetch_both(stmtt)


        if qlist :
            return render_template("admin_list_chat.html",ticket = getticket,qlist=qlist,listemail=listemail,messages=messages,status=status,querydate=querydate,querytime=querytime)
    else:
        return render_template("single_page.html",message="Error occured")


@app.route("/addfulldata",methods=['POST','GET'])
def addfulldata():
    if request.method =="POST":
        status = request.form['status']
        reply = request.form['reply']
        whois = "agent"

        x = datetime.datetime.now()
        date = x.strftime("%x")
        time = x.strftime("%X")

        allresq_sql = "INSERT INTO ALLRESQUE(TICKET_ID,RESPONSE,WHO,DATE,TIME) VALUES(?,?,?,?,?)"
        stmp = ibm_db.prepare(conn,allresq_sql)
        ibm_db.bind_param(stmp,1,getticket)
        ibm_db.bind_param(stmp,2,reply)
        ibm_db.bind_param(stmp,3,whois)
        ibm_db.bind_param(stmp,4,date)
        ibm_db.bind_param(stmp,5,time)

        ibm_db.execute(stmp)

        #Query for updating the Status in the CUSTOMERQUERIES Table
        up_sql = "UPDATE CUSTOMERQUERIES SET STATUS = ? WHERE TICKET_ID = ?;"
        upstmst = ibm_db.prepare(conn,up_sql)
        ibm_db.bind_param(upstmst,1,status)
        ibm_db.bind_param(upstmst,2,getticket)
        ibm_db.execute(upstmst)


        em_sql = "SELECT EMAIL FROM CUSTOMERQUERIES WHERE TICKET_ID=?"
        stmtem = ibm_db.prepare(conn,em_sql)
        ibm_db.bind_param(stmtem,1,getticket)
        ibm_db.execute(stmtem)
        useremail = ibm_db.fetch_both(stmtem)


        from_email = Email("2k19cse038@kiot.ac.in","CUSTOMER CARE REGISTRY")
        to_email = To(useremail[0])
        subject = "RESPONSE"
        content = Content("text/plain", "TICKET  #"+getticket+",\nThis is your RESPONSE FROM AGENT : "+str(reply)+"\n STATUS : "+str(status))
        mail = Mail(from_email, to_email, subject, content)
        sg = sendgrid.SendGridAPIClient('YOUR-SENDGRID-API-KEY')
        response = sg.client.mail.send.post(request_body=mail.get())

        return render_template("single_page.html",message="update successfully")
    else:
        return render_template("single_page.html",message="Error occured")

@app.route("/updatedagent",methods=['POST','GET'])
def updatedagent():
    if request.method =="POST":
        updateagent = request.form['updateagent']
        #Query for updating the Status in the CUSTOMERQUERIES Table
        up_agent_sql = "UPDATE CUSTOMERQUERIES SET AGENT_EMAIL = ? WHERE TICKET_ID = ?;"
        upagentstmst = ibm_db.prepare(conn,up_agent_sql)
        ibm_db.bind_param(upagentstmst,1,updateagent)
        ibm_db.bind_param(upagentstmst,2,getticket)
        ibm_db.execute(upagentstmst)
        return redirect("/dashboardadmin")
    else:
        return render_template("single_page.html",message="Error occured")


#------------------------  DASHBOARD ADMIN PROFILE -----------------------

@app.route('/adminprofile')
def adminprofile():
    logintype = session.get("login_type")
    loginemail = session.get("login_email")

    if (logintype==None or loginemail==None) :
        return render_template('userprofile.html',logintype="none",loginemail="none")
    else:
        list = []
        cus_sql = "SELECT FULLNAME,EMAIL,ORGANIZATIONNAME,ORGANIZATIONEMPLOYEES FROM ADMIN WHERE EMAIL=? "
        stmt = ibm_db.prepare(conn,cus_sql)
        ibm_db.bind_param(stmt,1,loginemail)
        ibm_db.execute(stmt)
        cus = ibm_db.fetch_tuple(stmt)
        while cus:
            list.append(cus)
            cus = ibm_db.fetch_tuple(stmt)

        if list:
            return render_template('adminprofile.html',logintype=logintype,loginemail=loginemail,list=list)

        return render_template('adminprofile.html',logintype=logintype,loginemail=loginemail)



#------------------------  DASHBOARD ADMIN KNOWLEDGE BASE -----------------------

@app.route('/knowledgebase')
def knowledgebase():

    logintype = session.get("login_type")
    loginemail = session.get("login_email")


    if (logintype==None or loginemail==None) :
        return render_template('knowledge2.html',logintype="none",loginemail="none")
    else:
        return render_template('knowledge2.html',logintype=logintype,loginemail=loginemail,list=list)


#------------------------  DASHBOARD ADMIN REPORT -----------------------

@app.route('/report')
def report():

    logintype = session.get("login_type")
    loginemail = session.get("login_email")

    if (logintype==None or loginemail==None) :
        return render_template('report.html',logintype="none",loginemail="none")
    else:
        #For Open Status
        list= []
        ostat = 'open'
        sel_sql = "SELECT COUNT(STATUS) FROM CUSTOMERQUERIES WHERE STATUS=?"
        stmt = ibm_db.prepare(conn,sel_sql)
        ibm_db.bind_param(stmt,1,ostat)
        ibm_db.execute(stmt)
        query = ibm_db.fetch_both(stmt)
        #Appending the list
        list.append(query[0])
    
        #For Closed Status
        cstat = 'closed'
        csel_sql = "SELECT COUNT(STATUS) FROM CUSTOMERQUERIES WHERE STATUS=?"
        cstmt = ibm_db.prepare(conn,csel_sql)
        ibm_db.bind_param(cstmt,1,cstat)
        ibm_db.execute(cstmt)
        cquery = ibm_db.fetch_both(cstmt)
        #Appending the list
        list.append(cquery[0])

        #For Pending Status
        pstat = 'pending'
        psel_sql = "SELECT COUNT(STATUS) FROM CUSTOMERQUERIES WHERE STATUS=?"
        pstmt = ibm_db.prepare(conn,psel_sql)
        ibm_db.bind_param(pstmt,1,pstat)
        ibm_db.execute(pstmt)
        pquery = ibm_db.fetch_both(pstmt)
        #Appending the list
        list.append(pquery[0])

        #For Solved Status
        sstat = 'solved'
        ssel_sql = "SELECT COUNT(STATUS) FROM CUSTOMERQUERIES WHERE STATUS=?"
        sstmt = ibm_db.prepare(conn,ssel_sql)
        ibm_db.bind_param(sstmt,1,sstat)
        ibm_db.execute(sstmt)
        squery = ibm_db.fetch_both(sstmt)
        #Appending the list
        list.append(squery[0])

        # Printing the Pie Chart
        fig = plt.figure(figsize=(10,10))

        y = np.array(list)
        mylabels = ["Open", "Closed", "Pending", "Solved"]
        # myexplode = [0.2, 0, 0, 0]

        total = sum(y)
        plt.pie(y, labels = mylabels,autopct=lambda p: '{:.0f}%'.format(p * total / 100),shadow = True)
        plt.legend(title = "Ticket Status")
        
        # plt.show()
        html_str = mpld3.fig_to_html(fig)
        Html_file= open("templates/report.html","w")
        Html_file.write(html_str)
        Html_file.close()
        return render_template('report.html')


#------------------------  DASHBOARD ADMIN INVITE -----------------------
@app.route('/inviteagents')
def inviteagents():
    return render_template("ad-inviteagent.html")

#------------------------  DASHBOARD ADMIN INVITE FINAL -----------------------
@app.route('/addinviteagents',methods=['POST','GET'])
def addinviteagents():
    if request.method =="POST":
        name = request.form['name']
        invemail = request.form['email']
        # Checking the Exixting Agent or Not
        selsql = "SELECT * FROM AGENT WHERE EMAIL=?"
        stmt = ibm_db.prepare(conn,selsql)
        ibm_db.bind_param(stmt,1,invemail)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)

        if acc:
            return render_template("single_page.html",message="Existing Agent , so Assign new Role")
        else:
            #Generating the Random Password with digits and lowercase for digits add -> +string.digits befor comma
            N = 8
            res = ''.join(random.choices(string.ascii_lowercase, k=N))
            #Storing in Db
            ins_sql = "INSERT INTO AGENT VALUES(?,?,?)"
            pstmt = ibm_db.prepare(conn,ins_sql)
            ibm_db.bind_param(pstmt,1,name)
            ibm_db.bind_param(pstmt,2,invemail)
            ibm_db.bind_param(pstmt,3,res)
            ibm_db.execute(pstmt)

            from_email = Email("2k19cse038@kiot.ac.in","CUSTOMER CARE REGISTRY")
            to_email = To(invemail)
            subject = "Invitation( AGENT )"
            content = Content("text/plain", "Hi "+name+" , \nThis is your Email : "+str(invemail)+"\n Password : "+str(res))
            mail = Mail(from_email, to_email, subject, content)
            sg = sendgrid.SendGridAPIClient('YOUR-SENDGRID-API-KEY')
            response = sg.client.mail.send.post(request_body=mail.get())

            # Wan to send email to the Agent
            return render_template("single_page.html",message="successfully invited")
    else:
        return render_template("single_page.html",message="Error occured")


#------------------------  DASHBOARD ADMIN AGENTS -----------------------

@app.route('/listagent')
def listagent():

    logintype = session.get("login_type")
    loginemail = session.get("login_email")


    if (logintype==None or loginemail==None) :
        return render_template('list_agent.html',logintype="none",loginemail="none")
    else:
        emails = "NotAssign"
        list =[]
        #Display all tickets from the Db
        all_agent = "SELECT FULLNAME,EMAIL FROM AGENT WHERE EMAIL != ?"
        allmtt = ibm_db.prepare(conn,all_agent)
        ibm_db.bind_param(allmtt, 1, emails)
        ibm_db.execute(allmtt)
        alltable = ibm_db.fetch_both(allmtt)

        #Looping the All Table
        while alltable:
            list.append(alltable)
            alltable = ibm_db.fetch_both(allmtt)

        return render_template('list_agent.html',logintype=logintype,loginemail=loginemail,list=list)

#------------------------  DASHBOARD ADMIN NEW ROLE -----------------------
@app.route('/newrole',methods=['POST','GET'])
def newrole():
    if request.method == 'POST':
        setagent =request.form['email']
        problem = request.form['problem']

        sel_sql = "SELECT problem FROM SPECIAL WHERE  EMAIL= ?"
        stmt = ibm_db.prepare(conn,sel_sql)
        ibm_db.bind_param(stmt,1,setagent)
        ibm_db.execute(stmt)
        checkprb = ibm_db.fetch_assoc(stmt)

        if checkprb:
            return render_template("single_page.html",message="Agent has Assigned a Exixting Problem")
        else:
            #Inserting the Email and Problem in Table SPECIAL
            ns_sql = "INSERT INTO SPECIAL VALUES(?,?)"
            pstmt = ibm_db.prepare(conn,ns_sql)
            ibm_db.bind_param(pstmt,1,problem)
            ibm_db.bind_param(pstmt,2,setagent)
            ibm_db.execute(pstmt)
            return render_template("single_page.html",message="Successfully Assigned")
    else:
        return render_template("single_page.html",message="Error occured")


#------------------------  DASHBOARD ADMIN SHOW AGENT DETAILS  -----------------------
@app.route('/agentdetails',methods=['POST','GET'])
def agentdetails():
    logintype = session.get("login_type")
    loginemail = session.get("login_email")

    if (logintype==None or loginemail==None) :
        return render_template('list_agent.html',logintype="none",loginemail="none")
    else:
        if request.method == "POST":
            list =[]
            global agentemail
            agentemail = request.form['email']

            #Getting the Details of the Agent
            sel_sql = "SELECT AGENT.FULLNAME , AGENT.EMAIL , SPECIAL.PROBLEM FROM AGENT INNER JOIN SPECIAL ON AGENT.EMAIL = SPECIAL.EMAIL WHERE AGENT.EMAIL=?"
            stmt = ibm_db.prepare(conn,sel_sql)
            ibm_db.bind_param(stmt,1,agentemail)
            ibm_db.execute(stmt)
            query = ibm_db.fetch_both(stmt)
            while query:
                list.append(query)
                query = ibm_db.fetch_both(stmt)
            if list:
                return render_template("list-agent-details.html",logintype=logintype,loginemail=loginemail,list=list)
            else:
                return render_template("single_page.html",message="role not yet assigned")
        else:
            return render_template("single_page.html",message="Error occured")


@app.route('/updateproblem',methods=['POST','GET'])
def updateproblem():
    if request.method == 'POST':
        role = request.form['role']

        # Updating the Query
        up_sql = "UPDATE SPECIAL SET EMAIL = ? WHERE PROBLEM = ?;"
        upstmst = ibm_db.prepare(conn,up_sql)
        ibm_db.bind_param(upstmst,1,agentemail)
        ibm_db.bind_param(upstmst,2,role)
        
        ibm_db.execute(upstmst)
        return render_template("single_page.html",message="update successfully")
    else:
        return render_template("single_page.html",message="Error occured")

@app.route('/deleteagentrole')
def deleteagentrole():
    up_sql = "DELETE FROM SPECIAL WHERE EMAIL = ?"
    upstmst = ibm_db.prepare(conn,up_sql)
    ibm_db.bind_param(upstmst,1,agentemail)
        
    ibm_db.execute(upstmst)
    return render_template("single_page.html",message="deleted successfully")








#------------------------  DASHBOARD AGENT  -----------------------

@app.route('/dashboardagent')
def dashboardagent():
    logintype = session.get("login_type")
    loginemail = session.get("login_email")

    if (logintype==None or loginemail==None) :
        return render_template('agent_allticket.html',logintype="none",loginemail="none")
    else:
        list =[]
        #Display all tickets from the Db
        all_sql = "SELECT * FROM CUSTOMERQUERIES WHERE AGENT_EMAIL = ?"
        allmt = ibm_db.prepare(conn,all_sql)
        ibm_db.bind_param(allmt, 1, loginemail)
        ibm_db.execute(allmt)
        alltable = ibm_db.fetch_both(allmt)

        #Looping the All Table
        while alltable:
            list.append(alltable)
            alltable = ibm_db.fetch_both(allmt)

        if list:
            return render_template("agent_allticket.html",list=list,logintype=logintype,loginemail=loginemail)
        else:
            return render_template('agent_allticket.html',logintype=logintype,loginemail=loginemail)

 

@app.route('/agentsinglepage',methods=['POST','GET'])
def agentsinglepage():
    logintype = session.get("login_type")
    loginemail = session.get("login_email")
    global messages

    if (logintype==None or loginemail==None) :
        return render_template('agent_single_page.html',logintype="none",loginemail="none")
    else:
        if request.method == "POST":
            adminkey = request.form['getsinglemsg']
            messages = adminkey
            
            list =[]

            all_sql = "SELECT * FROM CUSTOMERQUERIES WHERE STATUS = ? AND AGENT_EMAIL = ?"
            allmt = ibm_db.prepare(conn,all_sql)
            ibm_db.bind_param(allmt, 1, messages)
            ibm_db.bind_param(allmt, 2, loginemail)
            ibm_db.execute(allmt)
            alltable = ibm_db.fetch_both(allmt)

            #Looping the All Table
            while alltable:
                list.append(alltable)
                alltable = ibm_db.fetch_both(allmt)

            if list:
                return render_template("agent_single_page.html",msg=messages,list=list,logintype=logintype,loginemail=loginemail)
            else:
                return render_template('agent_single_page.html',msg=messages,logintype=logintype,loginemail=loginemail)
        else:
            return render_template("single_page.html",message="Error occured")

@app.route('/agentlistchat',methods=['POST','GET'])
def agentlistchat():
    if request.method =='POST':
        qlist = []
        global getticket
        getticket = request.form['ticket']


        stat_sql = "SELECT STATUS FROM CUSTOMERQUERIES WHERE TICKET_ID=?"
        st = ibm_db.prepare(conn,stat_sql)
        ibm_db.bind_param(st,1,getticket)
        ibm_db.execute(st)
        status = ibm_db.fetch_both(st)


        sel_sql = "SELECT RESPONSE,WHO FROM ALLRESQUE WHERE TICKET_ID=?"
        stmt = ibm_db.prepare(conn,sel_sql)
        ibm_db.bind_param(stmt,1,getticket)
        ibm_db.execute(stmt)
        query = ibm_db.fetch_both(stmt)

        while query:
            qlist.append(query)
            query = ibm_db.fetch_both(stmt)


        dat_sql = "SELECT DATE FROM ALLRESQUE WHERE TICKET_ID=?"
        stmtdate = ibm_db.prepare(conn,dat_sql)
        ibm_db.bind_param(stmtdate,1,getticket)
        ibm_db.execute(stmtdate)
        querydate = ibm_db.fetch_both(stmtdate)

        tim_sql = "SELECT TIME FROM ALLRESQUE WHERE TICKET_ID=?"
        stmttime = ibm_db.prepare(conn,tim_sql)
        ibm_db.bind_param(stmttime,1,getticket)
        ibm_db.execute(stmttime)
        querytime = ibm_db.fetch_both(stmttime)


        if qlist :
            return render_template("agent_list_chat.html",ticket = getticket,qlist=qlist,status=status,querydate=querydate,querytime=querytime)
    else:
        return render_template("single_page.html",message="Error occured")


@app.route("/agentaddfulldata",methods=['POST','GET'])
def agentaddfulldata():
    if request.method =="POST":
        status = request.form['status']
        reply = request.form['reply']
        whois = "agent"

        x = datetime.datetime.now()
        date = x.strftime("%x")
        time = x.strftime("%X")

        allresq_sql = "INSERT INTO ALLRESQUE(TICKET_ID,RESPONSE,WHO,DATE,TIME) VALUES(?,?,?,?,?)"
        stmp = ibm_db.prepare(conn,allresq_sql)
        ibm_db.bind_param(stmp,1,getticket)
        ibm_db.bind_param(stmp,2,reply)
        ibm_db.bind_param(stmp,3,whois)
        ibm_db.bind_param(stmp,4,date)
        ibm_db.bind_param(stmp,5,time)

        ibm_db.execute(stmp)

        #Query for updating the Status in the CUSTOMERQUERIES Table
        up_sql = "UPDATE CUSTOMERQUERIES SET STATUS = ? WHERE TICKET_ID = ?;"
        upstmst = ibm_db.prepare(conn,up_sql)
        ibm_db.bind_param(upstmst,1,status)
        ibm_db.bind_param(upstmst,2,getticket)
        ibm_db.execute(upstmst)

        em_sql = "SELECT EMAIL FROM CUSTOMERQUERIES WHERE TICKET_ID=?"
        stmtem = ibm_db.prepare(conn,em_sql)
        ibm_db.bind_param(stmtem,1,getticket)
        ibm_db.execute(stmtem)
        useremail = ibm_db.fetch_both(stmtem)


        from_email = Email("2k19cse038@kiot.ac.in","CUSTOMER CARE REGISTRY")
        to_email = To(useremail[0])
        subject = "RESPONSE"
        content = Content("text/plain", "TICKET  #"+getticket+",\nThis is your RESPONSE FROM AGENT : "+str(reply)+"\n STATUS : "+str(status))
        mail = Mail(from_email, to_email, subject, content)
        sg = sendgrid.SendGridAPIClient('YOUR-SENDGRID-API-KEY')
        response = sg.client.mail.send.post(request_body=mail.get())

        return render_template("single_page.html",message="Updated Successfully")
    else:
        return render_template("single_page.html",message="Error occured")


#------------------------  DASHBOARD ADMIN PROFILE -----------------------

@app.route('/agentprofile')
def agentprofile():

    logintype = session.get("login_type")
    loginemail = session.get("login_email")

    if (logintype==None or loginemail==None) :
        return render_template('userprofile.html',logintype="none",loginemail="none")
    else:
        list = []
        cus_sql = "SELECT FULLNAME,EMAIL FROM AGENT WHERE EMAIL=? "
        stmt = ibm_db.prepare(conn,cus_sql)
        ibm_db.bind_param(stmt,1,loginemail)
        ibm_db.execute(stmt)
        cus = ibm_db.fetch_tuple(stmt)
        while cus:
            list.append(cus)
            cus = ibm_db.fetch_tuple(stmt)

        if list:
            return render_template('agentprofile.html',logintype=logintype,loginemail=loginemail,list=list)
        else:
            return render_template('agentprofile.html',logintype=logintype,loginemail=loginemail)







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

@app.route('/commingsoon')
def commingsoon():
    return render_template('comingsoon.html')




@app.route('/forgetuseremail')
def adduseremail():
    return render_template("forget-email.html")

@app.route('/forgetadminemail')
def addadminemail():
    return render_template("forget-admin-email.html")

@app.route('/forgetagentemail')
def addagentemail():
    return render_template("forget-agent-email.html")



@app.route('/emailverfiy', methods=['POST','GET'])
def emailverify():
    if request.method == "POST":
        global foremail
        foremail = request.form['foremail']
        who = request.form['who']

        if who=="user":
            selsql = "SELECT * FROM CUSTOMER WHERE EMAIL=?"
        
        if who=="admin":
            selsql = "SELECT * FROM ADMIN WHERE EMAIL=?"

        if who=="agent":
            selsql = "SELECT * FROM AGENT WHERE EMAIL=?"

        # Checking for the email whether email is present or not
        stmt = ibm_db.prepare(conn,selsql)
        ibm_db.bind_param(stmt,1,foremail)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)
        fname = ibm_db.result(stmt,'FULLNAME')


        if acc:
            global forgotrand
            forgotrand = random.randint(10000,99999)
            from_email = Email("2k19cse038@kiot.ac.in","CUSTOMER CARE REGISTRY")
            to_email = To(foremail)
            subject = "Forgot Password"
            content = Content("text/plain", "Hi "+fname+",\nThe OTP for the Forgot Password is Initiated : "+str(forgotrand))
            mail = Mail(from_email, to_email, subject, content)

            sg = sendgrid.SendGridAPIClient('YOUR-SENDGRID-API-KEY')
            response = sg.client.mail.send.post(request_body=mail.get())
            return render_template("forget-new-pass.html",msg="OTP is send Successfully",who=who)
        else:
            return render_template("single_page.html",message="No account found")
    else:
        return render_template("single_page.html",message="Error occured")

@app.route("/newpass", methods=['POST','GET'])
def newpass():
    if request.method == 'POST':
        otpverify = request.form['otpverify']
        newpass = request.form["newpass"]
        who = request.form["who"]

        print(otpverify)
        if(str(otpverify)==str(forgotrand)):
            if who=="user":
                up_sql = "UPDATE CUSTOMER SET PASSWORD = ? WHERE EMAIL = ?;"
        
            if who=="admin":
                up_sql = "UPDATE ADMIN SET PASSWORD = ? WHERE EMAIL = ?;"

            if who=="agent":
                up_sql = "UPDATE AGENT SET PASSWORD = ? WHERE EMAIL = ?;"
            
            upstmst = ibm_db.prepare(conn,up_sql)
            ibm_db.bind_param(upstmst,1,newpass)
            ibm_db.bind_param(upstmst,2,foremail)
            ibm_db.execute(upstmst)
            return render_template("single_page.html",message="updated successfully")
        else:
            return render_template("single_page.html",message="otp doesn't match")
    else:
        return render_template("single_page.html",message="Error occured")





if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
