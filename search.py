from appdef import *
from flask import Flask, render_template, request, session, url_for, redirect,Response
from flask_mysqldb import MySQL
import MySQLdb.cursors
from fpdf import FPDF
# from init import *
a=randint(0,9999999)
# x=randint(1000, 9999)

@app.route('/search',methods =['GET', 'POST'])  
def search():
  if request.method == 'POST' and 'from' in request.form and 'to' in request.form and 'date' in request.form and 'class' in request.form:
    dept = request.form['from']
    to = request.form['to']
    date=request.form['date']
    clas=request.form['class']
    session['adult']=request.form['adult']
    session['child']=request.form['child']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM airplane WHERE dept = % s and arr = % s and d_date =% s and class= % s ', (dept, to, date, clas, ))
    account = cursor.fetchall()
    if account:
      return render_template('result.html', results=account)
    
  return render_template('book_ticket.html')

@app.route('/checkout',methods =['GET', 'POST'])  
def checkout():
  if request.method == 'POST' and 'f_no' in request.form :
    pid = request.form['f_no']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM airplane WHERE pid = % s ', (pid, ))
    account = cursor.fetchone()
    if account:
      session['loggedin'] = True
      session['pid'] = account['pid']
      session['dept'] = account['dept']
      session['d_date'] = account['d_date']
      session['d_time'] = account['d_time']
      session['arr'] = account['arr']
      session['a_date'] = account['a_date']
      session['a_time'] = account['a_time']
      session['class'] = account['class']
      session['fare'] = account['fare']*int(session['adult'])*(int(session['child'])//2)
      # session['amt']=session['fare']*int(session['adult'])
      # print(session['amt'])
      return render_template('check.html', results=account)
  return render_template('check.html')    


@app.route('/payment', methods =['GET', 'POST'])
def payment():
  uid=session['uid']
  if request.method == 'POST' and 'pid' in request.form and 'from' in request.form and 'to' in request.form and 'd_date' in request.form and 'd_time' in request.form and 'a_date' in request.form and 'a_time' in request.form and 'class' in request.form and 'fare' in request.form :
    pid = request.form['pid']
    dept = request.form['from']
    to = request.form['to']
    d_date = request.form['d_date']
    d_time = request.form['d_time']
    a_date = request.form['a_date']
    a_time = request.form['a_time']
    clas = request.form['class']
    fare = request.form['fare']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO ticket VALUES (% s,% s, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (a, uid, pid, dept, to, d_date, d_time, a_date, a_time, clas, fare,  ))
    mysql.connection.commit()
  return render_template('payment.html')

@app.route('/download/report/pdf')
def download_report():
  
  cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  cursor.execute('select account.username,account.email,ticket.tid,ticket.pid,ticket.dept,ticket.d_date,ticket.d_time,ticket.arr,ticket.a_date,ticket.a_time,ticket.class,ticket.fare from account inner join ticket on account.uid=ticket.uid where ticket.tid= %s',(a, ))
  result = cursor.fetchall()
 
  pdf = FPDF()
  pdf.add_page()
  page_width = pdf.w - 2 * pdf.l_margin
         
  pdf.set_font('Times','B',14.0) 
  pdf.cell(page_width, 0.0, 'Ticket', align='C')
  pdf.ln(10)
 
  pdf.set_font('Courier', '', 12)
         
  col_width = page_width/4
         
  pdf.ln(1)
         
  th = pdf.font_size
         
  for row in result:
    pdf.cell(col_width, th, 'Passenger Name:  ')
    pdf.cell(col_width, th, row['username'])
    pdf.ln()
    pdf.ln()
    pdf.cell(col_width, th, 'Passenger Email:')
    pdf.cell(col_width, th, row['email'])
    pdf.ln()
    pdf.ln()
    pdf.cell(col_width, th, 'Ticket Number:  ')
    pdf.cell(col_width, th, str(row['tid']))
    pdf.ln()
    pdf.ln()
    pdf.cell(col_width, th, 'Flight Number:  ')
    pdf.cell(col_width, th, str(row['pid']))
    pdf.ln()
    pdf.ln()
    pdf.cell(col_width, th, 'Departure:  ')
    pdf.cell(col_width, th, row['dept'])
    pdf.ln()
    pdf.ln()
    pdf.cell(col_width, th, 'Departure Date:  ')
    pdf.cell(col_width, th, row['d_date'])
    pdf.ln()
    pdf.ln()
    pdf.cell(col_width, th, 'Departur Time:  ')
    pdf.cell(col_width, th, row['d_time'])
    pdf.ln()
    pdf.ln()
    pdf.cell(col_width, th, 'Arrival:  ')
    pdf.cell(col_width, th, row['arr'])
    pdf.ln()
    pdf.ln()
    pdf.cell(col_width, th, 'Arrival Date:  ')
    pdf.cell(col_width, th, row['a_date'])
    pdf.ln()
    pdf.ln()
    pdf.cell(col_width, th, 'Arrival Time:  ')
    pdf.cell(col_width, th, row['a_time'])
    pdf.ln()
    pdf.ln()
    pdf.cell(col_width, th, 'Class:  ')
    pdf.cell(col_width, th, row['class'])
    pdf.ln()
    pdf.ln()
    pdf.cell(col_width, th, 'Total Fare:  ')
    pdf.cell(col_width, th, str(row['fare']))
    pdf.ln(th)
    
         
  pdf.ln(10)
         
  pdf.set_font('Times','',10.0) 
  pdf.cell(page_width, 0.0, '- Happy Journey -', align='C')
         
  return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=ticket.pdf'})
# @app.route('/OTP')  
# def OTP():
#     abc = session['email'] 
#     msg = Message('OTP',sender = 'kowshicksrinivasan@gmail.com', recipients = [abc]) 
#     msg.body = str(x)  
#     mail.send(msg)
#     return render_template('payment.html', msg = msg)
 

# a=session['uid']
# @app.route('/abc')
# def hi():
#   print(a)  