ALTER TABLE articles ADD COLUMN published boolean default false;
UPDATE articles SET published = true WHERE published is false;

ALTER TABLE articles ADD COLUMN raw_input text;
ALTER TABLE articles ADD COLUMN mime_type varchar(256);
