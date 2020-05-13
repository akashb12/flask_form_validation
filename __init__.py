from flask import Flask,request,render_template,redirect,url_for,session,logging,flash,send_from_directory
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
import os
from flask_login import login_user, login_required, current_user, logout_user, LoginManager, UserMixin
import random
app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/databasename'
db = SQLAlchemy(app)
# creating content in database same column names should be provided in mysql
class tablename(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String(12), unique=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)
    hashCode = db.Column(db.String(120))


login_manager = LoginManager(app)  
@login_manager.user_loader
def load_user(user_id):
    return tablename.query.get(int(user_id))  
login_manager.login_view = "login"
login_manager.login_message_category = "info"

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if(request.method=='POST'):
        "fetch entry from database"
        # u name is just a variable which is storing name content of form
        uname=request.form.get('uname')
        passw=request.form.get('passw')
        existing_entry=tablename.query.filter_by(email=uname).first()
        if existing_entry:
            flash("Email already exist","danger")
            return redirect(url_for("register"))
        # to add entry
        # email from database will store uname variable and password from database will store passw variable
        new_entry=tablename(email=uname,password=passw)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if(request.method=='POST'):
        "fetch entry from database"
        louname=request.form.get('uname')
        lopassw=request.form.get('passw')
        session['uname']=request.form['uname']
        # now we will compare email from database with loname which stores the login username  ans same for password if this matches then only it will render to nakshoverview
        login=tablename.query.filter_by(email=louname,password=lopassw).first()
        if login is not None:
            return render_template('plcpro.html')
    flash('Please login to submit your queries',"danger")    
    return render_template("login.html")

@app.route("/logout")
def logout():
    if 'uname' in session:
            uname=session['uname']
            logout_user()
            session.pop('uname',None)
            flash('You were logged Out',"success")
            return redirect(url_for('login'))
    else:
           # flash('Please login first',"danger")
            return redirect(url_for('login'))

