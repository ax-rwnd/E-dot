from flask import abort, g
from flask.ext.login import current_user

from access_levels import access

## Admin Table
# pk(user_id), level
# user_id - fk, int(11)
# level, unsigned int(4)
	
def test_access (uid, access):
	db = getattr(g, 'db', None)

	with db as cursor:
		query = "select level from tbl_admin where user_id = %s;"

		if cursor.execute(query, (uid,)) <= 0:
			#That user has no clearance.
			return False;
		elif cursor.fetchone()[0] > access:
			#That user has insufficient clearance.
			return False;
		else:
			#That user has sufficient clearance.
			return True

#check if current_user actually has access
def perimeter_check (access_str):
	if not test_access(current_user.uid, access[access_str]):
		abort(403)

def admin_config (uid, newaccess):
	db = getattr(g, 'db', None)

	with db as cursor:
		query = "insert into tbl_admin (user_id, level) values (\
			(select id from tbl_user where id = %s), %s) on\
			duplicate key update level=values(level);"
		cursor.execute(query, (uid, newaccess))
