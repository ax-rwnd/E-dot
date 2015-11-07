DATABASE = 'db_edot'

# mysql
HOST = 'localhost'
PORT = 3306
USER = 'root'
PASSWD = ''
SQLDB = 'db_edot'
from flask import Flask, render_template, request, g
app = Flask(__name__)

# DB support
import sqlite3, MySQLdb

# returns a dabase connection for sqlite3
def connect_to_database_sqlite3():
    return sqlite3.connect(DATABASE)

# returns a database connection for MySQL
def connect_to_database_mysql(database=None):
    if database:
        return MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=database)
    else:
        return MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD)

# set this line to define database connection
DBFUNC = connect_to_database_mysql

tbl_user = "tbl_user"
tbl_product = "tbl_product"
tbl_orderlines = "tbl_orderlines"
tbl_order = "tbl_order"
tbl_category = "tbl_category"

def main():
    print "E-dot commerce database tester...\n"
    add_testdata()
    print_database()  # Removing existing database if it already exists
    print "\nCompleted sucessfully"

def add_testdata():
    db = DBFUNC(SQLDB)
    print "Adding testdata"
    cursor = db.cursor()
    cursor.execute("insert into " + tbl_user + " (username, password, email) VALUES ('kurt', 'pass', 'kurt@live.se');")
    cursor.execute("insert into " + tbl_category + "(name) values ('weapons');")
    cursor.execute("insert into " + tbl_product + "(name, description, image_url, price, cat_id) values ('rock', 'a hard thing', '/images/rock.png', '1337.0', 1);")
    db.commit()
    db.close()

def print_database():
    db = DBFUNC(SQLDB)
    cursor = db.cursor()
    cursor.execute("show tables;")
    numrows = int(cursor.rowcount)
    tables = []
    
    print "Tables found:"
    for x in range(0, numrows):
        row = cursor.fetchone()
        print row[0]
        tables.append(row[0])
        
    print ""
    
    for t in tables:
        cursor.execute("select * from " + t+";") 
        num = int(cursor.rowcount)
        print "Content in table " +  t + ":"
        for x in range(0,num):
            row = cursor.fetchone()
            print row

    db.close()


main()



