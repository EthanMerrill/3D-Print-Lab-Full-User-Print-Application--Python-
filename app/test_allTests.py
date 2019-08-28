import unittest
import json
import full_user_filter

class Test_TestMain(unittest.TestCase):
    def test_main(self):
        with open("app\keys.json", "r") as read_file:
            adminKeys = json.load(read_file)
        #main = main() 
        driver = full_user_filter.driver_handler.initializeListener(self)
        full_user_filter.main.admin_login(self, driver, adminKeys)

    def test_user_auth_deny(self):  
        badUserKeysDict = {
        'username': 'test',
        'password' : 'test'
        }
        assert full_user_filter.user_auth_check(badUserKeysDict) == False
    
    def test_user_auth_granted(self):
        with open("app\keys.json", "r") as read_file:
            goodUserKeysDict = json.load(read_file)
    
        assert full_user_filter.user_auth_check(goodUserKeysDict) == True
if __name__ == '__main__':
    unittest.main()