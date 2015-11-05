from flask import Blueprint, render_template, request

login_page = Blueprint('login_page', __name__, template_folder='templates')

@login_page.route("/login", methods=['GET', 'POST'])
def show_login():
	if request.method == 'POST':
		print "In post!"
	return render_template("login.html")
