from flask import Flask,render_template
import ibm_db
conn =ibm_db.connect("DATABASE=bludb;HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31198;SECURITY=SSL;UID=jjn09936;PWD=ktf1zAbeEEq0OBLl",'','')

print(conn)
print("connection successful...")

app=Flask(__name__)

@app.route("/")
def root():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route('/signin',methods=["POST","GET"])
def signin():
   return render_template("signin.html")

@app.route('/addsignin',methods=['POST','GET'])
def addsignin():
    if request.method == "POST":
        email = request.form["email"]
        password  = request.form["password"]
        
        select_sql = "SELECT * FROM USERS WHERE EMAIL=?"
        statement = ibm_db.prepare(conn,select_sql)
        ibm_db.bind_param(statement,1,email)
        ibm_db.execute(statement)
        account = ibm_db.fetch_assoc(statement)
        firstname = ibm_db.result(statement,'FIRSTNAME')

        if acc:
            if(str(password)) == str(account['CPASS'].strip()):
                return render_template("home.html",messge="Welcome,",firstname = firstname)
            else:
                return render_template("signin.html",messge="Invalid E-Mail or Password")

        else:
            return render_template("signup.html",messge="Not a Member First SignUp")

@app.route('/signup',methods=['POST','GET'])
def signup(): 
    return render_template("signup.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/addsignup',methods=["POST","GET"])
def addsignup():
    if request.method == "POST":
        fname = request.form['firstname']
        lname = request.form["lastname"]
        email = request.form["email"]
        num = request.form["number"]
        passwrd = request.form["password"]
        cpass = request.form["confirmpassword"]

        select_sql = "SELECT * FROM PERSON WHERE EMAIL=?"
        stmt = ibm_db.prepare(conn,select_sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)

        if acc:
            return render_template("signin.html",text="Your are a Existing User so Please Sign In")
        
        else:
            ins_sql = "INSERT INTO PERSON VALUES(?,?,?,?,?,?)"
            stmt = ibm_db.prepare(conn,ins_sql)
            ibm_db.bind_param(stmt,1,fname)
            ibm_db.bind_param(stmt,2,lname)
            ibm_db.bind_param(stmt,3,email)
            ibm_db.bind_param(stmt,4,num)
            ibm_db.bind_param(stmt,5,passwrd)
            ibm_db.bind_param(stmt,6,cpass)

            ibm_db.execute(stmt)

            return render_template("home.html",messge="Successfully SignedUp")


if __name__=="__main__":
    app.run(debug=True)