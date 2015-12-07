from flask import g
from flask.ext.login import UserMixin, current_user, logout_user

from basket_page import prods_in_basket

class User (UserMixin):
	def __init__(self, uid=None):
		#load from db if uid specified!
		if not uid==None and not uid==0:
			db = getattr(g, 'db', None)

			with db as cursor:
				data = (uid,)
				query = "select (name) from tbl_user where id = (%s);"
				cursor.execute(query, data)
				name = cursor.fetchone()[0]

			with db as cursor:
				query = "select (email) from tbl_user where id = (%s);"
				if cursor.execute(query, data) > 0:
					email = cursor.fetchone()[0]
				else:
					email = ""


			#create user
			self.email = email
			self.name = name
			self.uid = uid
			self.numbasket = prods_in_basket(uid)


			print "initierar"



	@classmethod
	def get (self, uid):
		try:
			return self(uid)
		except UserNotFoundError:
			return None

	def get_id(self):
		return self.uid
