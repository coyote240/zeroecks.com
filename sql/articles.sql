CREATE SCHEMA IF NOT EXISTS articles;

CREATE TABLE IF NOT EXISTS articles.articles (
    id SERIAL PRIMARY KEY,
    author varchar(256) REFERENCES users.users(user_name),
    date_created timestamp,
    date_updated timestamp,
    content text,
    signature varchar(256)
);
