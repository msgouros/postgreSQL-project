CREATE TABLE pat2doc (
pat_id int,
doc_id int,
doc_name text,
FOREIGN KEY (pat_id) REFERENCES patients(pat_id),
FOREIGN KEY (doc_id) REFERENCES doctors(doc_id)
);
