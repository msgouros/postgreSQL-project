CREATE TABLE doctors (
doc_id int PRIMARY KEY,
user_id int,
FOREIGN KEY (doc_id) REFERENCES doctors(doc_id)
);