#Grid esports for Every by sarmadasgher

import json

SEPARATOR = '_'

def denormalize_one_to_many(row, table):
    row_number = 0
    for entry in table:
        temp_dictionary = dict()
        for (k, v) in row.items():
            unique_key =  k + str(row_number)
            temp_dictionary[unique_key] = v
        row_number = row_number + 1
        entry.update(temp_dictionary)

def denormalize_many_to_one(table, row):

    row_number = 0
    for entry in table:
        for (k, v) in entry.items():
            unique_key = k + SEPARATOR + str(row_number)
            row[unique_key] = v
        row_number = row_number + 1

def iterate_array(json_array, table_name_prefix):
    table_name_prefix_with_separator = table_name_prefix + SEPARATOR    
    table = list()
    row_number = 0
    for element in json_array:
        row = dict()
        unique_key = table_name_prefix_with_separator + str(row_number)
        if type(element) == dict:
            row.update(iterate_dict(element, unique_key))
            denormalize_one_to_many(row, table)
        #too much adding in denormalized form
        #work in progress
        elif type(element) == list:
            pass
        else:
            row [unique_key] = str(element)
        table.append(row)
        row_number = row_number + 1
    return table

def iterate_dict(json_dictionary, table_name_prefix):
    row = dict()
    table_name_prefix_with_separator = table_name_prefix + SEPARATOR
    for (k, v) in json_dictionary.items():
        unique_key = table_name_prefix_with_separator + k
        if type(v) == dict:
            row.update(iterate_dict(v, unique_key))
        elif type(v) == list:
            table = iterate_array(v, unique_key)
            denormalize_many_to_one(table, row)
        else:
            row[unique_key] = str(v)
    return row

#This transformation is about iterating through JSON, picking every node and transforming into single denormalized relation.
#The denormalization process transforms to a dictionary, where value against each key is a string.
#This dictionary can be saved in db as a single row with keys as column names or can be saved in Redis as a key/value. 
def jtor(json_dictionary, table_name_prefix):
    return iterate_dict(json_dictionary, table_name_prefix)

