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
	query = "select id, email, password from tbl_user WHERE email = (%s);"
	pw = ""

	with db as cursor:
	    cursor.execute(query, email)
	    row = cursor.fetchone()
	    uid = row[0]
	    em = row[1]
	    pw = row[2]
		

	if check_password_hash(pw, password):
	    login_user(User(uid))
	    return render_template("basket.html", message="You have been logged in!", status = False)

	return render_template("login.html", message="Login failed.")

    # try:
    #     # prepare query
    #     name = (request.form['usertext'],)
    #     password = (request.form['pwtext'],)
    #     query = "select (password) from tbl_user where username = (%s);"
    #
    #     with db as cursor:
    #         cursor.execute(query, name)
    #         pw = cursor.fetchone()[0]
    #
    #     if check_password_hash(pw, password[0]):
    #         with db as cursor:
    #             query = "select (id) from tbl_user where username = (%s);"
    #             cursor.execute(query, name)
    #             uid = cursor.fetchall()[0][0]
    #
    #         login_user(User(uid))
    #         return 'You have been logged in! \
		# 	<br/>Follow <a href="/">this</a> link to proceed.'
    # except Exception as e:
    #     print e
    # return 'Login failed.<br/>Follow <a href="/login">this</a> \
		#  link to try again.'
