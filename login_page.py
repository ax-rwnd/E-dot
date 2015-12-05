from flask import Blueprint, render_template, request, g
from werkzeug.security import check_password_hash, generate_password_hash
from flask.ext.login import LoginManager, login_user, logout_user, current_user
from user import User

login_page = Blueprint('login_page', __name__, template_folder='templates')
logout_page = Blueprint('logout_page', __name__, template_folder='templates')


@login_page.route("/login")
def show_login():
	# determine whether the user is logged in or not
	if current_user.is_authenticated:
		return "You're already authenticated, user " \
			   + str(current_user.get_id()) + "."

	return render_template("login.html")


@login_page.route("/logout")
def show_logout():
	logout_user()
	return render_template("index.html", message="You have been logged out.", status = True)


# main login routine
@login_page.route("/login", methods=['POST'])
def show_login_post():
	db = getattr(g, 'db', None)

	email = (request.form['emailtext'],)
	password = request.form['pwtext']

	query = "select id, password from tbl_user WHERE email = (%s);"
	with db as cursor:
		if cursor.execute(query, email) <= 0:
			return render_template("login.html", message="Invalid e-mail or password.")
		else:
			row = cursor.fetchone()
			uid = row[0]
			pw = row[1]

	if check_password_hash(pw, password):
		login_user(User(uid))
		return render_template("/index.html", message="You have been logged in!", status = True)
	else:
		 return render_template("/login.html", message="Invalid e-mail or password.")
