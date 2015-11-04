#sqlite3
DATABASE = 'database.db'

#mysql
HOST=''
PORT=''
USER=''
PASSWD=''
SQLDB=''

from flask import Flask, render_template, request, g #Web server
import sqlite3, MySQLdb #DB support

app = Flask(__name__)

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
		print "DB was null!"

#main page
@app.route("/")
def main():
	t = ("*",)
	try:
		cur = g.db.execute('SELECT * FROM tbl1')
		print cur.fetchall()
	except Exception as e:
		print e
	return render_template("index.html")

@app.route("/home")
def home():
	try:
		print request.args.get('username') 
	except Exception as e:
		print e
	return render_template("index.html")

if __name__ == "__main__":
	app.run(host='192.168.1.6', port=5000)
