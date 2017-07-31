CREATE TABLE IF NOT EXISTS u2f_devices (
    id SERIAL PRIMARY KEY,
    user_name varchar(256) REFERENCES users (user_name) NOT NULL,
    key_nick varchar(256) NOT NULL,
    version varchar(16) NOT NULL,
    keyHandle text NOT NULL,
    transports varchar(256),
    appId varchar(256) NOT NULL,
    registration_date timestamp default now()
);
