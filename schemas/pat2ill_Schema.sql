CREATE TABLE pat2ill (
pat_id int,
ill_id int,
ill_name text,
FOREIGN KEY (pat_id) REFERENCES patients(pat_id),
FOREIGN KEY (ill_id) REFERENCES illnesses(ill_id)
);