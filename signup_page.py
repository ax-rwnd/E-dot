from flask import Blueprint, render_template

signup_page = Blueprint('signup_page', __name__, template_folder='templates')

@signup_page.route("/signup")
def show_signup():
	print "In signup!"
	return render_template("signup.html")
