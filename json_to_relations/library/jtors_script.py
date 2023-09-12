#Grid esports for Every by sarmadasgher

import json
from datetime import datetime

SEPARATOR = '_'

def create_table_and_insert_rows_script(table, table_name, file_handle_to_sql_script):
    if len(table) == 0:
        return
    
    column_names = set()
    for row in table:
        for column_name in row.keys():
            column_names.add(column_name)
    if len(column_names) == 0:
        return

    column_names = list(column_names)
    column_names.sort()
    create_table_script = f'CREATE TABLE `{table_name}` (\n'
    for column_name in column_names:
        create_table_script += f'`{column_name}` LONGTEXT,\n'
    create_table_script = create_table_script[:-2]
    create_table_script += ');\n' 

    insert_rows_script = f'INSERT INTO `{table_name}` VALUES \n'
    for row in table: 
        insert_rows_script += '('
        for column_name in column_names:
            insert_rows_script += f'"{row.get(column_name, "")}", '
        insert_rows_script = insert_rows_script[:-2]
        insert_rows_script += '),\n'
    insert_rows_script = insert_rows_script[:-2]
    insert_rows_script += ';\n'
    file_handle_to_sql_script.write(create_table_script)
    file_handle_to_sql_script.write(insert_rows_script)

def convert_to_table(row, json_array, json_array_prefix):
    table = list()
    for entry in json_array:
        if type(entry) == dict:
            row_from_entry = dict()
            for (k, v) in entry.items():
                row_from_entry[json_array_prefix + SEPARATOR + k] = str(v)
            row_from_entry.update(row)
            table.append(row_from_entry)
        elif type(entry) != list:
            row_from_entry = dict()
            row_from_entry[json_array_prefix] = str(entry)
            row_from_entry.update(row)
            table.append(row_from_entry)

            
    return table

def iterate_next_level(json_dictionary, unique_table_name, file_handle_to_sql_script):
    array_found_at_current_level = False
    for (k, v) in json_dictionary.items():
        if type(v) == dict:
            unique_table_name_at_current_level = unique_table_name + SEPARATOR + k
            if (iterate_next_level(v, unique_table_name_at_current_level, file_handle_to_sql_script) == False):
                continue
            json_arrays = dict()
            row = dict()
            for (key, value) in v.items():
                if type(value) == list:
                    json_arrays[key] = value
                elif type(value) == dict:
                    pass
                else:
                    row[key] = str(value)
            for (json_array_key, json_array) in json_arrays.items():
                table = convert_to_table(row, json_array, json_array_key) 
                create_table_and_insert_rows_script(table, unique_table_name_at_current_level, file_handle_to_sql_script)     
        elif type(v) == list:            
            array_found_at_current_level = True
    return array_found_at_current_level

#assumption json starts with a dictionary
def iterate(json_dictionay, unique_table_name, file_handle_to_sql_script):
    row = dict()
    for (k, v) in json_dictionay.items():
        if type(v) != dict and type(v) != list:
            row[k] = str(v)

    suffix = 1
    for(k, v) in json_dictionay.items():
        if type(v) == list:
           table = convert_to_table(row, v, k)
           create_table_and_insert_rows_script(table, unique_table_name + SEPARATOR + str(suffix), file_handle_to_sql_script)
           suffix = suffix + 1
    iterate_next_level(json_dictionay, unique_table_name, file_handle_to_sql_script)


#This transformation is about iterating through JSON, picking an object, picking an array that is a member of the object, and transforming into a denormalized relation.
#The denormalization process repeats the object members at every index of the array to create rows to be inserted into the table.
#This transformation is useful in cases where JSON is drafted in a kind of master/detail relationship.
def jtors(json_string, table_name_prefix, output_sql_script_file_name):
    json_dictionary = json.loads(json_string)
    file_handle_to_sql_script = open(output_sql_script_file_name, 'w+')
    iterate(json_dictionary, table_name_prefix, file_handle_to_sql_script)
    file_handle_to_sql_script.seek(0)
    create_table_insert_rows_sql_script = file_handle_to_sql_script.read()
    file_handle_to_sql_script.close()
    return create_table_insert_rows_sql_script
