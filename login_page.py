from flask import Blueprint, render_template

login_page = Blueprint('login_page', __name__, template_folder='templates')

@login_page.route("/login")
def show_login():
	print "In login!"
	return render_template("catalogue.html")
