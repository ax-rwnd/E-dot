# -*- coding: utf-8 -*-
import os
from flask import Blueprint, request, render_template, g
from flask.ext.login import login_required
from config import config
from werkzeug import secure_filename

from admin import perimeter_check

cms_page = Blueprint('cms_page', __name__, template_folder='templates')



# render catalogue with listed categories
@cms_page.route("/cms/")
@login_required
def show_cms():
	perimeter_check("CMSINDEX")
	return render_template("cms.html", editname="Content Management")

# render catalogue with product
@cms_page.route("/cms/<editname>")
@login_required
def show_cms_editor(editname):
	perimeter_check("CMSINDEX")

	if editname == "Add Product":
		perimeter_check("CMSPRODUCT")
		cat_info = read_categories()
		return render_template("cms.html", editname=editname, cat_info = cat_info)
	if editname == "Edit Categories":
		perimeter_check("CMSCATEGORY")
		cat_info = read_categories()
		return render_template("cms.html", editname=editname, cat_info = cat_info)
	if editname == "Edit Products":
		perimeter_check("CMSSTOCK")
		info = read_stock()
		others = read_not_stock()
		cat_info = read_categories()
		return render_template("cms.html", editname=editname, info=info, others=others, cat_info=cat_info)
	if editname == "Remove Category":
		perimeter_check("CMSCATEGORY")
		cat_info = read_categories()
		return render_template("cms.html", editname=editname, cat_info=cat_info)
	if editname == "Remove Product":
		perimeter_check("CMSPRODUCT")
		info =  read_products_and_categories()
		return render_template("cms.html", editname=editname, info=info)

	return render_template("cms.html", editname=editname)

@cms_page.route("/cms/Add Category", methods=['POST'])
@login_required
def add_category():
	perimeter_check("CMSCATEGORY")

	catname = request.form['catname']
	categories = read_categories()

	if catname in categories:
		cat_info = read_categories()
		return render_template("cms.html", editname="Add Category", ins="error")

	db = getattr(g, 'db', None)
	query = "insert into tbl_category (name) VALUES (%s);";
	with db as cursor:
		cursor.execute(query, (catname,))
		db.commit()

	cat_info = read_categories()
	return render_template("cms.html", editname="Add Category", ins="success")

@cms_page.route("/cms/Add Product", methods=['POST'])
@login_required
def add_product():
	perimeter_check("CMSPRODUCT")

	prodname = request.form['prodname']
	prodprice = request.form['prodprice']
	proddesc = request.form['proddesc']
	prodcat = request.form['prodcat']
	prodstock = request.form['prodstock']
	prodfile = request.files['prodfile']
	produrl = ""

	existing_products = read_products()
	cat_info = read_categories()
	if prodname in existing_products:
		return render_template("cms.html", editname = "Add Product", cat_info=cat_info, ins = "error")

	db = getattr(g, 'db', None)
	query = "INSERT INTO tbl_product (name, description,price, cat_id) VALUES (%s, %s, %s, (SELECT id from tbl_category WHERE name=%s));"
	with db as cursor:
		data = (prodname, proddesc, prodprice, prodcat)
		cursor.execute(query, data)
		db.commit()

	query = "INSERT INTO tbl_stock (product_id, amount) VALUES ((SELECT id FROM tbl_product WHERE name = %s), %s);"
	with db as cursor:
		data = (prodname, prodstock)
		cursor.execute(query, data)
		db.commit()


	query = "SELECT id FROM tbl_product WHERE name = %s;"
	id = None
	with db as cursor:
		data = (prodname,)
		cursor.execute(query, data)
		db.commit()
		id = cursor.fetchone()[0]

	#attempt fileupload
	if id:
		filename = str(id) + "_" + secure_filename(prodfile.filename)
		add_file(prodfile, filename)
		produrl = filename


	query = "UPDATE tbl_product SET image_url=%s WHERE id=%s;"
	with db as cursor:
		data = (produrl, id)
		cursor.execute(query, data)
		db.commit()

	return render_template("cms.html", editname = "Add Product", cat_info=cat_info, ins = "success")

@cms_page.route("/cms/Edit Categories", methods=['POST'])
@login_required
def edit_categories():
	perimeter_check("CMSCATEGORY")


	newname = request.form['rename_cat']
	oldname = request.form['old_name']

	cat_info = read_categories()

	if newname in cat_info:
		return render_template("cms.html", editname="Edit Categories", cat_info = cat_info, ins="error")

	db = getattr(g, 'db', None)
	query = "UPDATE tbl_category SET name=%s WHERE name=%s;"

	with db as cursor:
		cursor.execute(query, (newname, oldname))
		db.commit()

	cat_info = read_categories()
	return render_template("cms.html", editname="Edit Categories", cat_info = cat_info, ins="success")


