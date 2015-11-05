from flask import Blueprint, render_template, request, g

signup_page = Blueprint('signup_page', __name__, template_folder='templates')

@signup_page.route("/signup")
def show_signup():
	return render_template("signup.html")


@signup_page.route("/signup", methods=['POST'])
def show_signup_post():
	db = getattr(g, 'db', None)
	cursor = db.cursor()

	#automated policy check
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

	#validate form
	if not request.form['usertext'] or len(request.form['usertext'])>16:
		return 'Invalid username.<br/>Follow <a href="/signup">this</a> \
			link to try again.'
	elif request.form['emailtext'] and not email_validation(request.form['emailtext']):
		return 'Invalid e-mail, make sure you\'ve typed it in correctly.<br/> \
			Follow <a href="/signup">this</a> link to try again.'
	elif not password_policy(request.form['pwtext']):
		return 'Invalid password.<br/>Follow <a href="/signup">this</a> \
			link to try again.'
	elif not (request.form['pwtext'] == request.form['repwtext']):
		return 'The passwords you entered did not match.<br/>Follow \
			<a href="/signup">this</a> link to try again.'
	else:
		#TODO: add real behavior here!
		return 'Registration okay!'
