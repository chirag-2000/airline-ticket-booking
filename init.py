#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import pymysql.cursors

from appdef import *
import register
import login
import forget
import search
import history
# import publicinfo
# import customer
# import agent
# import staff
# import purchase

# Understanding Flask static: http://stackoverflow.com/a/28208187
# app = Flask(__name__)

#Define a route to hello function
@app.route('/')
def hello():
  return render_template('landing.html')

@app.route('/logout')
def logout():
  session.pop('username',None)
  session.pop('uid',None)
  session.pop('email',None)
  session.pop('adult',None)
  session.pop('child',None)
  session.pop('pid',None)
  session.pop('dept',None)
  session.pop('d_date',None)
  session.pop('d_time',None)
  session.pop('arr',None)
  session.pop('a_date',None)
  session.pop('a_time',None)
  session.pop('class',None)
  session.pop('fare',None)
  return redirect('/login')

# Why secret_key? http://stackoverflow.com/a/22463969
app.secret_key = 'S4p9Z#Z3vjw!@J66'

#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
  app.run('127.0.0.1', 5000, debug = True)