def edit_specific_product(oldname):
	perimeter_check("CMSPRODUCT")

	prodname = request.form['prodname']
	prodprice = request.form['prodprice']
	proddesc = request.form['proddesc']
	prodcat = request.form['prodcat']
	prodstock = request.form['prodstock']
	prodfile = request.files['prodfile']
	produrl = ""

	existing_products = read_products()
	cat_info = read_categories()

	db = getattr(g, 'db', None)

	query = "UPDATE tbl_product SET name=%s, description=%s, price=%s, cat_id=(SELECT id FROM " \
			"tbl_category WHERE tbl_category.name=%s) WHERE name=%s;"
	with db as cursor:
		data = (prodname, proddesc, prodprice,prodcat, oldname)
		cursor.execute(query, data)
		db.commit()

	query = "UPDATE tbl_stock SET amount=%s WHERE product_id=(SELECT id FROM tbl_product WHERE name=%s);"
	with db as cursor:
		data = (prodstock,prodname)
		cursor.execute(query, data)
		db.commit()


	query = "SELECT id, image_url FROM tbl_product WHERE name = %s;"
	id = None
	old_url = ""
	with db as cursor:
		data = (prodname,)
		cursor.execute(query, data)
		db.commit()
		temp = cursor.fetchone()
		id = temp[0]
		old_url = temp[1]


	#attempt fileupload
	if id:
		filename = str(id) + "_" + secure_filename(prodfile.filename)
		if prodfile:
			add_file(prodfile, filename)
			remove_file(old_url)
			produrl = filename
			query = "UPDATE tbl_product SET image_url=%s WHERE id=%s;"
			with db as cursor:
				data = (produrl, id)
				cursor.execute(query, data)
				db.commit()

	return render_template("cms.html", editname = "Add Product", cat_info=cat_info, ins = "success")


@cms_page.route("/cms/Edit Products", methods=['POST'])
@login_required
def edit_products():
	perimeter_check("CMSPRODUCT")

	alt = request.form['edit']

	if alt == "edit_prod":
		oldname = request.form['old_name']
		edit_specific_product(oldname)
		info = read_stock()
		others = read_not_stock()
		return render_template("cms.html", editname="Edit Products", info=info, others=others, ins = "success")

	unchecked = read_products()
	checked = []

	for p in unchecked:
		try:
			temp = request.form["check_" + p]
			checked.append(temp)
		except Exception:
			pass

	for p in checked:
		if p in unchecked:
			unchecked.remove(p)

	if alt == "set_unavaliable":
		for p in unchecked:
			remove_from_stock(p)
		for p in checked:
			stock_value = request.form["stock_" + p]
			add_to_stock(p, stock_value);
	elif alt == "set_avaliable":
		for p in checked:
			stock_value = request.form["stock_" + p]
			add_to_stock(p, stock_value);

	info = read_stock()
	others = read_not_stock()
	return render_template("cms.html", editname="Edit Products", info=info, others=others, ins = "success")

@cms_page.route("/cms/Remove Category", methods=['POST'])
@login_required
def remove_category():
	perimeter_check("CMSCATEGORY")

	cats = read_categories()
	to_remove = []
	status = "error"

	for c in cats:
		try:
			temp = request.form[c]
			to_remove.append(temp)
		except Exception:
			pass

	for c in to_remove:
		if category_remover(c):
			status = "success"
		else:
			status = "error"


	cat_info = read_categories()
	return render_template("cms.html", editname = "Remove Category", ins = status, cat_info=cat_info)

def category_remover(catname):
	db = getattr(g, 'db', None)
	query = "DELETE FROM tbl_category WHERE name = %s;";
	try:
		with db as cursor:
			cursor.execute(query, catname)
			db.commit()
		return True
	except Exception:
		return False

@cms_page.route("/cms/Remove Product", methods=['POST'])
@login_required
def remove_product():
	perimeter_check("CMSPRODUCT")

	prods = read_products()
	to_remove = []
	for p in prods:
		try:
			temp = request.form[p]
			to_remove.append(temp)
		except Exception:
			pass

	for p in to_remove:
		product_remover(p)

	info = read_products_and_categories()
	return render_template("cms.html", editname = "Remove Product", info=info, ins = "success")

