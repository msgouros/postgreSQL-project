#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 09:37:17 2018
@author: Marnie Biando

NOSQL PROJECT 2 - SmallTown Hospital
version 3: combine patients & doctors into one table

Create all csv files:
    users.csv
    patients.csv
    doctors.csv
    illnesses.csv
    diagnoses.csv
    pat2doc.csv
    pat2ill.csv
    ill2treat.csv

FUTURE UPDATE: make path to where CSV files should be stored a variable    
    
"""

import random
import pandas as pd
import numpy as np
from faker import Faker
fake = Faker()

"""
Configurable parameters
Modify variables below to alter total number of 
patients, doctors, illnesses, and treatments
"""

num_patients = 10000
num_doctors = 100
num_illnesses = 1000
num_treatments = 750

"""
Create 10000 patients, 100 doctors
Doctors have a 35% chance of being a patient!

Approach: create patients first, then doctors.

"""

print("")
print("=== Creating patient CSV files ===")

# Create 3 temp dictionaries
# tempDict1 = row in users table 
# tempDict2 = row in patients table
# tempDict3 = row in doctors table

user_rows = []     #tempDict1
patient_rows = []  #tempDict2
doctors_rows = []  #tempDict3

user_counter = 1
doctor_counter = 1
patient_counter = 1

# Create patients first:
for i in range(num_patients):
    name = fake.name()
    tempDict1 = {'user_id': user_counter,
                 'name': name,
                 'patient': 'y',
                 'doctor' : 'n'}
    user_rows.append(tempDict1)
# Create record for user as patient        
    tempDict2 = {'pat_id': patient_counter,
                 'user_id': user_counter}
    patient_rows.append(tempDict2)
# Increment user and patient counters
    user_counter += 1
    patient_counter += 1   

# Create doctors second:
while(doctor_counter <= num_doctors):  
    name = fake.name()
# Roll the die..... 35% chance patient is also a doctor   
    chance = (random.randint(1,100))
    if chance < 36:
# Create record for user as doctor AND patient      
        tempDict1 = {'user_id': user_counter,
                    'name': name,
                    'patient': 'y',
                    'doctor' : 'y'}
        user_rows.append(tempDict1)
# Create record for user as patient        
        tempDict2 = {'pat_id': patient_counter,
                 'user_id': user_counter}
        patient_rows.append(tempDict2)
# Create record for user as a doctor        
        tempDict3 = {'doc_id': doctor_counter,
                     'user_id': user_counter}
        doctors_rows.append(tempDict3)
# Increment user and doctor counters
        user_counter += 1
        patient_counter += 1
        doctor_counter += 1
                
    else:
# Create record for user as doctor but NOT patient        
        tempDict1 = {'user_id': user_counter,
                    'name': name,
                    'patient': 'n',
                    'doctor' : 'y'}
        user_rows.append(tempDict1)
# Create record for user as a doctor        
        tempDict3 = {'doc_id': doctor_counter,
                     'user_id': user_counter}
        doctors_rows.append(tempDict3)
# Increment user and patient counters
        user_counter += 1
        doctor_counter += 1        

# Columns for the 3 CSV files
user_list=['user_id', 'name', 'patient', 'doctor']
patient_list=['pat_id', 'user_id']
doctor_list=['doc_id', 'user_id']        

# Create users dataframe
df_users = pd.DataFrame(user_rows, columns=user_list)
df_users = df_users.set_index('user_id')
df_users.to_csv('/Users/sgourosfamily/GitHub_Repositories/NoSQL_Project2/data/users.csv')           

# Create  patients dataframe
df_patients = pd.DataFrame(patient_rows, columns=patient_list)
df_patients = df_patients.set_index('pat_id')  
df_patients.to_csv('/Users/sgourosfamily/GitHub_Repositories/NoSQL_Project2/data/patients.csv')      

# Create  doctors dataframe
df_doctors = pd.DataFrame(doctors_rows, columns=doctor_list)
df_doctors = df_doctors.set_index('doc_id') 
df_doctors.to_csv('/Users/sgourosfamily/GitHub_Repositories/NoSQL_Project2/data/doctors.csv')    


"""
Create many-to-many (relationships table): PATIENTS to DOCTORS
Doctors are patients, too: make sure doctor is not treating him/herself
Patients can have 1-5 doctors assigned to them
"""

print("")
print("=== Creating many-to-many table: ===")
print("=== PATIENTS to DOCTORS ===")

pat2doc_rows = []   # mapping for postgres (pat2doc table)
user2user_rows = [] # mapping for neo4j (users (who are doctors) see users)
patient_is_doctor = 0

# Loop through for each patient in df_patients
for index, row in df_patients.iterrows(): 
# patient can have 1-5 doctors
    for i in range(random.randint(1,5)):    
# Randomly select a doctor fby selecting from index
        doc_idx = np.random.choice(list(df_doctors.index))
# Exact userID for doc        
        docs_userID = df_doctors.loc[doc_idx].user_id
# If the randomly selected userID matches patient's ID, choose another
        if docs_userID == row.user_id:
            print("Patient assigned to treat himself!")
# Keep count on number of times patient is assigned to himself
            patient_is_doctor += 1
# Select another user_id                 
            docs_userID = np.random.choice(df_doctors['user_id'])
            tempDict4a = {'pat_id': index,
                         'doc_id': doc_idx,
                         'doc_name': df_users.loc[docs_userID]['name']}
            tempDict4b = {'userid1': docs_userID,
                          'doc_name': df_users.loc[docs_userID]['name'],
                          'userid2': row.user_id,
                          'pat_name': df_users.loc[row.user_id]['name']}
            pat2doc_rows.append(tempDict4a)
            user2user_rows.append(tempDict4b)
        else:
            tempDict4a = {'pat_id': index,
                         'doc_id': doc_idx,
                         'doc_name': df_users.loc[docs_userID]['name']}
            tempDict4b = {'userid1': docs_userID,
                          'doc_name': df_users.loc[docs_userID]['name'],
                          'userid2': row.user_id,
                          'pat_name': df_users.loc[row.user_id]['name']}
            pat2doc_rows.append(tempDict4a)
            user2user_rows.append(tempDict4b)
    
# Create pat2doc table (for postgres)
df_pat2doc = pd.DataFrame(pat2doc_rows, columns=['pat_id','doc_id','doc_name'])
df_pat2doc = df_pat2doc.set_index('pat_id') 
# Write out pat2doc many-to-many to csv:
df_pat2doc.to_csv('/Users/sgourosfamily/GitHub_Repositories/NoSQL_Project2/data/pat2doc.csv')

# Create user2user mapping (for neo4J)
user2user_list = ['userid1', 'doc_name', 'userid2', 'pat_name']
df_user2user = pd.DataFrame(user2user_rows, columns=user2user_list)
# Write out user2user many-to-many to csv:
df_user2user.to_csv('/Users/sgourosfamily/GitHub_Repositories/NoSQL_Project2/data/user2user_neo4j.csv',
                  index=False)

print("Illness data loaded into CSV format....")
print("Total number of illnesses sampled: ", num_illnesses) 
print("")
print("Number of times patient was assigned to himself: ", patient_is_doctor)


"""
Create illnesses.csv
Variables: num_illnesses
"""

print("")
print("=== Creating illness CSV file ===")

filename = '/Users/sgourosfamily/GitHub_Repositories/NoSQL_Project2/data/ICD-9-Diagnoses.csv'
nlines_in_file = 14568

lines2skip = np.random.choice(np.arange(1,nlines_in_file+1), 
                              (nlines_in_file-num_illnesses), 
                              replace=False)
df_ill = pd.read_csv(filename, skiprows=lines2skip)

# add a numbered index
df_ill['ILL_ID'] = range(1, len(df_ill)+1)

# Drop the long description
df_ill.drop(['LONG DESCRIPTION'], axis=1)
df_ill = df_ill[['ILL_ID', 'SHORT DESCRIPTION', 'DIAGNOSIS CODE']]
df_ill.rename(columns={"ILL_ID": "ill_id", 
                              "SHORT DESCRIPTION": "description", 
                              "DIAGNOSIS CODE":"icd9"}, inplace=True)
df_ill = df_ill.set_index('ill_id')

# Write out illnesses to csv:
df_ill.to_csv('/Users/sgourosfamily/GitHub_Repositories/NoSQL_Project2/data/illnesses.csv')
print("Illness data loaded into CSV format....")
print("Total number of illnesses sampled: ", num_illnesses)


"""
Create treatments.csv
Variables: num_treatments
"""

print("")
print("=== Creating treatment CSV file ===")

filename = '/Users/sgourosfamily/GitHub_Repositories/NoSQL_Project2/data/ICD-9-Treatments.csv'
nlines_in_file = 1123

lines2skip = np.random.choice(np.arange(1,nlines_in_file+1), 
                              (nlines_in_file-num_treatments), 
                              replace=False)
df_treat = pd.read_csv(filename, skiprows=lines2skip)

print(num_treatments,  "rows sampled from ICD9 Treatments file: ", filename)
print("")

# add a numbered index
df_treat['id'] = range(1, len(df_treat)+1)

# change order of columns
df_treat = df_treat[['id', 'Code Description', 'CPT Code']]
cols = list(df_treat.columns.values)
df_treat.rename(columns={"id": "treat_id",
                   "Code Description":"description",
                   "CPT Code": "icd9"}, inplace=True)
df_treat = df_treat.set_index('treat_id')

# Write out udpated data to csv:
df_treat.to_csv('/Users/sgourosfamily/GitHub_Repositories/NoSQL_Project2/data/treatments.csv')
print("Treatment data loaded into CSV format....")



"""
Create many-to-many: PATIENTS to ILLNESSES
Create 1-to-3: treatments to illness

