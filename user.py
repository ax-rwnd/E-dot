from flask import g
from flask.ext.login import UserMixin, current_user, logout_user

class User (UserMixin):
	def __init__(self, uid=None):
		#load from db if uid specified!
		if not uid==None and not uid==0:
			db = getattr(g, 'db', None)

			with db as cursor:
				data = (uid,)
				query = "select (username) from tbl_user where id = (%s);"
				cursor.execute(query, data)
				username = cursor.fetchone()[0]

			with db as cursor:
				query = "select (email) from tbl_user where id = (%s);"
				if cursor.execute(query, data) > 0:
					email = cursor.fetchone()[0]
				else:
					email = ""

			#create user
			self.email = email
			self.username = username
			self.uid = uid



	@classmethod
	def get (self, uid):
		try:
			return self(uid)
		except UserNotFoundError:
			return None

	def get_id(self):
		return self.uid
