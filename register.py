from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import MySQLdb.cursors
from appdef import app,mysql
import random
a=random.randint(1,21)*5
@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form and 'address' in request.form and 'mobile' in request.form and 'gender' in request.form :
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		address = request.form['address']
		mobile = request.form['mobile']
		gender = request.form['gender']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('INSERT INTO account VALUES (% s, % s, % s, % s,% s,% s,% s)', (a, username, email, password, address, mobile, gender, ))
		mysql.connection.commit()
		msg = 'You have successfully registered !'
		return render_template('index.html', msg = msg)
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('reg (1).html', msg = msg)
