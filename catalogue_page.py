# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, g
from flask.ext.login import current_user
from itertools import product

from basket_page import add_to_basket

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

@catalogue_page.route("/catalogue/<catname>/<prodid>")
def show_product(catname, prodid):
	product_info = read_product_info(prodid)
	cats = read_categories()
	return render_template("catalogue.html", catname=catname, prodid=prodid, c = cats, prod = product_info)

@catalogue_page.route("/catalogue/<catname>/<prodid>", methods=['POST'])
def show_product_post(catname, prodid):
	if request.method == 'POST' and current_user.is_authenticated:
		return add_to_basket(prodid, current_user.uid)
	else:
		abort(403)

def read_product_info(prodid):
	db = getattr(g, 'db', None)
	cursor = db.cursor()
	query = ("select name, description, price, image_url from tbl_product where id = %s;")
	data = (prodid,)
	cursor.execute(query, data)
	
	prod_info = cursor.fetchone()
	
	return prod_info

#Read products from catalogue where catname is correct
def read_products(catname):
	db = getattr(g, 'db', None)
	cursor = db.cursor()
	query = ("select tbl_product.id, tbl_product.name, description, price, image_url from tbl_product join\
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
