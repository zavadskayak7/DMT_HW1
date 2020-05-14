#!/usr/bin/env python
# coding: utf-8



import pandas as pd
import numpy as np
import string
import csv
import re
import random 
import math

#############################################################################
# Hash Functions
#############################################################################

num_hash_functions = 81
upper_bound_on_number_of_distinct_elements  = 10000000

### primality checker
def is_prime(number):
    if number == 2:
        return True
    if (number % 2) == 0:
        return False
    for j in range(3, int(math.sqrt(number)+1), 2):
        if (number % j) == 0: 
            return False
    return True

### generating the parameters tuples
set_of_all_hash_functions = set()
while len(set_of_all_hash_functions) < num_hash_functions:
    a = random.randint(1, upper_bound_on_number_of_distinct_elements-1)
    b = random.randint(0, upper_bound_on_number_of_distinct_elements-1)
    p = random.randint(upper_bound_on_number_of_distinct_elements, 10*upper_bound_on_number_of_distinct_elements)
    while is_prime(p) == False:
        p = random.randint(upper_bound_on_number_of_distinct_elements, 10*upper_bound_on_number_of_distinct_elements)
    #
    current_hash_function_id = tuple([a, b, p])
    set_of_all_hash_functions.add(current_hash_function_id)

### generating the data file with the parameters tuples

hash_df = pd.DataFrame(set_of_all_hash_functions)
hash_df.insert(3, column = "n", value = "10000000")
hash_df.columns= ["a", "b", "p", "n"]
hash_df.to_csv("81_hash_functions.tsv", sep='\t', index = False)

#############################################################################
# Shingling
#############################################################################


#### Creating the dataset 


directory_to_dataset = 'part_2/dataset/250K_lyrics_from_MetroLyrics.csv'
data = pd.read_csv(directory_to_dataset)
data.drop(columns = ["song", "year", "artist", "genre"], inplace = True)
data.head()


#### Removing punctuation and transforming everything into lowercase


data['lyrics'] = [re.sub('[^A-Za-z0-9]+', ' ', data['lyrics'][i]) for i in range(0,len(data['lyrics'])) ]
data['lyrics'] = [data['lyrics'][i].lower() for i in range(0, len(data['lyrics']))]


#### Creating and hashing the shingles


def get_shingles(size, f):
    shingles = set()
    for i in range (0, len(f)-size+1):
        shingles.add((abs(hash(''.join(f[i:i+size]))) % (10 ** 8)))
    return shingles

data['lyrics'] = [list(get_shingles(3, data['lyrics'][i].split())) for i in range(0, len(data['lyrics']))]


#### Export the data file


data.to_csv("input_data_250K.tsv", sep='\t', index = False)

#############################################################################
# Final Analysis
#############################################################################



appJ = [0.89, 0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1]

directory_to_output = './data/near_duplicates_13_15.tsv'
results = pd.read_csv(directory_to_output, sep = '\t')
results['dummy_field'] = results['dummy_field'].round(2)

# Counting the results

appJ = {i: [results['dummy_field'][results.dummy_field >=i].count(), results['dummy_field'][results.dummy_field == i].count()] for i in appJ}

# Displaying the results

duplicatesFound = pd.DataFrame(appJ).T
duplicatesFound.index.names = ["Jaccard Similarity s"]
duplicatesFound.columns = ["Duplicates with Jaccard Similarity at least s", "Duplicates at Jaccard Similarity s"]
duplicatesFound

