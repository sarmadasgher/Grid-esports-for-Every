#Grid esports for Every by sarmadasgher

import unittest
import json
from json_to_relations.library.jtors_script import jtors
class TestJtors(unittest.TestCase):
    
    def test_iterate_1(self):
        sample_json_1 = '{ "menu": { "id": "file", "value": "File", "popup": [ { "value": "New", "onclick": "CreateNewDoc()" }, { "value": "Open", "onclick": "OpenDoc()" }, { "value": "Close", "onclick": "CloseDoc()" } ] } }'
        create_table_insert_rows_sql_script = jtors(sample_json_1, 'window', 'sample-json-output-1.sql')
        expected_sql_script = 'CREATE TABLE `window_menu` (\n'
        expected_sql_script += '`id` LONGTEXT,\n'
        expected_sql_script += '`popup_onclick` LONGTEXT,\n'
        expected_sql_script += '`popup_value` LONGTEXT,\n'
        expected_sql_script += '`value` LONGTEXT);\n'
        expected_sql_script += 'INSERT INTO `window_menu` VALUES \n'
        expected_sql_script += '("file", "CreateNewDoc()", "New", "File"),\n'
        expected_sql_script += '("file", "OpenDoc()", "Open", "File"),\n'
        expected_sql_script += '("file", "CloseDoc()", "Close", "File");\n'
        self.assertEqual(create_table_insert_rows_sql_script, 
                         expected_sql_script)
 
    def test_iterate_2(self):
        sample_json_2 = '{ "glossary": { "title": "example glossary", "GlossDiv": { "title": "S", "GlossList": { "GlossEntry": { "ID": "SGML", "SortAs": "SGML", "GlossTerm": "Standard Generalized Markup Language", "Acronym": "SGML", "Abbrev": "ISO 8879:1986", "GlossDef": { "para": "A meta-markup language, used to create markup languages such as DocBook.", "GlossSeeAlso": ["GML", "XML"] }, "GlossSee": "markup" } } } } }'
        create_table_insert_rows_sql_script = jtors(sample_json_2,'Shop', 'sample-json-output-2.sql')
        expected_sql_script = 'CREATE TABLE `Shop_glossary_GlossDiv_GlossList_GlossEntry_GlossDef` (\n'
        expected_sql_script += '`GlossSeeAlso` LONGTEXT,\n'
        expected_sql_script += '`para` LONGTEXT);\n'
        expected_sql_script += 'INSERT INTO `Shop_glossary_GlossDiv_GlossList_GlossEntry_GlossDef` VALUES \n'
        expected_sql_script += '("GML", "A meta-markup language, used to create markup languages such as DocBook."),\n'
        expected_sql_script += '("XML", "A meta-markup language, used to create markup languages such as DocBook.");\n'
        self.assertEqual(create_table_insert_rows_sql_script, 
                         expected_sql_script)

    def test_iterate_3(self):
        sample_json_3 = '{ "id": "file", "value": "File", "popup": [ { "value": "New", "onclick": "CreateNewDoc()" }, { "value": "Open", "onclick": "OpenDoc()" }, { "value": "Close", "onclick": "CloseDoc()" } ] } '
        create_table_insert_rows_sql_script = jtors(sample_json_3, 'window', 'sample-json-output-3.sql')
        expected_sql_script = 'CREATE TABLE `window_1` (\n'
        expected_sql_script += '`id` LONGTEXT,\n'
        expected_sql_script += '`popup_onclick` LONGTEXT,\n'
        expected_sql_script += '`popup_value` LONGTEXT,\n'
        expected_sql_script += '`value` LONGTEXT);\n'
        expected_sql_script += 'INSERT INTO `window_1` VALUES \n'
        expected_sql_script += '("file", "CreateNewDoc()", "New", "File"),\n'
        expected_sql_script += '("file", "OpenDoc()", "Open", "File"),\n'
        expected_sql_script += '("file", "CloseDoc()", "Close", "File");\n'
        self.assertEqual(create_table_insert_rows_sql_script, 
                         expected_sql_script)        

if __name__ == "__main__":
    unittest.main()