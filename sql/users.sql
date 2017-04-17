CREATE SCHEMA IF NOT EXISTS users;

CREATE TABLE IF NOT EXISTS users.users (
    id SERIAL PRIMARY KEY,
    user_name varchar(256) NOT NULL UNIQUE,
    key_id char(16) NOT NULL,
    fingerprint char(40) NOT NULL,
    armored_key varchar(4096),
    verified boolean default false,
    date_verified timestamp,
    date_created timestamp,
    last_login timestamp 
);

CREATE TABLE IF NOT EXISTS users.pending (
    id SERIAL PRIMARY KEY,
    key_id char(16) NOT NULL,
);
