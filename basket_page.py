from flask import Blueprint, render_template, request, g
from flask.ext.login import login_required, current_user

basket_page = Blueprint('basket_page', __name__, template_folder='templates')

#use this to add a product
def add_to_basket(prod_id, user_id):
	db = getattr(g, 'db', None)

	current = amount_in_basket(prod_id, user_id)

	with db as cursor:
		if current == 0:
			query = "insert into tbl_basketlines (user_id, prod_id, amount)\
			values ((select id from tbl_user where id=%s), (select id from tbl_product where id=%s), %s);"
		else:
			query = "insert into tbl_basketlines (user_id, prod_id, amount)\
			values ((select id from tbl_user where id=%s), (select id from tbl_product where id=%s), %s) on duplicate key update amount=VALUES(amount);"
		ne = current + 1L
		data = (user_id, prod_id, ne)
		cursor.execute(query,data)
		db.commit()
	
def amount_in_basket (prod_id, user_id):
	db = getattr(g, 'db', None)
	with db as cursor:
		query = "select amount from tbl_basketlines where user_id = %s and prod_id = %s;" 
		cursor.execute(query, (user_id, prod_id))
		ret = cursor.fetchone()
		if ret:
			amount = ret[0]
		else:
			amount = 0
	return amount
	

@basket_page.route("/basket")
@login_required
def show_basket():
	db = getattr(g, 'db', None)
	orderlist = {} 

	#select all basketed products and amounts for this user
	with db as cursor:
		query = "select prod_id, amount from tbl_basketlines where user_id = %s;"
		data = (current_user.uid,)
		cursor.execute(query,data)
		prods = cursor.fetchall()

	#sample insert into basketlines
	#insert into tbl_basketlines (user_id, prod_id, amount) values ((select id from tbl_user where id=4), (select id from tbl_product where id=1), 1);

	#resolve name, price and amount
	def resolve(tup):
		with db as cursor:
			query = "select name, price, image_url from tbl_product where id = %s;"
			data = (tup[0],)
			cursor.execute(query,data)
			ret = cursor.fetchone()
			return (ret[0], ret[1], tup[1], ret[2])

	return render_template("basket.html", plist = map(resolve, prods))
