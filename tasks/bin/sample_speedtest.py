#!/usr/bin/env python3

# import os
# os.environ['SQLITE3_DB_PATH']
import logging
import speedtest
import json
import sys
import os
import sqlite3

log = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(levelname)s %(asctime)s %(message)s', '%Y-%m-%dT%H:%M:%S%z'))

log.setLevel(logging.INFO)
log.addHandler(handler)

st = speedtest.Speedtest()

log.info('fetching list of available servers...')
st.get_servers()

log.info('determining best server...')
st.get_best_server()

log.info('sampling download speeds...')
st.download()

log.info('sampling upload speeds...')
st.upload()

log.info('generating share link...')
st.results.share()

db_path = sys.argv[1] or os.environ['SQLITE3_DB_PATH']
log.info(f'connecting to database {db_path}...')
conn = sqlite3.connect(db_path)

log.info(f'saving results...')
results = st.results.dict()
results['server'] = json.dumps(results['server'])
results['client'] = json.dumps(results['client'])
conn.execute('''
	INSERT INTO speedtest (`timestamp`,`download`,`upload`,`ping`,`bytes_sent`,`bytes_received`,`share`,`server`,`client`)
	VALUES (:timestamp,:download,:upload,:ping,:bytes_sent,:bytes_received,:share,:server,:client)
''', results)

log.info(f'cleaning up...')
conn.commit()
conn.close()
