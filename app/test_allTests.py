import unittest
import json
import full_user_filter
import time
import two_chrome_window

class Test_TestMain(unittest.TestCase):
    def test_all_two_chrome_window(self):
        with open("app\keys.json", "r") as read_file:
            keys = json.load(read_file)
        adminKeys = keys["adminKeys"]
        userKeys = keys["studentKeys"]
        two_chrome_window.main(adminKeys, userKeys)

        assert True == True

    def test_page_removal(self):
        with open("app\keys.json", "r") as read_file:
            keys = json.load(read_file)
        adminKeys = keys["adminKeys"]
        driver = two_chrome_window.initialize_admin_window()
        two_chrome_window.user_auth_check(driver, "PAGE EDIT TEST", adminKeys)
        two_chrome_window.clear_all_tables(driver, "mjadiletta@wpi.edu")
        time.sleep(10)

if __name__ == '__main__':
    unittest.main()