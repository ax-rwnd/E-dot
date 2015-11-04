#sqlite3
DATABASE = 'database.db'

#mysql
HOST='localhost'
PORT=3306
USER='axel'
PASSWD='bollboll'
SQLDB='edot'

from flask import Flask, render_template, request, g
import sqlite3, MySQLdb #DB support

#child pages
from login_page import login_page
from account_page import account_page
from catalogue_page import catalogue_page
from signup_page import signup_page


app = Flask(__name__)


##Register Blueprints Here
app.register_blueprint(login_page)
app.register_blueprint(account_page)
app.register_blueprint(catalogue_page)
app.register_blueprint(signup_page)

#returns a dabase connection for sqlite3
def connect_to_database_sqlite3():
	return sqlite3.connect(DATABASE)

#returns a database connection for MySQL
def connect_to_database_mysql():
	return MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=SQLDB)

#set this line to define database connection
DBFUNC = connect_to_database_sqlite3

##Setup DB connection
@app.before_request
def before_request():
	try:
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

@app.route("/")
def main():
	return render_template("index.html")


if __name__ == "__main__":
	app.run(host='192.168.1.6', port=5000)
