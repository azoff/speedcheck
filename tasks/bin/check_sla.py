#!/usr/bin/env python3

import logging
import speedtest
import json
import sys
import os
import sqlite3

logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z', level=logging.INFO)

db_path = sys.argv[1] if len(sys.argv) > 1 else os.environ['SQLITE3_DB_PATH']
logging.info(f'connecting to database {db_path}...')
conn = sqlite3.connect(db_path)
conn.row_factory=sqlite3.Row

offset = sys.argv[2] if len(sys.argv) > 2 else '-6 days'
sla = float(sys.argv[3] if len(sys.argv) > 3 else (100 * 1000000))
logging.info(f'checking {offset} average...')
cur = conn.cursor()
cur.execute('''
	select avg(download) as `avg`
	from speedtest
	where datetime(`timestamp`) >= datetime('now', ?)
''', (offset,))

avg = cur.fetchone()['avg']
if avg is None:
	logging.warning(f'no data found in {offset}')
elif sla > avg:
	logging.error(f'sample aggregate of {avg} is less than {sla}')
else:
	logging.info(f'sample aggregate of {avg} is greater than {sla}')


logging.info(f'cleaning up...')
cur.close()
conn.close()
