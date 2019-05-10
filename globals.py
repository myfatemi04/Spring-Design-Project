import mysql.connector

messages = {}
pool_params = []

def init_globals():
	global mysqld, messages, pool_params
	messages['l'] = "You must be logged in to do that"
	messages['ss'] = "Signup successful"
	messages['ssu'] = "Signup unsuccessful"
	messages['us'] = "Unsignup successful"
	messages['usu'] = "Unsignup unsuccessful"
	messages['af'] = "Please fill out all fields"
	messages['pf'] = "Pool is full"
	messages['bf'] = "One of your fields was in an incorrect format"
	pool_params = ['pool_id', 'pool_size','pool_date','driver_id','leave_location','come_location','leave_time','come_time', 'comments']
	mysqld = mysql.connector.connect(
		host = "localhost",
		user = "root",
		passwd = "jinny2yoo",
		database = "tjpool"
	)
def get_message(m):
	global messages
	if m in messages:
		return messages[m]
	else:
		return ''
