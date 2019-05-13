from flask import Blueprint, Response, render_template, abort, request, session, redirect
from util import *
from werkzeug import generate_password_hash, check_password_hash
import globals

blueprint = Blueprint('register', __name__, template_folder='')

def get_user_info(username):
	cur = globals.mysqld.cursor(buffered=True)
	cur.execute("select * from users where username = %s;", (username,))
	f = cur.fetchall()
	if (len(f) > 0):
		return f[0]
	else:
		return []

@blueprint.route("/register/", methods = ['GET', 'POST'])
def register():
	username = request.form.get('username')
	firstname = request.form.get('firstname')
	lastname = request.form.get('lastname')
	password = request.form.get('password')
	phone = request.form.get('phone')
	
	if all((username, firstname, lastname, password, phone)):
		cursor = globals.mysqld.cursor(buffered=True)
		password_encrypt = generate_password_hash(password)
		if not user_exists(username, cursor):
			cursor.execute("insert into users values (%s, %s, %s, %s, %s, %s, %s)", (username, password_encrypt, firstname, lastname, 0, 0, phone))
			globals.mysqld.commit()
			
			return txt("frame", title="Register", style="", script="", body=get_nav(session) + "Added {} [{}, {}]".format(username, firstname, lastname))
		else:
			
			return txt("frame", title="Register", style="", script="", body=get_nav(session) + "User already exists. <br/>" + txt("form_register"))
	return txt("frame", title="Register", style="", script="", body=get_nav(session) + "Please fill out all fields. <br/>" + txt("form_register"))

@blueprint.route("/login/", methods = ['GET', 'POST'])
def login():
	if 'username' in session:
		return redirect('/')
	if 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = globals.mysqld.cursor(buffered=True)
		if not user_exists(username, cursor):
			return redirect('/login/?error=User%20doesn\'t%20exist')
		cursor.execute("select password from users where username = %s;", (username,))
		password_encrypt = cursor.fetchall()[0][0]
		password_correct = check_password_hash(password_encrypt, password)
		if password_correct:
			session['username'] = username
			return txt("frame", title="Login", style="", script="", body=get_nav(session) + "Successfully logged in.")
		return "Login unsuccessful"
	else:
		err = ''
		if 'error' in request.args and request.args['error'] in globals.messages:
				err = globals.messages[request.args['error']]
		return txt("frame", title="Login", style="", script="", body=get_nav(session) + err + "<br/><h2>Login</h2><br/>" + txt("form_login"))
	
@blueprint.route("/logout/", methods = ['GET'])
def logout():
	if 'username' in session:
		session.pop('username', None)
		return txt("frame", script = '', style = '', title = 'Log out', body = get_nav(session) + "<br/>Successfully logged out")
	else:
		return txt("frame", script = '', style = '', title = 'Log out', body = get_nav(session) + "<br/>You aren't logged in")

@blueprint.route("/user/<string:username>")
def user_contact(username='null'):
	return txt("frame", script = '', style = '', title = 'Contact Info: ' + username, body = get_nav(session) + "<br/>" + txt("contact_info", driver_id = username, phone = get_user_info(username)[6]))