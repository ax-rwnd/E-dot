from flask import Blueprint, render_template, abort, g
from flask.ext.login import current_user, login_required

from basket_page import prods_in_basket

account_page = Blueprint('account_page', __name__, template_folder='templates')

def read_order_details(uid):
	db = getattr(g, 'db', None)

	query = "select tbl_order.id, tbl_order.date, tbl_orderlines.prod_id,\
		tbl_orderlines.amount from tbl_order inner join\
		tbl_orderlines on tbl_order.id=tbl_orderlines.order_id\
		where tbl_order.customer_id = %s ORDER BY tbl_order.id DESC;"

	with db as cursor:
		cursor.execute(query, (uid,))
		return cursor.fetchall()
		
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
	#set_account_info(current_user.uid, "Kurt","road","123","gavle","sweden")
	#print get_account_info(current_user.uid)
	render_template("account.html", user_info = get_account_info(current_user.uid), pagename="Account")
	return render_template("account.html", user_info = get_account_info(current_user.uid), pagename="Account")


@account_page.route("/account/<pagename>")
def show(pagename):
	if pagename =="Orders":
		order_info =  read_order_details(current_user.uid)
		return render_template("account.html", pagename=pagename, order_info=order_info)
	elif pagename == "Account Settings":
		return render_template("account.html", pagename=pagename, user_info = get_account_info(current_user.uid))

	return render_template("account.html", pagename="Account")