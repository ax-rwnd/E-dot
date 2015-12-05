# -*- coding: utf-8 -*-
import os
from flask import Blueprint, request, render_template, g
from config import config
from werkzeug import secure_filename

config['UPLOAD_FOLDER'] = 'static/img'
config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

cms_page = Blueprint('cms_page', __name__, template_folder='templates')

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in config['ALLOWED_EXTENSIONS']

# render catalogue with listed categories
@cms_page.route("/cms/")
def show_cms():
	return render_template("cms.html", editname="")

# render catalogue with product
@cms_page.route("/cms/<editname>")
def show_cms_editor(editname):
	if editname == "Remove Category":
		cats = read_categories()
		return render_template("cms.html", editname=editname, cats = cats)
	elif editname == "Add Product":
		cats = read_categories()
		return render_template("cms.html", editname=editname, cats = cats)
	elif editname == "Remove Product":
		prod = read_products()
		cats = read_categories()
		return render_template("cms.html", editname=editname, cats = cats, prod = prod)

	return render_template("cms.html", editname=editname)

@cms_page.route("/cms/Add Product", methods=['POST'])
def add_product():
	prodname = request.form['prodname']
	prodprice = request.form['prodprice']
	proddesc = request.form['proddesc']
	prodcat = request.form['prodcat']
	prodfile = request.files['prodfile']
	produrl = ""

	existing_products = read_products()
	cats = read_categories()
	if prodname in existing_products:
		return render_template("cms.html", editname = "Add Product", cats = cats, ins = "error")

	if prodfile and allowed_file(prodfile.filename) and not os.path.isfile(config['UPLOAD_FOLDER'] + "/" + prodfile.filename):
		# Make the filename safe, remove unsupported chars
		filename = secure_filename(prodfile.filename)
		prodfile.save(os.path.join(config['UPLOAD_FOLDER'], filename))
		produrl = config['UPLOAD_FOLDER'] + "/" + filename
	else:
		print "Image Upload Error"
	db = getattr(g, 'db', None)
	try:
		query = "INSERT INTO tbl_product (name, description, image_url, price, cat_id) VALUES (%s, %s, %s, %s, (SELECT id from tbl_category WHERE name=%s));"
		with db as cursor:
			data = (prodname, proddesc, produrl, prodprice, prodcat)
			cursor.execute(query, data)
			db.commit()
	except Exception as e:
		print e
	return render_template("cms.html", editname = "Add Product", cats = cats, ins = "success")


@cms_page.route("/cms/Remove Product", methods=['POST'])
def remove_product():
	prodname = (request.form['removeprod'],)
	db = getattr(g, 'db', None)
	url = ""
	query = "SELECT image_url from tbl_product WHERE name = %s"
	with db as cursor:
		cursor.execute(query, prodname)
		url = cursor.fetchone()[0]
		if url:
			os.remove(url)

	query = "DELETE FROM tbl_product WHERE name = %s"
	with db as cursor:
		data = (prodname,)
		cursor.execute(query, data)
		db.commit()

	p = read_products()
	return render_template("cms.html", editname = "Remove Product", prod = p, ins = "success")


@cms_page.route("/cms/Add Category", methods=['POST'])
def add_category():
	catname = (request.form['catname'],)
	cats = read_categories()

	if catname[0] in cats:
		return render_template("cms.html", editname = "Add Category", ins = "error")
	else:
		db = getattr(g, 'db', None)
		query = "insert into tbl_category (name) VALUES (%s);";
		with db as cursor:
			cursor.execute(query, catname)
			db.commit()

	return render_template("cms.html", editname = "Add Category", ins = "success")


@cms_page.route("/cms/Remove Category", methods=['POST'])
def remove_category():
	catname = (request.form['removecat'],)
	db = getattr(g, 'db', None)
	try:
		query = "DELETE FROM tbl_category WHERE name = %s;";
		with db as cursor:
			cursor.execute(query, catname)
			db.commit()
	except Exception as e:
		print e

	cats = read_categories()
	return render_template("cms.html", editname = "Remove Category", cats=cats, ins = "success")

# Read categories fom database and returm them as a list
def read_categories():
	db = getattr(g, 'db', None)
	cursor = db.cursor()
	cursor.execute("select name from tbl_category;")

	cats = []

	for x in cursor:
		cats.append(x[0])

	return cats


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
