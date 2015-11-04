DATABASE = 'database.db'

from flask import Flask, render_template, g #Web server
import sqlite3 #DB support

app = Flask(__name__)

#returns a dabase connection for sqlite3
def connect_to_database_sqlite3():
	return sqlite3.connect(DATABASE)

#set this line to define database connection
DBFUNC = connect_to_database_sqlite3

@app.before_request
def before_request():
	try:
		g.db = DBFUNC()
	except Exception as e:
		print e

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
	t = ("tbl1",)
	try:
		cur = g.db.execute('SELECT ? FROM tbl1',t)
		print cur.fetchall()
	except Exception as e:
		print e
	return render_template("index.html")

if __name__ == "__main__":
	app.run(host='192.168.1.6')
