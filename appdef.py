from flask import Flask, render_template, request
import pymysql.cursors
import datetime
from flask_mysqldb import MySQL
import MySQLdb.cursors


#Initialize the app from Flask
app = Flask(__name__)

app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '******'
app.config['MYSQL_DB'] = 'airline'
from flask_mail import *  
from random import *  


app.config["MAIL_SERVER"]='smtp.gmail.com'  
'  
app.config["MAIL_PORT"] = 465      
app.config["MAIL_USERNAME"] = 'Your email'  
app.config['MAIL_PASSWORD'] = 'your password'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True  


mysql = MySQL(app)
mail = Mail(app)  
otp = randint(000000,999999)  

def validateDates(begintime, endtime):
    begindate = datetime.datetime.strptime(begintime, '%Y-%m-%dT%H:%M:%S')
    enddate = datetime.datetime.strptime(endtime, '%Y-%m-%dT%H:%M:%S')
    return begindate <= enddate

@app.route('/back')
def back():
    
    return render_template('dash.html')
