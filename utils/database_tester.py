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
    clear_database()
    add_testdata()
    print_database()  # Removing existing database if it already exists
    print "\nCompleted sucessfully"

def add_testdata():
    db = DBFUNC(SQLDB)
    print "Adding testdata"
    cursor = db.cursor()
    cursor.execute("insert into " + tbl_user + " (username, password, email) VALUES ('kurt', 'ollonmacka', 'kurt@live.se');")
    cursor.execute("insert into " + tbl_user + " (username, password, email) VALUES ('axel', 'bollboll', 'axel@gmail.se');")
     
    cursor.execute("insert into " + tbl_category + "(name) values ('Fine Gravel');")
    cursor.execute("insert into " + tbl_category + "(name) values ('Lag Gravel');")
    cursor.execute("insert into " + tbl_category + "(name) values ('Plateau Gravel');")
    cursor.execute("insert into " + tbl_category + "(name) values ('Pea Gravel');")
    cursor.execute("insert into " + tbl_category + "(name) values ('Crushed Stone');")
   
    cursor.execute("insert into " + tbl_product + "(name, description, image_url, price, cat_id) values ('Gravel 2mm', 'Two millimeter fine gravel', '/images/fine1.png', '29.50', (SELECT id from tbl_category WHERE name='Fine Gravel'));")
    cursor.execute("insert into " + tbl_product + "(name, description, image_url, price, cat_id) values ('Gravel 4mm', 'Four millimeter fine gravel', '/images/fine2.png', '99.90', (SELECT id from tbl_category WHERE name='Fine Gravel'));")
    cursor.execute("insert into " + tbl_product + "(name, description, image_url, price, cat_id) values ('Granite', 'A common type of felsic intrusive igneous rock that is granular and phaneritic in texture.', '/images/granite.png', '995.90', (SELECT id from tbl_category WHERE name='Crushed Stone'));")
    cursor.execute("insert into " + tbl_product + "(name, description, image_url, price, cat_id) values ('Limestone', 'A sedimentary rock composed largely of the minerals calcite and aragonite.', '/images/limestone.png', '1050.0', (SELECT id from tbl_category WHERE name='Crushed Stone'));")
    cursor.execute("insert into " + tbl_product + "(name, description, image_url, price, cat_id) values ('Dolomite', 'An anhydrous carbonate mineral composed of calcium magnesium carbonate.', '/images/rock.png', '1250.0', (SELECT id from tbl_category WHERE name='Crushed Stone'));")
    
    db.commit()
    db.close()
    
def clear_database():
    db = DBFUNC(SQLDB)
    print "Removing testdata"
    cursor = db.cursor()
    cursor.execute("delete from tbl_user;")
    cursor.execute("delete from tbl_product;")
    cursor.execute("delete from tbl_orderlines;")
    cursor.execute("delete from tbl_order;")
    cursor.execute("delete from tbl_category;")
    print "Done"
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



