# -*- coding: utf-8 -*-
from _mysql_exceptions import IntegrityError
from flask import Blueprint, render_template, request, g
from flask.ext.login import current_user, login_required
from itertools import product
from config import config

from basket_page import add_to_basket, prods_in_basket

catalogue_page = Blueprint('catalogue_page', __name__, template_folder='templates')

#render catalogue with listed categories
@catalogue_page.route("/catalogue/")
def show_catalogue_index():
	cats = read_categories()
	numbasket = prods_in_basket(current_user.get_id())
	return render_template("catalogue.html", catname='Categories', c = cats, numbasket=numbasket)

#render catalogue with product
@catalogue_page.route("/catalogue/<catname>")
def show_catalogue(catname):
	products = read_products(catname)
	cats = read_categories()
	numbasket = prods_in_basket(current_user.get_id())
	return render_template("catalogue.html", catname=catname, c = cats, p = products, numbasket=numbasket)

@catalogue_page.route("/catalogue/<catname>/<prodid>")
def show_product(catname, prodid):
	product_info = read_product_info(prodid)
	cats = read_categories()
	numbasket = prods_in_basket(current_user.get_id())
	return render_template("catalogue.html", rating = read_score(prodid), comments=read_comments(prodid),
						   catname=catname, prodid=prodid, c = cats, prod = product_info, numbasket=numbasket)

#set user vote
def vote (uid, pid, mod):
	db = getattr(g, 'db', None)
	
	with db as cursor:
		query = "insert into tbl_rating (user_id, prod_id, score) values\
			( (select id from tbl_user where id = %s),\
			(select id from tbl_product where id = %s), %s)\
			on duplicate key update score=VALUES(score);"
		cursor.execute(query, (uid, pid, mod))

def post_comment (uid, pid, comment):
	db = getattr(g, 'db', None)

	with db as cursor:
		query = "insert into tbl_review (user_id, prod_id, comment, commentdate) values\
			( (select id from tbl_user where id = %s),\
			(select id from tbl_product where id = %s), %s, NOW()) on duplicate key update comment=values(comment), " \
				"commentdate=NOW();"
		cursor.execute(query, (uid, pid, comment))
		db.commit()

def read_comments (pid):
	db = getattr(g, 'db', None)
	
	with db as cursor:
		query = "select user_id, commentdate, comment from tbl_review where prod_id = %s order by commentdate desc;"
		cursor.execute(query, (pid,))
		return cursor.fetchall()

def read_score (pid):
	db = getattr(g, 'db', None)
	with db as cursor:
		query = "select sum(score) as totalscore from tbl_rating where prod_id = %s;"
		cursor.execute(query, (pid,))
		return cursor.fetchone()[0]

@catalogue_page.route("/catalogue/<catname>/<prodid>", methods=['POST'])
@login_required
def show_product_post(catname, prodid):
	message = ""
	status = ""
	if 'send' in request.form:
		if add_to_basket(prodid, current_user.uid):
			status = "success"
			message = "Product Added To Basket!"
	elif 'post_comment' in request.form:
		try:
			post_comment(current_user.uid, prodid, request.form['comment_text'])
			message = "You Commented!"
			status = "success"
		except IntegrityError:
			message = "You have already commented."
			status = "error"
	elif 'vote_up' in request.form:
		vote(current_user.uid, prodid, 1)	
		message = 'You voted up!'
		status = "success"
	elif 'vote_down' in request.form:
		vote(current_user.uid, prodid, -1)	
		message = 'You voted down.'
		status = "success"
	else:
		abort(500)

	product_info = read_product_info(prodid)
	cats = read_categories()
	numbasket = prods_in_basket(current_user.get_id())
	return render_template("catalogue.html", rating = read_score(prodid), comments=read_comments(prodid),
						   catname=catname, prodid=prodid, c = cats, prod = product_info, status=status,
						   message=message, numbasket=numbasket)

def read_product_info(prodid):
	
	db = getattr(g, 'db', None)
	cursor = db.cursor()
	query = ("SELECT tbl_product.name, tbl_product.description, tbl_product.price, tbl_product.image_url, "
			 "tbl_stock.amount FROM tbl_product "
			 "inner join tbl_stock on tbl_product.id = tbl_stock.product_id where tbl_product.id = %s;")
	data = (prodid,)
	cursor.execute(query, data)
	
	prod_info = list(cursor.fetchone())

	prod_info[3] = config['UPLOAD_FOLDER'] + prod_info[3]

	return prod_info

#Read products from catalogue where catname is correct
def read_products(catname):
	db = getattr(g, 'db', None)
	cursor = db.cursor()
	query = ("select tbl_product.id, tbl_product.name, tbl_product.description, tbl_product.price, "
			 "tbl_product.image_url,tbl_stock.amount from tbl_product "
			 "join "
			 "tbl_stock "
			 "on tbl_product.id = tbl_stock.product_id join\
		tbl_category on tbl_product.cat_id = tbl_category.id where tbl_category.name = %s;")
	data = (catname,)
	cursor.execute(query, data)
	prod = []
		
	for x in cursor:
		x = list(x)
		x[4] = config['UPLOAD_FOLDER'] + x[4]
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