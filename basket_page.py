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
	
"""
Order of transaction:
1. Secure amount in store
2. Create order
3. Remove amount from store
4. Clear basket
"""

#creates an order from the basket of a user
def place_order (uid):
	db = getattr(g, 'db', None)

	with db as cursor:
		#Start transaction
		query = "start transaction;"
		cursor.execute(query)
		
		#create order
		query = "select prod_id, amount from tbl_basketlines where user_id = %s;"
		if cursor.execute(query, (uid,)) <= 0:
			cursor.execute("ROLLBACK;")
			return (False, "No items in basket.");
		else:
			prods = cursor.fetchall() #will contain all products in basket with amount

			
			#check stock amount
			query = "select amount from tbl_stock where product_id = %s;"
			for current in prods:
				if cursor.execute(query, (current[0],)) <= 0:
					cursor.execute("rollback;")
					return (False, 'Product '+current[0]+' is missing from the stock.')
				else:
					line = cursor.fetchone()[0]
					line = 0 if not line else line

					if current[1] > line:
						cursor.execute("ROLLBACK;")
						return (False, "Too few items of id "+str(current[0])+" in stock.");

			#create row in order 
			query = "insert into tbl_order (customer_id, date) values \
				((select id from tbl_user where id=%s), NOW());"
			cursor.execute(query, (uid,))
			last_row = cursor.lastrowid

			#update stock amount
			update_query = "update tbl_stock set amount = amount - %s where product_id = %s and amount > 0;"
			query = "insert into tbl_orderlines (prod_id, order_id, amount) values (\
				(select id from tbl_product where id = %s),\
				(select id from tbl_order where id = %s), \
				%s);"

			#add to order, remove from stock
			for current in prods:
				cursor.execute(query, (current[0], last_row, current[1]))
				cursor.execute(update_query, (current[1], current[0]))

			#remove from basket
			query = "delete from tbl_basketlines where user_id=%s;"
			cursor.execute(query, (uid,))
			
			cursor.execute("commit;")

	return (True, "Your order was placed.")


@basket_page.route("/basket", methods=['POST'])
@login_required
#transact all wares from basket to order
def show_basket_post():
	db = getattr(g, 'db', None)
	suc, resstr = place_order(current_user.uid)
	return render_template("/basket.html", status=suc, message=resstr)



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
