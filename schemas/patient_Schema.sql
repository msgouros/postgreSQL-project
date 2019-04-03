CREATE TABLE patients (
pat_id int PRIMARY KEY,
user_id int,
FOREIGN KEY (user_id) REFERENCES users (user_id)
);
