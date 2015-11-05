from flask import Blueprint, render_template

catalogue_page = Blueprint('catalogue_page', __name__, template_folder='templates')

@catalogue_page.route("/catalogue")
def show_catalogue():
	#fetch items from catalogue to insert into template
	return render_template("catalogue.html")
