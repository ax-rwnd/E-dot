from flask import Blueprint, render_template, abort, request, g, abort
from flask.ext.login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from basket_page import prods_in_basket

account_page = Blueprint('account_page', __name__, template_folder='templates')

def read_order_details(uid):
	db = getattr(g, 'db', None)


	query = "select tbl_order.id, tbl_order.date from tbl_order where tbl_order.customer_id = %s ORDER BY " \
			"tbl_order.id DESC;"

	with db as cursor:
		cursor.execute(query, (uid,))
		return cursor.fetchall()

def set_password(uid, plaintext):
	db = getattr(g, 'db', None)

	query = "update tbl_user set password=%s where tbl_user.id = %s;"
	with db as cursor:
		cursor.execute(query, (generate_password_hash(plaintext),uid))

def get_account_info(uid):
	db = getattr(g, 'db', None)
	with db as cursor:
		query = "select email, name, address, postcode, city, country from tbl_user where id = %s;"
		if cursor.execute(query, (uid,)) > 0:
			return cursor.fetchone()
		else:
			abort (500)

def set_account_info(uid, name, address, postcode, city, country):
	db = getattr(g, 'db', None)
	query = "update tbl_user set name=%s, address=%s, postcode=%s, city=%s, country=%s\
		where tbl_user.id = %s;"

	with db as cursor:
		cursor.execute(query, (name, address, postcode, city, country, uid))
	db.commit()

@account_page.route("/account")
@login_required
def show_account():
	render_template("account.html", user_info = get_account_info(current_user.uid), pagename="Account")
	return render_template("account.html", user_info = get_account_info(current_user.uid), pagename="Account")

def read_order_details_by_id(uid, orderid):
	db = getattr(g, 'db', None)

	query = "select tbl_order.date, \
		sum(tbl_orderlines.amount), sum(tbl_orderlines.price * tbl_orderlines.amount) from tbl_orderlines inner join\
		tbl_order on tbl_orderlines.order_id=tbl_order.id\
		where tbl_order.customer_id = %s and tbl_order.id = %s;"

	with db as cursor:
		cursor.execute(query, (uid,orderid))
		return cursor.fetchone()

def read_product_rows(uid, orderid):
	db = getattr(g, 'db', None)

	query ="SELECT tbl_category.name, tbl_product.id, tbl_product.name, tbl_orderlines.amount, " \
		   "tbl_orderlines.price " \
		   "from tbl_orderlines " \
		   "left join tbl_product on tbl_orderlines.prod_id = tbl_product.id " \
		   "join tbl_order on tbl_orderlines.order_id = tbl_order.id " \
		   "join tbl_category on tbl_product.cat_id = tbl_category.id " \
		   "where tbl_order.id = %s and tbl_order.customer_id = %s;"

	with db as cursor:
		cursor.execute(query, (orderid, uid))
		return cursor.fetchall()


@account_page.route("/account/Orders/<orderid>")
@login_required
def show_orders(orderid):
	product_rows =  read_product_rows(current_user.uid, orderid)
	order_row = read_order_details_by_id(current_user.uid, orderid)
	if not order_row[0]:
		abort(404)
	return render_template("account.html", pagename="Orders", order_id=orderid, product_rows = product_rows,
						   order_row=order_row)

@account_page.route("/account/<pagename>")
@login_required
def show(pagename):
	if pagename =="Orders":
		order_info =  read_order_details(current_user.uid)
		return render_template("account.html", pagename=pagename, order_info=order_info)
	elif pagename == "Account Settings":
		return render_template("account.html", pagename=pagename, user_info = get_account_info(current_user.uid))
	else:
		return render_template("account.html", pagename="Account")

@account_page.route("/account/update_info", methods=["POST"])
@login_required
def show_post():
	if 'update_account' in request.form:
		set_account_info(current_user.uid, request.form['nametext'], request.form['addresstext'], \
						 request.form['postcodetext'], request.form['citytext'], request.form['countrytext'])
		return render_template("account.html", pagename="Account Settings", \
							   user_info = get_account_info(current_user.uid), status = True, \
							   message="Your information was updated.")

	elif 'update_pass' in request.form:
		db = getattr(g, 'db', None)
		query = "select password from tbl_user where id=%s;"
		with db as cursor:
			cursor.execute(query, (current_user.uid,))
			pw = cursor.fetchone()[0]

		if check_password_hash(pw, request.form['pwtext_current']):
			set_password(current_user.uid, request.form['pwtext_new'])
			return render_template("account.html", pagename="Account Settings", \
								   user_info = get_account_info(current_user.uid), status = True, \
								   message="Your password was updated.")
		else:
			return render_template("account.html", pagename="Account Settings", \
								   user_info = get_account_info(current_user.uid), status = False, \
								   message="Wrong password entered.")

	else:
		abort(500)
