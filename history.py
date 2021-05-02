from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
from appdef import *
#import pymysql.cursors
#from index import *
#Define route for login
#@app.route('/login')
@app.route('/history')  
def history():
  uid = session['uid']
  # print('uid:',uid)
  cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  cursor.execute('SELECT * FROM ticket WHERE uid = % s ', (uid, ))
  account = cursor.fetchall()
  if account:
    return render_template('history.html', results=account)
  return render_template('history.html')