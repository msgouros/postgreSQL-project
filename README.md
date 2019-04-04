# postgreSQL-project

## Background
This was an assignment in a NoSQL course that covered the following databases:
(1) PostgreSQL
(2) MongoDB
(3) CouchDB
(4) Neo4J
(5) Redis

And yes, I understand that PostgreSQL is *not* a "NoSQL" database.  However, the course needed to include PostgreSQL as a contrast to the noSQL databases.

## About this Project
In this project we were asked to populate a database with the following requirements:
1. Create a minimum of 10,000 patients.
2. 10% of the patients must be doctors.
3. Doctors have a 35% chance of also being a patient.
4. Create a minimum of 1,000 illnesses.
5. Every patient will have 0, 1, 2, or 3 illnesses.  Probabilities are equally distributed.
6. If a patient has 1 or more illnesses, s/he must have 1 or more treatments assigned to each illness.
7. The maximum number of treatments per illness is up to the creator.

## Creating the Data

Python scripts were used to generate the 10,000 patients using the Python package ```Faker```.  This ensured person's identification information was realistic (instead of gobbledygook).

Faker was also used to generate diagnoses and treatments -- however in this case, the source files are real ICD-9 codes (which are used by the healthcare industry): http://www.icd9data.com

See Python scripts -- the random package was used to calculate probabilities (each doctor had a 35% probability of also being a patient), whether a patient was assigned 0-3 illnesses (these were equally weighted) and finally, randomly choosing 1000 illnesses from the ICD-9 diagnosis file.
