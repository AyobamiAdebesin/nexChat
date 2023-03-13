-- setup development database in MySQL server
CREATE DATABASE IF NOT EXISTS twibbly_dev_db;
CREATE USER IF NOT EXISTS 'twibbly_dev'@'localhost' IDENTIFIED BY 'Olaseni..1996';
GRANT ALL PRIVILEGES ON twibbly_dev_db.* TO 'twibbly_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'twibbly_dev'@'localhost';