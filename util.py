import os.path
import globals
cache = {}

def get_name(username):
	cur = globals.mysqld.cursor(buffered=True)
	cur.execute("select * from users where username = %s;", (username,))
	fetch = cur.fetchall()
	if len(fetch) == 0:
		return "Anonymous"
	user = fetch[0]
	return user[2] + " " + user[3];

def txt(fname="frame", **args):
	filename = "frames/%s.html" % fname
	if fname in cache:
		mtime, txt = cache[fname]
		if os.path.getmtime(filename) == mtime:
			return txt % args
	txt = open(filename).read()
	cache[fname] = (os.path.getmtime(filename), txt)
	return txt % args
def user_exists(username, cursor=None):
	if cursor == None:
		cursor = globals.mysqld.cursor()
	cursor.execute("select * from users where username = %s;", (username,))
	return len(cursor.fetchall()) > 0

def get_nav(session):
	if 'username' in session:
		name = get_name(session['username'])
		print(name)
		return txt("nav_login", realname = name)
	else:
		return txt("nav_logout")
def pool_label(pool):
	params = globals.pool_params
	pool_values ={}
	for x in range(len(params)):
		pool_values[params[x]] = pool[x]
	return pool_values

def people_for_pool(pool_id):
	cur = globals.mysqld.cursor(buffered=True)
	cur.execute('select * from links where pool_id = %s', (pool_id,))
	people_coming = "None"
	people_list = cur.fetchall()
	ret = []
	for x in people_list:
		ret = ret + [x[0]]
	return ret

def get_pool_info(pool_id):
	cur = globals.mysqld.cursor(buffered=True)
	cur.execute("select * from carpools where pool_id = %s;", (pool_id,))
	pools = cur.fetchall()
	if len(pools) == 0:
		return None
	else:
		pool = pool_label(pools[0])
		people_list = people_for_pool(pool_id)
		people_coming = "None"
		for person in people_list:
			if people_coming == "None":
				people_coming = ""
			people_coming = people_coming + "<li>%s</li>" % person
		pool.update({'people_coming': people_coming})
		pool['driver_name'] = get_name(pool['driver_id'])
		return pool