Patient can have 0-3 illnesess
If patient has 1+ illness, must have at least 1 treatment for each illness
"""

print("")
print("=== Creating many-to-many table: ===")
print("=== PATIENTS to ILLNESSES ===")

pat2ill_rows = []   #records patient to illness relationship
ill2treat_rows = []  #records illness to treatment relationship

# Loop through for each patient in df_patients
for index, row in df_patients.iterrows():
# patient can have 0-3 illnesses
# if patient has 0 illnesses, needs no treatment    
    for i in range(random.randint(0,3)):    
# Create 0-3 illnesses for patient     
# Randomly select an illness from df_ill dataframe:        
        ill_idx = np.random.choice(list(df_ill.index))
# Assign that illness to the patient, then store in patient-2-illness table        
        tempDict5 = {'pat_id': index,
                     'user_id': row.user_id,
                     'ill_id': ill_idx,
                     'ill_desc': df_ill.loc[ill_idx]['description']}
        pat2ill_rows.append(tempDict5)
# Randomly select a treatment from df_treat dataframe:
        treat_idx = np.random.choice(list(df_treat.index))
# Assign the treatment to the illness, then store in illness-2-treatment table
        tempDict6 = {'ill_id': ill_idx,
                     'treat_id': treat_idx, 
                     'treat_desc': df_treat.loc[treat_idx]['description'],
                     'pat_id': index,
                     'user_id': row.user_id,}
        ill2treat_rows.append(tempDict6)

# Columns for the  2 CSV files
pat2ill_list=['pat_id', 'user_id', 'ill_id', 'ill_desc']
ill2treat_list=['ill_id', 'treat_id', 'treat_desc', 'pat_id','user_id']

# Convert list of patient to illness mappings from a dataframe to CSV file     
df_pat2ill = pd.DataFrame(pat2ill_rows, columns=pat2ill_list)
df_pat2ill = df_pat2ill.set_index('pat_id')
df_pat2ill.to_csv('/Users/sgourosfamily/GitHub_Repositories/NoSQL_Project2/data/pat2ill.csv')    

# Convert list of illness to treatments from a dataframe to CSV file     
df_ill2treat = pd.DataFrame(ill2treat_rows, columns=ill2treat_list)
df_ill2treat = df_ill2treat.set_index('ill_id')
df_ill2treat.to_csv('/Users/sgourosfamily/GitHub_Repositories/NoSQL_Project2/data/ill2treat.csv')    

print("")
print("Total number patient-to-illness relationships created: ", len(df_pat2ill)) 

print("")
print("Total number illness-to-treatment relationships created: ", len(df_ill2treat)) 

