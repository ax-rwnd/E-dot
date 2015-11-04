from flask import Blueprint, render_template

account_page = Blueprint('account_page', __name__, template_folder='templates')

@account_page.route("/account")
def show_account():
	print "In account!"
	return render_template("account.html")
