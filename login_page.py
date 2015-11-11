from flask import Blueprint, render_template, request, g
from werkzeug.security import check_password_hash, generate_password_hash
from flask.ext.login import LoginManager, login_user, current_user
from user import User

login_page = Blueprint('login_page', __name__, template_folder='templates')

@login_page.route("/login")
def show_login():
	if current_user.is_authenticated:
		return "You're already authenticated"
	return render_template("login.html")

@login_page.route("/login", methods=['POST'])
def show_login_post():
	print current_user.is_authenticated
	db = getattr(g, 'db', None)
	cursor = db.cursor()

	#prepare query
	name = (request.form['usertext'],)
	password = (request.form['pwtext'],)
	query = "select (password) from tbl_user where username = (%s);"

	try :
		if cursor.execute(query,name)>0:		
			if check_password_hash(cursor.fetchone()[0], password[0]):
				login_user(User().init(name))
				return 'You have been logged in! \
				<br/>Follow <a href="/">this</a> link to proceed.'
	except Exception as e:
		print e
	
	return 'Login failed.<br/>Follow <a href="/login">this</a> \
		 link to try again.'
