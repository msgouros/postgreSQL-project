CREATE TABLE ill2treat (
ill_id int,
treat_id int,
treat_desc text,
pat_id int,
user_id int,
FOREIGN KEY (ill_id) REFERENCES illnesses(ill_id),
FOREIGN KEY (treat_id) REFERENCES treatments(treat_id),
FOREIGN KEY (pat_id) REFERENCES patients(pat_id)
);
