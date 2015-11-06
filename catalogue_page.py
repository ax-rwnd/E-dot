from flask import Blueprint, render_template

catalogue_page = Blueprint('catalogue_page', __name__, template_folder='templates')

#render catalogue with listed categories
@catalogue_page.route("/catalogue/")
def show_catalogue_index():
	return render_template("catalogue.html", catname='Categories')

#render catalogue with product
@catalogue_page.route("/catalogue/<catname>")
def show_catalogue(catname):
	return render_template("catalogue.html", catname=catname)
