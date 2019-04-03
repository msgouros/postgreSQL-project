#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 14:45:32 2018
NOSQL PROJECT 2 - SmallTown Hospital
LOAD ICD9 Treatments CSV file, sample 750, then generate subset CSV

enumerated output file at /Users/sgourosfamily/nosql-db/Project2/data
"""

import pandas as pd
import numpy as np

print("")
print("=== Creating treatment CSV file ===")

filename = '/Users/sgourosfamily/GitHub_Repositories/NoSQL_Project2/data/ICD-9-Treatments.csv'
nlines_in_file = 1123
num_treatments = 5

lines2skip = np.random.choice(np.arange(1,nlines_in_file+1), 
                              (nlines_in_file-num_treatments), 
                              replace=False)
df_treat = pd.read_csv(filename, skiprows=lines2skip)

print(num_treatments,  "rows sampled from ICD9 Treatments file: ", filename)
print("")

# add a numbered index
df_treat['id'] = range(0, len(df_treat))

# change order of columns
df_treat = df_treat[['id', 'Code Description', 'CPT Code']]
cols = list(df_treat.columns.values)
print("new order of columns: ", cols)

df_treat.rename(columns={"id": "id",
                   "Code Description":"description",
                   "CPT Code": "icd9"}, inplace=True)

# Write out udpated data to csv:
df_treat.to_csv('/Users/sgourosfamily/GitHub_Repositories/NoSQL_Project2/data/treatments_test.csv',
                   index=False)
print("Treatment data loaded into CSV format....")