def product_remover(prodname):
	db = getattr(g, 'db', None)

	query = "DELETE FROM tbl_stock WHERE product_id = (SELECT id FROM tbl_product WHERE name = %s);"
	with db as cursor:
		cursor.execute(query, (prodname,))
		db.commit()

	url = ""
	query = "SELECT image_url from tbl_product WHERE name = %s;"
	with db as cursor:
		cursor.execute(query, (prodname,))
		url = cursor.fetchone()[0]
		db.commit()

	if url != config['DEFAULT_IMAGE']:
		remove_file(url)

	query = "DELETE FROM tbl_product WHERE name = %s;"
	with db as cursor:
		cursor.execute(query, (prodname,))
		db.commit()

def search_product(name):
	info = []
	db = getattr(g, 'db', None)
	cursor = db.cursor()

	query = "select tbl_category.name, tbl_product.name, tbl_product.price, " \
			"tbl_product.description, tbl_product.image_url " \
			"from tbl_product " \
			"inner join tbl_category on tbl_category.id = tbl_product.cat_id " \
			"where tbl_product.name = %s;"
	cursor.execute(query, (name,))

	for x in cursor.fetchall():
		info.append(x)
	return info


#Read all products that are in stock.
def read_stock():
	info = []
	db = getattr(g, 'db', None)
	cursor = db.cursor()

	query = "select tbl_category.name, tbl_product.name, tbl_stock.amount, tbl_product.price, " \
			"tbl_product.description, tbl_product.image_url " \
			 "from tbl_product " \
			 "inner join tbl_stock on tbl_product.id = tbl_stock.product_id " \
			 "inner join tbl_category on tbl_category.id = tbl_product.cat_id;"
	cursor.execute(query)

	for x in cursor.fetchall():
		info.append(x)
	return info

def read_not_stock():
	info = []
	db = getattr(g, 'db', None)
	cursor = db.cursor()
	query = "SELECT tbl_category.name, tbl_product.name " \
			"FROM tbl_product " \
			"inner join tbl_category on tbl_category.id = tbl_product.cat_id " \
			"WHERE tbl_product.id NOT IN (SELECT tbl_stock.product_id " \
			"FROM tbl_stock);"
	cursor.execute(query)
	for x in cursor.fetchall():
		print x
		info.append(x)

	return info


# Read categories fom database and returm them as a list
def read_categories():
	db = getattr(g, 'db', None)
	cursor = db.cursor()
	cursor.execute("select name from tbl_category ORDER BY name;")
	categories = []

	for c in cursor:
		categories.append(c[0])
	return categories

#Read products from catalogue where catname is correct
def read_products_and_categories():
	db = getattr(g, 'db', None)
	cursor = db.cursor()
	query = "select tbl_category.name, tbl_product.name " \
			"from tbl_product " \
			"inner join tbl_category on tbl_category.id = tbl_product.cat_id;"
	cursor.execute(query)
	prod = []

	for x in cursor.fetchall():
		prod.append(x)

	return prod

#Read products from catalogue where catname is correct
def read_products():
	db = getattr(g, 'db', None)
	cursor = db.cursor()
	query = "select name from tbl_product;"
	cursor.execute(query)
	prod = []

	for x in cursor.fetchall():
		prod.append(x[0])

	return prod


def remove_from_stock(product):
	db = getattr(g, 'db', None)
	query = "DELETE FROM tbl_stock WHERE product_id = (SELECT id FROM tbl_product WHERE name = %s);"
	with db as cursor:
		cursor.execute(query, (product,))
		db.commit()

def add_to_stock(product, stock_value):
	db = getattr(g, 'db', None)
	query = "INSERT INTO tbl_stock (product_id, amount) VALUES " \
			"((SELECT id FROM tbl_product WHERE name = %s), %s) " \
			"ON DUPLICATE KEY UPDATE amount = %s ;"
	with db as cursor:
		data = (product, stock_value, stock_value)
		cursor.execute(query, data)
		db.commit()

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in config['ALLOWED_EXTENSIONS']


def remove_file(filename):
	url = get_os_string(filename)
	if filename and os.path.isfile(url):
		os.remove(url)

def add_file(prodfile, filename):
	url = get_os_string(filename)
	if prodfile and allowed_file(prodfile.filename) and not os.path.isfile(url):
		prodfile.save(url)
		return True
	else:
		return False


def get_os_string(filename):
	return os.path.dirname(os.path.realpath(__file__)) + config['UPLOAD_FOLDER'] + filename
