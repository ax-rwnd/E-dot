from flask import Blueprint, render_template, request, g
from werkzeug.security import check_password_hash, generate_password_hash

login_page = Blueprint('login_page', __name__, template_folder='templates')

@login_page.route("/login")
def show_login():
	return render_template("login.html")

@login_page.route("/login", methods=['POST'])
def show_login_post():
	db = getattr(g, 'db', None)
	cursor = db.cursor()

	#prepare query
	name = (request.form['usertext'],)
	password = (request.form['pwtext'],)
	query = "select (password) from user where username = ("+g.fmt+");"

	try :
		if cursor.execute(query,name)>0:		
			if check_password_hash(cursor.fetchone()[0], password[0]):
				return 'You have been logged in! \
				<br/>Follow <a href="/">this</a> link to proceed.'
	except Exception as e:
		print e
	
	return 'Login failed.<br/>Follow <a href="/login">this</a> \
		 link to try again.'
