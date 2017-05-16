CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_name varchar(256) NOT NULL UNIQUE,
    password varchar(256) NOT NULL,
    key_id char(16),
    fingerprint char(40),
    armored_key varchar(4096),
    verified boolean default false,
    date_verified timestamp,
    date_created timestamp default now(),
    last_login timestamp 
);

CREATE TABLE IF NOT EXISTS pending (
    id SERIAL PRIMARY KEY,
    key_id char(16) NOT NULL
);

CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    author varchar(256) REFERENCES users(user_name),
    date_created timestamp default now(),
    date_updated timestamp default now(),
    content text,
    signature varchar(256)
);
