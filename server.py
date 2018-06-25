from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re


app = Flask(__name__)
mysql = MySQLConnector(app,'emaildb')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app.secret_key = "Toih';g;s;ZC:LKdZ;lkdkj!"

@app.route('/')
def index():
	return render_template('index.html')
	

@app.route('/create_email', methods=['POST'])
def create_email():

	session['email'] = request.form['email']

	if len(session['email']) < 1 and session['email'] != EMAIL_REGEX.match(session['email']):
         flash("Email cannot be blank or email is not in database")
    	else:
	        flash("Success! Welcome!")
	        query = "INSERT INTO users(email, created_at, updated_at)VALUES(:email, NOW(), NOW())"
	        data = {
	        		'email':request.form['email'],
	        }
	        mysql.query_db(query,data)
	        return redirect('/success')
	return redirect('/')

#route cannot be post!
@app.route('/success')
def success():

	query = "SELECT * FROM users"
	users = mysql.query_db(query)

	return render_template('success.html', emails=users)


@app.route('/delete')
def delete():
	query = 'DELETE FROM users WHERE email=email'
	mysql.query_db(query)

	return redirect('/')

	


app.run(debug=True)