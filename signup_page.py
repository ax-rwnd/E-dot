from flask import Blueprint, render_template, request, g
from werkzeug.security import generate_password_hash

signup_page = Blueprint('signup_page', __name__, template_folder='templates')

@signup_page.route("/signup")
def show_signup():
    return render_template("signup.html")

# policy check
def password_policy(pwd):
    if not pwd:
        return False
    elif (len(pwd) < 8 or len(pwd) > 32):
        return False
    else:
        # TODO: add upper+lower+num check, use regex?
        return True

def email_validation(txt):
    if (-1 == txt.find('@')):
        return False
    elif (-1 == txt.find('.')):
        return False
    else:
        return True

@signup_page.route("/signup", methods=['POST'])
def show_signup_post():

    email = request.form['emailtext']
    passwd = request.form['pwtext']
    repass = request.form['pwrepeat']
    nametext = request.form['nametext']
    addresstext = request.form['addresstext']
    postcodetext = request.form['postcodetext']
    citytext = request.form['citytext']
    country = request.form['countrytext']

    if not(email and passwd and nametext and addresstext and postcodetext and citytext and country):
        return render_template("signup.html", message = "Registration Complete")
    elif email and not email_validation(email):
        return render_template("signup.html", message = "Invalid Email")
    elif not password_policy(passwd) or not (passwd == repass):
        return render_template("signup.html", message = "Invalid Password")

    db = getattr(g, 'db', None)

    try:
        query = ""
        with db as cursor:
            data = (email)
            query = "SELECT * FROM tbl_user WHERE email=%s;"
            cursor.execute(query, data)
            if cursor.fetchone() > 0:
                return render_template("signup.html", message = "Email Address Already Registered.")
    except Exception as e:
        print e

    try:
        query = ""
        with db as cursor:
            data = (email, generate_password_hash(passwd), nametext, addresstext, postcodetext, citytext, country)
            query = "INSERT INTO tbl_user (email, password, name, address, postcode, city, country) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(query, data)
            db.commit()
    except Exception as e:
        print e

    return render_template("login.html", message = "Registration Complete", status = True)
