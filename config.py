import time

config = dict(
	#server
	HOSTIP='localhost',
	HOSTPORT=5000,
	HOSTDBG=True,
	HOSTKEY="SUPER-SECRET-SIGNING-KEY-:o)"+str(int(time.time())),
	RATE_LIMIT = ["90/minute"],

	DEFAULT_IMAGE = '/static/img/default.png/',
	UPLOAD_FOLDER = '/static/img/',
	ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif']),

	#mysql
	HOST='localhost',
	PORT=3306,
	USER='',
	PASSWD='',
	SQLDB='db_edot',
	CHARSET='utf8',

	#SSL-enabled?
	USE_SSL=False
	)
