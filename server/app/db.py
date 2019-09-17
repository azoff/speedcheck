import os
import sqlite3

_conn = None

def conn():
	global _conn
	if _conn is None:
		_conn = sqlite3.connect(os.environ['SQLITE3_DB_PATH'])
		_conn.row_factory=sqlite3.Row
	return _conn

def cursor():
	return conn().cursor()

def execute(query, params, cur = None):
	cur = cur or cursor()
	cur.execute(query, params)
	return cur

def fetchone(*args, **kwargs):
	return execute(*args, **kwargs).fetchone()

def fetchall(*args, **kwargs):
	return execute(*args, **kwargs).fetchall()

def mogrify(*args, cur = None, **kwargs):
	cur = cur or cursor()
	return cur.mogrify(*args, **kwargs)

#TODO: conn.close()
