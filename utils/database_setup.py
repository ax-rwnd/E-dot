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
def connect_to_database_sqlite3(database):
    return sqlite3.connect(database)

# returns a database connection for MySQL
def connect_to_database_mysql(database=None):
    if database:
        return MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=database)
    else:
        return MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD)

# set this line to define database connection
DBFUNC = connect_to_database_mysql
#DBFUNC = connect_to_database_sqlite3

tbl_user = "tbl_user"
tbl_product = "tbl_product"
tbl_orderlines = "tbl_orderlines"
tbl_order = "tbl_order"
tbl_category = "tbl_category"

def main():
    print "E-dot commerce database script starting..."
    remove_db()  # Removing existing database if it already exists
    create_db()  # Create database to work on

    # Set up all tables
    create_user_tbl()
    create_category_tbl()
    create_product_tbl()
    create_order_tbl()
    create_orderlines_tbl()
    
    print "Completed sucessfully"
        
def create_category_tbl():
    db = DBFUNC(SQLDB)
    cursor = db.cursor()
    print "Creating table", tbl_category
    query = "create table " + tbl_category + "(id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY, name VARCHAR(32));"
    cursor.execute(query)
    db.close()

def create_product_tbl():
    db = DBFUNC(SQLDB)
    cursor = db.cursor()
    print "Creating table", tbl_product
    query = "create table " + tbl_product + " (id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY, name VARCHAR(45), description VARCHAR(256), image_url VARCHAR(128), price DECIMAL(6,2), cat_id INT(11) UNSIGNED);"
    cursor.execute(query)
    
    query = "alter table " + tbl_product+" add CONSTRAINT fk_cat FOREIGN KEY (cat_id) REFERENCES "+tbl_category+"(id);"
    cursor.execute(query)
    db.close()

def create_orderlines_tbl():
    db = DBFUNC(SQLDB)
    cursor = db.cursor()
    print "Creating table", tbl_orderlines
    query = "create table "+ tbl_orderlines +" (prod_id INT(11) UNSIGNED, order_id INT(11) UNSIGNED);"
    cursor.execute(query)
    
    query = "alter table "+tbl_orderlines+" add CONSTRAINT fk_prod FOREIGN KEY (prod_id) REFERENCES "+tbl_product+"(id);"
    cursor.execute(query)
    
    query = "alter table "+tbl_orderlines +" add CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES "+tbl_order+"(id);"
    cursor.execute(query)
    db.close()

def create_order_tbl():
    db = DBFUNC(SQLDB)
    cursor = db.cursor()
    print "Creating table", tbl_order
    query = "create table "+ tbl_order+" (id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY, customer_id INT(11), date DATE);"
    cursor.execute(query)
    query = "alter table "+ tbl_order+" add CONSTRAINT customer_id FOREIGN KEY (id) REFERENCES "+tbl_user+"(id);"
    cursor.execute(query)
    db.close()

def create_user_tbl():
    db = DBFUNC(SQLDB)
    cursor = db.cursor()
    print "Creating table", tbl_user
    query = "create table "+ tbl_user+" (id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY, username VARCHAR(16), password VARCHAR(128), email VARCHAR(32));"
    cursor.execute(query)
    db.close()

def create_db():
    db = DBFUNC()
    cursor = db.cursor()
    print "Creating database", DATABASE
    query = "create database " + DATABASE + ";"
    cursor.execute(query)
    db.close()

def remove_db():
    db = DBFUNC()
    cursor = db.cursor()
    cursor.execute("show databases;")
    numrows = int(cursor.rowcount)

    for x in range(0, numrows):
        row = cursor.fetchone()
        if row[0] == DATABASE:
            print "Removing database", DATABASE
            query = "drop database " + DATABASE + ";"
            cursor.execute(query)
            break

    db.close()


main()


