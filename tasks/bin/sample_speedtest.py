#!/usr/bin/env python3

import logging
import speedtest
import json
import sys
import os
import sqlite3

logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z', level=logging.INFO)

st = speedtest.Speedtest()

logging.info('fetching list of available servers...')
st.get_servers()

logging.info('determining best server...')
st.get_best_server()

logging.info('sampling download speeds...')
st.download()

logging.info('sampling upload speeds...')
st.upload()

logging.info('generating share link...')
st.results.share()

db_path = sys.argv[1] if len(sys.argv) > 1 else os.environ['SQLITE3_DB_PATH']
logging.info(f'connecting to database {db_path}...')
conn = sqlite3.connect(db_path)

logging.info(f'saving results...')
results = st.results.dict()
results['server'] = json.dumps(results['server'])
results['client'] = json.dumps(results['client'])
conn.execute('''
	INSERT INTO speedtest (`timestamp`,`download`,`upload`,`ping`,`bytes_sent`,`bytes_received`,`share`,`server`,`client`)
	VALUES (:timestamp,:download,:upload,:ping,:bytes_sent,:bytes_received,:share,:server,:client)
''', results)

logging.info(f'cleaning up...')
conn.commit()
conn.close()
