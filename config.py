config = dict(
	#server
	HOSTIP='192.168.1.6',
	HOSTPORT=5000,
	HOSTDBG=True,
	HOSTKEY="SUPER-SECRET-SIGNING-KEY-:o)",

	UPLOAD_FOLDER = 'static/img',
	ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif']),

	#mysql
	HOST='localhost',
	PORT=3306,
	USER='axel',
	PASSWD='bollboll',
	SQLDB='db_adot',
	CHARSET='utf8',

	#SSL-enabled?
	USE_SSL=False
	)
