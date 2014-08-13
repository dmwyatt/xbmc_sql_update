import argparse
import os

import pymysql


VIDEO_DATABASE = "MyVideos78"


def get_args():
	parser = argparse.ArgumentParser(description="Modify XBMC MySQL database when you change the location of files.")
	parser.add_argument("replace_this", help="The part of the path to replace.")
	parser.add_argument("with_this", help="What to replace replace_this with.")
	parser.add_argument("host", help="Database host.")
	parser.add_argument("user", help="Database user.")
	parser.add_argument("password", help="Database password.")
	parser.add_argument('--folders', help="A comma-separated list of folders surrounded by double quotes, "
	                                      "or a path to a text file containing a list of folders (one per line).  "
	                                      "If you have a folder with a comma in its name, god help you.")

	return parser.parse_args()


def get_folder_list(args):
	"""
	If the user provided the --folders argument, return a list of folders.  Otherwise returns None.
	"""
	if not args.folders:
		return None

	if os.path.isfile(args.folders):
		return [x.strip() for x in list(open(args.folders, 'r'))]

	else:
		return [x.strip() for x in args.folders.split(',')]


def build_sql_cmds(sql):
	"""
	Takes a string and formats it with the appropriate database, table, and column.

	:param sql:  A string formatted like "UPDATE {db}.{table} SET {column} = REPLACE({column}, %s, %s)"
	"""
	sql_cmds = []

	# Sql for path table
	sql_cmds.append(sql.format(db=VIDEO_DATABASE, table="path", column="strPath"))
	# SQL for movie table
	sql_cmds.append(sql.format(db=VIDEO_DATABASE, table="movie", column="c22"))
	# SQL for episode table
	sql_cmds.append(sql.format(db=VIDEO_DATABASE, table="episode", column="c18"))
	# SQL for art table
	sql_cmds.append(sql.format(db=VIDEO_DATABASE, table="art", column="url"))
	# SQL for tvshow table
	sql_cmds.append(sql.format(db=VIDEO_DATABASE, table="tvshow", column="c16"))

	return sql_cmds


def execute_sql_cmds(cursor, cmds, args):
	"""
	Execute each cmd in `cmds` parameterized with `args` with the provided cursor.

	:param cursor: MySQL-ish cursor.
	:param cmds: SQL statements
	:param args: Args to provide to the SQL statements in `cmds`
	"""
	for cmd in cmds:
		cursor.execute(cmd, args)
		print("{} rows updated on {} table for {}".format(cursor.rowcount, str.split(cmd)[1], args[2]))


def main(args):
	conn = pymysql.connect(args.host, args.user, args.password, VIDEO_DATABASE)
	cur = conn.cursor()

	# Basic sql without LIKE
	sql = "UPDATE {db}.{table} SET {column} = REPLACE({column}, %s, %s)"

	# Check if user passed in a list of folders
	folders = get_folder_list(args)
	if not folders:
		# User didn't so we're going to do a global replace
		execute_sql_cmds(cur, build_sql_cmds(sql), (args.replace_this, args.with_this))
	else:
		# User did, so we're going to add a LIKE on to our basic sql
		sql += " WHERE {column} LIKE %s"
		for folder in folders:
			like_folder = "%" + "{}" + "%"
			folder = like_folder.format(folder)
			cmds = build_sql_cmds(sql)
			execute_sql_cmds(cur, cmds, (args.replace_this, args.with_this, folder))
			conn.commit()

	cur.close()
	conn.close()


if __name__ == "__main__":
	main(get_args())

