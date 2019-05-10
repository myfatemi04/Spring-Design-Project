import globals
import util
import random
import copy
from flask import Blueprint, redirect, session, request

blueprint = Blueprint('pool_signup', __name__, template_folder = '')

@blueprint.route('/signup/<string:pool_id>/')
def pool_signup(pool_id):
	if not 'username' in session:
		return redirect("/login/?error=l&next=/signup/%s" % pool_id)
	username = session['username']
	pool = util.get_pool_info(pool_id)
	if pool == None:
		return util.get_nav(session) + "Pool not found."
	cur = globals.mysqld.cursor(buffered=True)
	cur.execute("select * from links where username = %s and pool_id = %s", (username, pool_id))
	if len(cur.fetchall()) > 0:
		return util.get_nav(session) + "You've already signed up for this carpool"
	cur.execute("insert into links values (%s, %s);", (username, pool_id))
	globals.mysqld.commit()
	return redirect("/poolinfo/%s/?m=ss" % pool_id)

@blueprint.route('/unsignup/<string:pool_id>/')
def pool_unsignup(pool_id):
	if not 'username' in session:
		return redirect("/login/?error=l&next=/unsignup/%s" % pool_id)
	username = session['username']
	cur = globals.mysqld.cursor(buffered=True)
	cur.execute("delete from links where username = %s and pool_id = %s;", (username, pool_id))
	globals.mysqld.commit()
	if (cur.rowcount > 0):
		return redirect("/poolinfo/%s/?m=us" % pool_id)
	else:
		return redirect("/poolinfo/%s/?m=usu" % pool_id)
@blueprint.route('/poolinfo/<string:pool_id>/', methods = ['GET'])
def pool_info(pool_id):
	ret = util.get_nav(session) + globals.get_message(request.args.get('m'))
	pool = util.get_pool_info(pool_id)
	if pool == None:
		ret = ret + "Pool not found"
	else:
		ret = ret + ("<h1>Pool ID: %s</h1>" % pool_id) + util.txt("pool_box", **pool)
	return util.txt('frame', title='Pool info', style='', script='', body=ret)

@blueprint.route('/createpool/do/', methods = ['POST'])
def pool_create_do():
	params = copy.copy(globals.pool_params)
	params.remove('driver_id')
	params.remove('pool_id')
	if 'username' not in session:
		return redirect("/login/?error=l")
	pool_values = {'pool_id': random.randint(0, 1e9), 'driver_id': session['username']}
	for x in params:
		if x not in request.form or request.form[x] == '':
			return redirect('/createpool/?m=af')
		pool_values[x] = request.form[x]
	date_int = pool_values['pool_date']
	print(date_int)
	year, month, day = date_int.split("-")
	year = int(year)
	month = int(month)
	day = int(day)
	print(year,month,day)
	print(10000 * (year - 2018) + 100 * month + day)
	pool_values['pool_date'] = 10000 * (year - 2018) + 100 * month + day;
	cur = globals.mysqld.cursor(buffered=True)
	cur.execute("insert into carpools values (%(pool_id)s, %(pool_size)s, %(pool_date)s, %(driver_id)s, %(leave_location)s, %(come_location)s, %(leave_time)s, %(come_time)s, %(comments)s)", pool_values)
	globals.mysqld.commit()
	return redirect("/poolinfo/%s/" % pool_values['pool_id'])
@blueprint.route('/createpool/')
def pool_create():
	if 'username' not in session:
		return redirect("/login/?error=l")
	return util.txt('frame', title='Create pool', style='', script='', body=util.get_nav(session) + globals.get_message(request.args.get('m')) + '<br/>' + util.txt('pool_create_form'))