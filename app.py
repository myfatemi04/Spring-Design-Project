from flask import Flask, render_template, json, request, session
from werkzeug import generate_password_hash, check_password_hash
import register
import pool_signup
import globals
import os.path
from util import *

app = Flask(__name__)

app.secret_key = 'PkOBZ0LzRZ3abaSdYaZF'

app.register_blueprint(register.blueprint)
app.register_blueprint(pool_signup.blueprint)

@app.route("/")
def main():
	cur = globals.mysqld.cursor(buffered=True)
	cur.execute("select * from users;")
	users = cur.fetchall()
	cur.execute("select * from carpools;")
	pools = cur.fetchall()
	cur.execute("select * from links;")
	links = cur.fetchall()
	ret = "Welcome!<br/><h2>Users:</h2><ul>"
	for u in users:
		ret = ret + "<li>%s %s [%s]</li>" % (u[2], u[3], u[0])
	ret = ret + "</ul>"
	ret = ret + "<h2>Carpools:</h2><ul>"
	for x in pools:
		p = get_pool_info(x[0])
		ret = ret + txt("pool_box", **p)
	ret = ret + "</ul>"
	"""
	ret = ret + "Links: <ul>"
	for l in links:
		ret = ret + "<li>%s: going to pool %s</li>" % (l[0], l[1])
	ret = ret + "</ul>"
	"""
	return txt("frame", title="TJ Pool", style="", script="", body = get_nav(session) + ret)

@app.route("/css/<string:fname>")
def css(fname):
	fname = fname.replace("/", "").replace("\\", "");
	if (os.path.isfile("./css/" + fname)):
		return open("./css/" + fname).read()
	else:
		return "File not found"
if __name__ == "__main__":
	globals.init_globals()
	app.run(host='10.16.176.89', port=5000, debug=False)