
-- DROP TABLE IF EXISTS user;
-- DROP TABLE IF EXISTS document;
-- DROP TABLE IF EXISTS keyword;

CREATE TABLE IF NOT EXISTS users (
	id SERIAL PRIMARY KEY,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS document (
	id SERIAL PRIMARY KEY,
	owner_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	name TEXT NOT NULL,
	checksum TEXT NOT NULL,
	FOREIGN KEY (owner_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS keyword (
	id SERIAL PRIMARY KEY,
	document_id INTEGER NOT NULL,
	keyword_text TEXT NOT NULL,
	keyword_weight FLOAT NOT NULL,
	FOREIGN KEY (document_id) REFERENCES document (id)
);
