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
1. A minimum of 10,000 patients.
2. 10% of the patients must be doctors.
3. Doctors have a 35% chance of also being a patient.
4. Create illnesses.
5. Every patient will have 0, 1, 2, or 3 illnesses.  Probabilities are equally distributed.
6. If a patient has 1 or more illnesses, s/he must have 1 or more treatments assigned to each illness.
7. The maximum number of treatments per illness is up to the creator.

## Creating the Data

Python scripts were used to generate
