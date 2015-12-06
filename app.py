# -*- coding: utf-8 -*-
#flask app glue
from flask import Flask, render_template, request, g
from flask.ext.login import LoginManager, UserMixin, current_user
from config import config

#for user session management
from user import  User

#blueprint imports
from login_page import login_page, logout_page
from account_page import account_page
from catalogue_page import catalogue_page
from signup_page import signup_page
from basket_page import basket_page
from cms_page import cms_page

from basket_page import prods_in_basket

#DB support
import MySQLdb

#ssl support
import ssl 

# Initiate flask 'app'
app = Flask(__name__)
app.secret_key = config['HOSTKEY']

##Register Blueprints Here
app.register_blueprint(login_page)
app.register_blueprint(account_page)
app.register_blueprint(catalogue_page)
app.register_blueprint(signup_page)
app.register_blueprint(basket_page)
app.register_blueprint(cms_page)

#login management support
try:
	#setup login manager
	login_manager = LoginManager()
	login_manager.init_app(app)
except Exception as e:
	print e

@login_manager.user_loader
def load_user(userid):
	return User(userid)

#returns a database connection for MySQL
def connect_to_database_mysql():
	return MySQLdb.connect(host=config['HOST'], port=config['PORT'],\
	user=config['USER'], passwd=config['PASSWD'], db=config['SQLDB'], charset=config['CHARSET'])

DBFUNC = connect_to_database_mysql

##Setup DB connection
@app.before_request
def before_request():
	try:
		#setup DB
		g.db = DBFUNC()
	except Exception as e:
		print e

##Kill DB connection
@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()
	else:
		print "DB was null!"

#main website route
@app.route("/")
def main():
	#Make check if user is logged in???
	numbasket = prods_in_basket(current_user.get_id())
	return render_template("index.html", numbasket=numbasket)

@app.errorhandler(401)
def unauthorized(e):
	return render_template("/login.html", status = False, message = "You must be logged in to do that.")

@app.errorhandler(404)
def forbidden(e):
	return render_template("/index.html", status = False, message = "That page didn't exists.")


#setup ssl context
def ready_ssl_context(cert='misc/edot.crt', key='misc/edot.key'):
	context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
	context.load_cert_chain(cert, key)
	return context;

#start server
if __name__ == "__main__":
	context = None if not config['USE_SSL'] else ready_ssl_context()
	app.run(host=config['HOSTIP'], port=config['HOSTPORT'],\
		debug=config['HOSTDBG'], ssl_context=context)
		
