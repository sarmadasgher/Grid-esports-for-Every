#Grid esports for Every by sarmadasgher

import unittest
import json
from json_to_relations.library.jtor_script import jtor

class TestJtor(unittest.TestCase):
    
    def test_jtor(self):
        sample_json = '{ "menu": { "id": "file", "value": "File", "popup": { "menuitem": [ { "value": "New", "onclick": "CreateNewDoc()" }, { "value": "Open", "onclick": "OpenDoc()" }, { "value": "Close", "onclick": "CloseDoc()" } ] } } }'
        json_dictionary = json.loads(sample_json)
        result_dictionary = jtor(json_dictionary, 'app')
        #result_dictionary contains more forms, have to argue the reason behind
        self.assertEqual(len(result_dictionary), 14)
        self.assertEqual(result_dictionary.get('app_menu_id'), "file")
        self.assertEqual(result_dictionary.get('app_menu_value'), "File")
        self.assertEqual(result_dictionary.get('app_menu_popup_menuitem_0_value_0'), "New")
        self.assertEqual(result_dictionary.get('app_menu_popup_menuitem_0_onclick_0'), "CreateNewDoc()")        
        self.assertEqual(result_dictionary.get('app_menu_popup_menuitem_1_value_1'), "Open")
        self.assertEqual(result_dictionary.get('app_menu_popup_menuitem_1_onclick_1'), "OpenDoc()")        
        self.assertEqual(result_dictionary.get('app_menu_popup_menuitem_2_value_2'), "Close")
        self.assertEqual(result_dictionary.get('app_menu_popup_menuitem_2_onclick_2'), "CloseDoc()")        


if __name__ == "__main__":
    unittest.main()