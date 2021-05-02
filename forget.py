from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
from flask_mail import *
import MySQLdb.cursors
from appdef import app,mysql,otp,mail
# @app.route('/')  
# def index():  
#     return render_template("forget.html")  
 
@app.route('/forget',methods = ['GET', 'POST'])  
def forget():
  if request.method == 'POST' and 'email' in request.form:
    email = request.form['email']
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM account WHERE email = % s ', (email, ))
    account = cursor.fetchone()
    if account:
      session['email'] = account['email']
      msg = Message('OTP',sender = 'kowshicksrinivasan@gmail.com', recipients = [email]) 
      msg.body = str(otp)  
      mail.send(msg)
      return render_template('verify.html', msg = msg)
  return render_template('forget.html') 

 
@app.route('/verify',methods=["POST"])  
def verify():  
    user_otp = request.form['otp']  
    if otp == int(user_otp):  
        return render_template('forget2.html')  
    return "<h3>failure</h3>" 

@app.route('/update',methods=["POST"])
def update():
  if request.method == 'POST' and 'password' in request.form :
    email=session['email']
    password = request.form['password']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('update account set password =% s where email=% s',(password, email, ))
    mysql.connection.commit()
    msg = 'You have successfully registered !'
    return render_template('login.html',msg=msg)
  session.pop('email')  
  return render_template('forget.html')