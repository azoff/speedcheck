#!/usr/bin/env python3

import logging
import speedtest
import json
import sys
import os
import sqlite3
import twitter

logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z', level=logging.INFO)

db_path = sys.argv[1] if len(sys.argv) > 1 else os.environ['SQLITE3_DB_PATH']
logging.info(f'connecting to database {db_path}...')
conn = sqlite3.connect(db_path)
conn.row_factory=sqlite3.Row

secrets = None
secrets_path = sys.argv[2] if len(sys.argv) > 2 else os.environ['SECRETS_PATH']
with open(secrets_path) as secrets_file:
	secrets = json.load(secrets_file)

offset = secrets['offset']
logging.info(f'checking {offset} maximum...')
cur = conn.cursor()
cur.execute('''
	select download, share
	from speedtest
	where datetime(`timestamp`) >= datetime('now', ?)
	order by download desc
	limit 1
''', (offset,))

sla = secrets['minimum']
row = cur.fetchone()
download = round(row['download'] / 1000000, 2)
if download is None:
	logging.warning(f'no data found in {offset}')
elif sla < download:
	logging.info(f'sample max of {download} mb/s is acceptable.')
else:
	logging.warning(f'sample max of {download} mb/s is less than acceptable min of {sla} mb/s...')
	logging.info('connecting to twitter...')
	api = twitter.Api(**secrets['twitter_api'])
	logging.info(f'posting status update...')
	status = api.PostUpdate(secrets['status'] % {
		'offset': secrets['offset'][1:],
		'download': download
	}, media=row['share'])
	logging.info(f'status update: {status.urls[0].expanded_url}')


logging.info(f'cleaning up...')
cur.close()
conn.close()
