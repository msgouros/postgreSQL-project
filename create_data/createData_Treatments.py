#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 14:45:32 2018
@author: Marnie Biando

NOSQL PROJECT 2 - SmallTown Hospital
LOAD ICD9 Treatments CSV file, sample 750 treatments, then generate subset CSV

"""

import os
import pandas as pd
import numpy as np

print("")
print("=== Creating treatment CSV file ===")


# get data from sibling directory
def getfile(sibling_dir, filename):
    
    parent_dir = os.path.split(os.getcwd())[0]
    sibling_dir = os.path.join(parent_dir, sibling_dir)
    datafile_path = os.path.join(sibling_dir, filename)
    return datafile_path


sibling_dir = 'data'
ICD_9_file = 'ICD-9-Treatments.csv'

nlines_in_file = 1123
num_treatments = 5

lines2skip = np.random.choice(np.arange(1,nlines_in_file+1), 
                              (nlines_in_file-num_treatments), 
                              replace=False)

df_treat = pd.read_csv(getfile(sibling_dir, ICD_9_file), skiprows=lines2skip)

print(num_treatments,  "rows sampled from ICD9 Treatments file: ", ICD_9_file)
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
df_treat.to_csv('../data/treatments_test.csv',
                   index=False)
print("Treatment data loaded into CSV format....")
