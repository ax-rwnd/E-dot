from flask import Blueprint, render_template

catalogue_page = Blueprint('catalogue_page', __name__, template_folder='templates')

@catalogue_page.route("/catalogue")
def show_catalogue():
	print "In catalogue!"
	return render_template("catalogue.html")
