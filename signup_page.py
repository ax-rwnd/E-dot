from flask import Blueprint, render_template, request, g
from werkzeug.security import generate_password_hash

signup_page = Blueprint('signup_page', __name__, template_folder='templates')

@signup_page.route("/signup")
def show_signup():
	return render_template("signup.html")


@signup_page.route("/signup", methods=['POST'])
def show_signup_post():
	db = getattr(g, 'db', None)
	#fmt = getattr(g, 'fmt', None)

	#policy check
	def password_policy(pwd):
		if not pwd:
			return False
		elif (len(pwd)<8 or len(pwd)>32):
			return False
		else:
			#TODO: add upper+lower+num check, use regex?
			return True
	
	def email_validation(txt):
		if (-1 == txt.find('@')):
			return False
		elif (-1 == txt.find('.')):
			return False
		else:
			return True

	user = request.form['usertext']
	email = request.form['emailtext']
	passwd = request.form['pwtext']
	repass = request.form['repwtext']

	#validate form
	if not user or len(user)>16:
		return 'Invalid username.<br/>Follow <a href="/signup">this</a> \
			link to try again.'
	elif email and not email_validation(email):
		return 'Invalid e-mail, make sure you\'ve typed it in correctly.<br/> \
			Follow <a href="/signup">this</a> link to try again.'
	elif not password_policy(passwd):
		return 'Invalid password.<br/>Follow <a href="/signup">this</a> \
			link to try again.'
	elif not (passwd == repass):
		return 'The passwords you entered did not match.<br/>Follow \
			<a href="/signup">this</a> link to try again.'
	else:
		cursor = g.db.cursor()
		if email:
			data = (user, generate_password_hash(passwd), email)
		else:
			data = (user, generate_password_hash(passwd))

		cursor.execute ("INSERT INTO tbl_user (username, password"+("" if not email else ", email")+ ") values (%s, %s" + ("" if not email else ", %s")+");", data)
		db.commit()
		return 'Registration okay!'
