from flask import Flask, render_template, Response, request, session, render_template, redirect, url_for
import time
import re
import joblib
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
serverip = s.getsockname()[0]
s.close()

from dbase import db


#Server IP and PORT
Server = serverip
Port = 5000

#instatiate flask app  
app = Flask(__name__, template_folder='./templates')
app.secret_key = '1a2b5ccd7e'
app.config['SESSION_TYPE'] = 'filesystem'

model = joblib.load('SVM_model.pkl')
#pred = model.predict(demand_test)
#print(pred)


dbObj = db

# ******************
# web partion
# ******************
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        con = dbObj.connect()
        qry = "select * from users WHERE username='" + str(username) + "' AND password='" + str(password) + "'"
        users = dbObj.selectQry(con, qry)
        for user in users:
            if len(users) > 0:
                session['loggedin'] = True
                session['userid'] = user['userid']
                session['roleid'] = user['roleid']
                session['username'] = user['username']
                return redirect(url_for('dashboard'))
            else:
                return render_template('index.html', title="Login", msg="Invalid username/password")
    return render_template('index.html', title="Login", msg="")

# This will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        fullName = request.form['fullname']
        email = request.form['email']
        mobile = request.form['mobile']
        natid = request.form['nat_id']
        gender = request.form['gender']
        con = db.connect()

        # Check if account exists using MySQL
        # cursor.execute('SELECT * FROM accounts WHERE username = %s', (username))
        qry = "SELECT * FROM users WHERE username='" + username + "'"
        account = db.selectQry(con, qry)

        # If account exists show error and validation checks
        if len(account) == 1:
            msg = "Account already exists!"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = "Invalid email address!"
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = "Username must contain only characters and numbers!"
        elif not username or not password or not email:
            msg ="Incorrect username/password!"
        else:
        # Account doesnt exists and the form data is valid, now insert new account into accounts table
            qry = "INSERT INTO users (username, password, fullname, email, mobile, nat_id, gender, roleid) "
            qry += " VALUES('" + str(username) + "','" + str(password) + "','" + str(fullName) + "','" + str(email) + "', '" + str(mobile) + "','" + str(natid) + "','" + str(gender) + "','3')"
            db.crudQry(con, qry)
            msg = "You have successfully registered!"
            return redirect(url_for('index'))

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = "Please fill out the form!"
    # Show registration form with message (if any)
    return render_template('register.html',title="Register")

@app.route('/logout')
def logout():
    session["userid"] = ""
    session["loggedin"] = False
    session["roleid"] = ""
    session["username"] = ""
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        con = dbObj.connect()
        qry = "select * from users WHERE roleid='2'"
        users = dbObj.selectQry(con, qry)
        return render_template('dashboard.html', title="Home",  users=users)
    return render_template('index.html', title="Login",  msg="")

@app.route('/profile')
def profile():
    # Check if user is loggedin
    con = db.connect()
    if 'loggedin' in session:
        qry = "SELECT * FROM users WHERE username='" + session['username'] + "'"
        users = db.selectQry(con, qry)
        for user in users:
            account = user
        # User is loggedin show them the home page
        return render_template('profile.html', username=session['username'],title="Profile", account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('/'))

@app.route('/viewreads', methods=['GET', 'POST'])
def viewreads():
    if 'loggedin' in session:
        con = dbObj.connect()
        qry = "SELECT *, FROM_UNIXTIME(readtime, '%Y/%m/%d') readtime FROM bioreads WHERE userid='" + str(session["userid"]) + "'"
        rows = dbObj.selectQry(con, qry)
        return render_template('reads.html', title="Reads",  rows=rows)
    return render_template('index.html', title="Login",  msg="")

@app.route('/newread', methods=['GET', 'POST'])
def newread():
    if 'loggedin' in session:
        if request.method == "POST":
            age = request.form['age'] 
            hrate = request.form['hrate'] 
            temper = request.form['temper'] 
            pressure = request.form['pres'] 
            readtime = int(time.time()) 
            con = dbObj.connect()
            qry = "INSERT INTO bioreads (userid, pressure, heartrate, temper, age, readtime) " 
            qry += " VALUES('" + str(session["userid"]) + "', '" + str(pressure) + "', '" + str(hrate) + "', '" + str(temper) + "', '" + str(age) + "', '" + str(readtime) + "')"
            dbObj.crudQry(con, qry)
            return redirect(url_for('viewreads'))
        return render_template('newread.html', title="Reads")
    return render_template('index.html', title="Login",  msg="")

@app.route('/allpatients')
def allpatients():
    if 'loggedin' in session:
        con = dbObj.connect()
        qry = "select * from users WHERE roleid='3'"
        users = dbObj.selectQry(con, qry)
        return render_template('allpatients.html', title="Patients",  users=users)
    return render_template('index.html', title="Login",  msg="")

@app.route("/saveComment", methods=['GET', 'POST'])
def saveComment():
    readid = request.form['readid']
    comm = request.form['comment']
    con = dbObj.connect()
    qry = "UPDATE bioreads SET doccomment='" + str(comm) + "'  WHERE readid='" + str(readid) + "'"
    dbObj.crudQry(con, qry)
    return "done"
    

@app.route("/addPatient", methods=['GET', 'POST'])
def addPatient():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        email = request.form['email']
        mobile = request.form['mobile']
        nat_id = request.form['nat_id']
        gender = request.form['gender']
        
        con = dbObj.connect()
        qry = "INSERT INTO users (roleid, username, password, fullname, email, mobile, nat_id, gender) "
        qry += " VALUES ('3','" + str(username) + "','" + str(password) + "','" + str(fullname) + "','" + str(email) + "','" + str(mobile) + "','" + str(nat_id) + "','" + str(gender) + "')"
        dbObj.crudQry(con, qry)
        return redirect(url_for('app.allpatients'))
    return render_template('addPatient.html', title="new patient")
   
       
@app.route("/patDetail/<string:userid>", methods=['GET', 'POST'])
def patDetail(userid):
    Gens = {"0":"Female","1":"Male"}
    con = dbObj.connect()
    qry = "select * from users WHERE userid='" + str(userid) + "'"
    rows = dbObj.selectQry(con, qry)
    qry = "SELECT *, FROM_UNIXTIME(readtime, '%Y/%m/%d') readtime FROM bioreads WHERE userid='" + str(userid) + "'"
    reads = dbObj.selectQry(con, qry)
    return render_template('patientDetail.html', title="Login",  rows=rows, reads=reads, Gens=Gens)
   
@app.route("/predicts", methods=['GET', 'POST'])
def predicts():
    # columns = ["Age","Gender","Heart_Rate_bpm","Body_Temperature_C","Blood_Pressure_mmHg","Oxygen_Saturation_%"]
    readid = request.form['readid'] 
    age = request.form['age'] 
    gender = request.form['gender'] 
    hrate = request.form['hrate'] 
    temper = request.form['temper'] 
    pressure = request.form['pres'] 
    diagnosis = ["Flu","Healthy","Bronchitis","Cold","Pneumonia"]
    test = [[age, gender, hrate, temper, pressure, 92]]
    preds = model.predict(test)
    for pred in preds:
        print(diagnosis[pred])
        con = dbObj.connect()
        qry = "UPDATE bioreads SET predicts='" + diagnosis[pred] + "' WHERE readid='" + str(readid) + "'"
        dbObj.crudQry(con, qry)
        return diagnosis[pred]

if __name__ == '__main__':
    app.run(host=Server, port=Port, debug=True)
    

