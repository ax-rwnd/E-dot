from util_config import config
from flask import Flask, render_template, request, g
app = Flask(__name__)

# DB support
import MySQLdb

# returns a database connection for MySQL
def connect_to_database_mysql(database=None):
    if database:
		return MySQLdb.connect(host=config['HOST'], port=config['PORT'],\
		user=config['USER'], passwd=config['PASSWD'], db=config['SQLDB'])
    else:
		return MySQLdb.connect(host=config['HOST'], port=config['PORT'],\
		user=config['USER'], passwd=config['PASSWD'])

# set this line to define database connection
DBFUNC = connect_to_database_mysql

tbl_user = "tbl_user"
tbl_product = "tbl_product"
tbl_orderlines = "tbl_orderlines"
tbl_basketlines = "tbl_basketlines"
tbl_order = "tbl_order"
tbl_category = "tbl_category"
tbl_stock = "tbl_stock"
tbl_rating = "tbl_rating"
tbl_review = "tbl_review"

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
    create_basketlines_tbl()
    create_stock_tbl()
    create_rating_tbl()
    create_review_tbl()

    print "Completed sucessfully"

def create_review_tbl():
	db = DBFUNC(config["SQLDB"])
	with db as cursor:
		query = "create table "+tbl_review+" (user_id INT(11) UNSIGNED NOT NULL, prod_id INT(11) UNSIGNED NOT NULL, commentdate datetime not null, comment VARCHAR(256), PRIMARY KEY (user_id, prod_id));"
		cursor.execute(query)

		query = "alter table "+tbl_review+" add constraint fk_review_user foreign key (user_id) references "+tbl_user+"(id);"
		cursor.execute(query)

		query = "alter table "+tbl_review+" add constraint fk_review_product foreign key (prod_id) references "+tbl_product+"(id);"
		cursor.execute(query)

	db.commit()

def create_rating_tbl():
	db = DBFUNC(config["SQLDB"])
	with db as cursor:
		query = "create table "+tbl_rating+" (user_id INT(11) UNSIGNED NOT NULL, prod_id INT(11) UNSIGNED NOT NULL, score INT(2), PRIMARY KEY (user_id, prod_id));"
		cursor.execute(query)

		query = "alter table "+tbl_rating+" add constraint fk_rating_user foreign key (user_id) references "+tbl_user+"(id);"
		cursor.execute(query)

		query = "alter table "+tbl_rating+" add constraint fk_rating_product foreign key (prod_id) references "+tbl_product+"(id);"
		cursor.execute(query)

	db.commit()

def create_stock_tbl():
	db = DBFUNC(config["SQLDB"])
	cursor = db.cursor()
	print "Creating table", tbl_stock
	query = "create table " + tbl_stock + "(product_id INT(11) UNSIGNED PRIMARY KEY, amount INT(9));"
	cursor.execute(query)
	query = "alter table " + tbl_stock+" add CONSTRAINT fk_prod_stock FOREIGN KEY (product_id) REFERENCES " \
									   ""+tbl_product+"(id);"
	cursor.execute(query)
	db.commit()
	db.close()

def create_category_tbl():
    db = DBFUNC(config["SQLDB"])
    cursor = db.cursor()
    print "Creating table", tbl_category
    query = "create table " + tbl_category + "(id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY, name VARCHAR(32));"
    cursor.execute(query)

    db.commit()
    db.close()

def create_product_tbl():
    db = DBFUNC(config["SQLDB"])
    cursor = db.cursor()
    print "Creating table", tbl_product
    query = "create table " + tbl_product + " (id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY, name VARCHAR(45), " \
											"description VARCHAR(256), image_url VARCHAR(128), price DECIMAL(6,2), cat_id INT(11) UNSIGNED);"
    cursor.execute(query)
    
    query = "alter table " + tbl_product+" add CONSTRAINT fk_cat FOREIGN KEY (cat_id) REFERENCES "+tbl_category+"(id);"
    cursor.execute(query)

    db.commit()
    db.close()

def create_orderlines_tbl():
    db = DBFUNC(config["SQLDB"])
    cursor = db.cursor()
    print "Creating table", tbl_orderlines
    query = "create table "+ tbl_orderlines +" (prod_id INT(11) UNSIGNED, order_id INT(11) UNSIGNED, amount INT(11) " \
											 "UNSIGNED);"
    cursor.execute(query)
    
    query = "alter table "+tbl_orderlines+" add CONSTRAINT fk_prod FOREIGN KEY (prod_id) REFERENCES "+tbl_product+"(id);"
    cursor.execute(query)
    
    query = "alter table "+tbl_orderlines +" add CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES "+tbl_order+"(id);"
    cursor.execute(query)
    db.commit()
    db.close()


def create_basketlines_tbl():
    db = DBFUNC(config["SQLDB"])
    cursor = db.cursor()
    print "Creating table", tbl_basketlines
    query = "create table "+ tbl_basketlines +" (user_id INT(11) UNSIGNED, prod_id INT(11) UNSIGNED, amount INT(11) UNSIGNED, PRIMARY KEY(user_id, prod_id));"
    cursor.execute(query)
    
    query = "alter table "+tbl_basketlines + " add CONSTRAINT fk_basket_prod FOREIGN KEY (prod_id) REFERENCES "+tbl_product+"(id);"
    cursor.execute(query)
    
    query = "alter table "+tbl_basketlines +" add CONSTRAINT fk_basket_user FOREIGN KEY (user_id) REFERENCES "+tbl_user+"(id);"
    cursor.execute(query)
    db.commit()
    db.close()

def create_order_tbl():
    db = DBFUNC(config["SQLDB"])
    cursor = db.cursor()
    print "Creating table", tbl_order
    query = "create table "+ tbl_order+" (id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY, customer_id INT(11) UNSIGNED NOT " \
					  "NULL, date DATE);"
    cursor.execute(query)
    query = "alter table "+ tbl_order+" add CONSTRAINT fk_customer_id FOREIGN KEY (customer_id) REFERENCES "+tbl_user+"(id);"
    cursor.execute(query)

    db.commit()
    db.close()

def create_user_tbl():
    db = DBFUNC(config["SQLDB"])
    cursor = db.cursor()
    print "Creating table", tbl_user
    query = "create table "+ tbl_user+" (id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY, email VARCHAR(32) UNIQUE,\
     password VARCHAR(128),name VARCHAR(128), address VARCHAR(64), postcode VARCHAR(9), city VARCHAR(32), country VARCHAR(32));"
    cursor.execute(query)

    db.commit();
    db.close()

def create_db():
    db = DBFUNC()
    cursor = db.cursor()
    print "Creating database", config["SQLDB"]
    query = "create database " + config["SQLDB"]+ ";"
    cursor.execute(query)

    db.commit();
    db.close()

def remove_db():
    db = DBFUNC()
    cursor = db.cursor()
    cursor.execute("show databases;")
    numrows = int(cursor.rowcount)

    for x in range(0, numrows):
        row = cursor.fetchone()
        if row[0] == config["SQLDB"]:
            print "Removing database", config["SQLDB"]
            query = "drop database " + config["SQLDB"]+ ";"
            cursor.execute(query)
            break
    db.commit();
    db.close()


main()



