ALTER TABLE users ADD COLUMN salt char(32) NOT NULL DEFAULT('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx');
ALTER TABLE users ALTER COLUMN password TYPE char(128);
