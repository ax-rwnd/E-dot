from flask import Blueprint, render_template, abort, g,request
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

def set_account_info(uid, name, address, postcode, city, country, email = None):
	db = getattr(g, 'db', None)

	data = None

	if email:
		data = (email,name, address, postcode, city, country, uid)
		query = "update tbl_user set email=%s, name=%s, address=%s, postcode=%s, city=%s, country=%s\
			where tbl_user.id = %s;"
	else:
		data = (name, address, postcode, city, country, uid)
		query = "update tbl_user set name=%s, address=%s, postcode=%s, city=%s, country=%s\
			where tbl_user.id = %s;"

	if data:
		with db as cursor:
			cursor.execute(query, data)
		db.commit()


def update_account_info():
	email = request.form['emailtext']
	nametext = request.form['nametext']
	addresstext = request.form['addresstext']
	postcodetext = request.form['postcodetext']
	citytext = request.form['citytext']
	country = request.form['countrytext']

	db = getattr(g, 'db', None)

	try:
		query = ""
		with db as cursor:
			data = (email,)
			query = "SELECT * FROM tbl_user WHERE email=%s;"
			if cursor.execute(query, data) > 0:
				#update all but email
				set_account_info(current_user.uid, nametext, addresstext, postcodetext, citytext,country)
			else:
				#it is ok to update mail
				set_account_info(current_user.uid, nametext, addresstext, postcodetext, citytext,country, email)
	except Exception:
		print "Error..."

	return True


@account_page.route("/account/<pagename>", methods=['POST'])
@login_required
def account_update(pagename):
	status = ""
	message= ""
	if pagename == "Account Settings":
		update_account_info()
		message = "Information Updated!"
		status = "success"

	return render_template("account.html", user_info = get_account_info(current_user.uid), pagename="Account Settings",
						   status=status, message=message)

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