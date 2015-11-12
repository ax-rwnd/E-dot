from flask import Blueprint, render_template, request, g
from flask.ext.login import login_required, current_user

basket_page = Blueprint('basket_page', __name__, template_folder='templates')

@basket_page.route("/basket")
@login_required
def show_basket():
	db = getattr(g, 'db', None)
	orderlist = {} 
	

	#get orders placed by this user
	with db as cursor:
		query = "select (id) from tbl_order where customer_id = (%s)"
		data = (current_user.uid,)
		cursor.execute(query, data)
		orders = cursor.fetchall()
	
	#user hasn't placed any orders, abort
	if not orders:
		return render_template("basket.html")
	
	#get products associated with orders
	with db as cursor:
		query = "select (prod_id) from tbl_orderlines where order_id = (%s);"

		#handle all orders
		for order in orders:
			data = (order[0],)
			count = cursor.execute(query, data)
			result = cursor.fetchall()

			for prod in result:
				if prod[0] in orderlist:
					orderlist[prod[0]] = orderlist[prod[0]]+1
				else:
					orderlist[prod[0]] = 1

	#object for brevity in template
	class prod:
		pass

	#fetch product descriptions from db
	prodlist = []
	query = "select name, image_url, price from tbl_product where id = (%s);"
	for key, value in orderlist.iteritems():
		data = (value,)
		with db as cursor:
			cursor.execute(query,data)
			res = cursor.fetchone()
			tmp = prod()
			tmp.name = res[0]
			tmp.url = res[1]
			tmp.price = res[2]
			tmp.amount = value
			prodlist += [tmp]
	
	return render_template("basket.html", plist = prodlist)
