#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 07:23:18 2018
@author: Marnie Biando

NOSQL PROJECT 2 - SmallTown Hospital
LOAD ICD9 Diagnoses CSV file, sample 1,000 then generate subset CSV

enumerated output file at /Users/sgourosfamily/nosql-db/Project2/data
"""

import pandas as pd
import numpy as np

filename = '/Users/sgourosfamily/GitHub_Repositories/NoSQL_Project2/data/ICD-9-Diagnoses.csv'
nlines_in_file = 14568
nlinesrandomsample = 10

lines2skip = np.random.choice(np.arange(1,nlines_in_file+1), 
                              (nlines_in_file-nlinesrandomsample), 
                              replace=False)
df = pd.read_csv(filename, skiprows=lines2skip)

print(nlinesrandomsample,  "rows sampled from ICD9 DIAGNOSES file: ", filename)
print("")

# add a numbered index
df['ILL_ID'] = range(1, len(df) + 1)

# Drop the long description
df.drop(['LONG DESCRIPTION'], axis=1)

# change order of columns
print("========== Before we reorder columns ===========")
cols = list(df.columns.values)
print("current order of columns: ", cols)
print("")
print("==========  After reordering of columns ===========")
df = df[['ILL_ID', 'SHORT DESCRIPTION', 'DIAGNOSIS CODE']]
cols = list(df.columns.values)
print("new order of columns: ", cols)

#relabel headers to match other csv files
#df.columns['id', 'desc', 'icd9']

df.rename(columns={"ILL_ID": "id", 
                              "SHORT DESCRIPTION": "desc", 
                              "DIAGNOSIS CODE":"icd9"}, inplace=True)

# Write out udpated data to csv:
df.to_csv('/Users/sgourosfamily/GitHub_Repositories/NoSQL_Project2/data/illnesses_test.csv',
                   index=False)
print("Illness data loaded into CSV format....")

