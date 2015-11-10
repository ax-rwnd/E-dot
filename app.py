import ssl #ssl support
def ready_ssl_context(cert='misc/edot.crt', key='misc/edot.key'):
	context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
	context.load_cert_chain(cert, key)
	return context;

#flask app glue
from flask import Flask, render_template, request, g
from flask.ext.login import LoginManager, UserMixin
from config import config

#blueprint imports
from login_page import login_page
from account_page import account_page
from catalogue_page import catalogue_page
from signup_page import signup_page

## Actually constructs the program!
app = Flask(__name__)
##---------------------------------

##Register Blueprints Here
app.register_blueprint(login_page)
app.register_blueprint(account_page)
app.register_blueprint(catalogue_page)
app.register_blueprint(signup_page)

#DB support
import MySQLdb #sqlite3

#login management support
try:
	#setup login manager
	login_manager = LoginManager()
	login_manager.init_app(app)
	login_manager.user_callback = UserMixin
except Exception as e:
	print e

#returns a database connection for MySQL
def connect_to_database_mysql():
	return MySQLdb.connect(host=config['HOST'], port=config['PORT'], user=config['USER'], passwd=config['PASSWD'], db=config['SQLDB'])

#set this line to define database connection
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
		print "DB was null, DB initialization failure?"

#main website route
@app.route("/")
def main():
	return render_template("index.html")


if __name__ == "__main__":
	context = None if not config['USE_SSL'] else ready_ssl_context()
	app.run(host='192.168.1.6', port=5000, debug=True, ssl_context=context)
		
