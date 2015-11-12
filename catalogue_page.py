from flask import Blueprint, render_template, g
from itertools import product

catalogue_page = Blueprint('catalogue_page', __name__, template_folder='templates')

#render catalogue with listed categories
@catalogue_page.route("/catalogue/")
def show_catalogue_index():
	cats = read_categories()
	return render_template("catalogue.html", catname='Categories', c = cats)

#render catalogue with product
@catalogue_page.route("/catalogue/<catname>")
def show_catalogue(catname):
	products = read_products(catname)
	cats = read_categories()
	return render_template("catalogue.html", catname=catname, c = cats, p = products)

@catalogue_page.route("/catalogue/<catname>/<prodname>")
def show_product(catname, prodname):
	product_info = read_product_info(prodname)
	cats = read_categories()
	return render_template("catalogue.html", catname=catname, c = cats, prod = product_info)

def read_product_info(prodname):
	db = getattr(g, 'db', None)
	cursor = db.cursor()
	query = ("select name, description, price from tbl_product where name = %s;")
	data = (prodname,)
	cursor.execute(query, data)
	
	prod_info = cursor.fetchone()
	
	return prod_info

#Read products from catalogue where catname is correct
def read_products(catname):
	db = getattr(g, 'db', None)
	cursor = db.cursor()
	query = ("select tbl_product.name, description, price from tbl_product join\
		tbl_category on tbl_product.cat_id = tbl_category.id where tbl_category.name = %s;")
	data = (catname,)
	cursor.execute(query, data)
	prod = []
		
	for x in cursor:
		prod.append(x)
	
	return prod

#Read categories fom database and returm them as a list
def read_categories():
	db = getattr(g, 'db', None)
	cursor = db.cursor()
	cursor.execute("select name from tbl_category;")
	
	cats = []
	
	for x in cursor:
		cats.append(x[0])
		
	return cats
