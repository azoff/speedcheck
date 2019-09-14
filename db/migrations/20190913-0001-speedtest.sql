CREATE TABLE IF NOT EXISTS speedtest (
	`timestamp` TIMESTAMP NOT NULL,
	download REAL NOT NULL,
	upload REAL NOT NULL,
	ping REAL NOT NULL,
	bytes_sent INTEGER NOT NULL,
	bytes_received INTEGER NOT NULL,
	share TEXT,
	server BLOB,
	client BLOB
);