    
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
import json
import getpass
import time
#import globals

# ##Will put chrome driver in the path automatically in the future
# if getattr(sys, 'frozen', False) :
#     # running in a bundle
#     chromedriver_path = os.path.join(sys._MEIPASS, 'chromedriver')

def user_auth_check(userKeys):
        #opens a driver in headless mode, attempts to login to 3dpos with passed credentials, reports a boolean of success or failure to login
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--remote-debugging-port=9222") #http://localhost:9222
        driver = webdriver.Chrome(chrome_options=chrome_options)
        #login procedure. 
        driver.get('https://cloud.3dprinteros.com/printing/')
        driver.find_element_by_id('signinUsername').send_keys(userKeys.get('username'))
        driver.find_element_by_id('signinPassword').send_keys(userKeys.get('password'))
        driver.find_element_by_name('signIn').click()
        if driver.current_url != 'https://cloud.3dprinteros.com/myfiles/#':
            driver.quit()
            return False
        else :
            driver.quit()
            return True
            
class driver_handler() :
    
    def initializeListener(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        #chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--remote-debugging-port=9222") #http://localhost:9222
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.minimize_window()
        #these might be useful for inserting into an sql table later
        #tazTable = driver.find_element(By.XPATH, "//*[@id='id_box_51246']/span/table")
        #ultiTable = driver.find_element(By.XPATH, "//*[@id='id_box_51247']/span/table")
        #print("Taz 6 Queue" +tazTable.text +"/n Ultimaker Table /n" +ultiTable.text)
        return driver

class main():
    

    def admin_login(self, driver, adminKeys):
        #admin keys is a array of keys with username and password. 
        #create the json file object which contains the keys
            #creates an array using data from the json file

        
     #login procedure. 
        driver.get('https://cloud.3dprinteros.com/printing/')
        driver.find_element_by_id('signinUsername').send_keys(adminKeys.get('username'))
        driver.find_element_by_id('signinPassword').send_keys(adminKeys.get('password'))
        driver.find_element_by_name('signIn').click()
        driver.get('https://cloud.3dprinteros.com/printing/')   

    def table_filter(self, driver, xpath, fullUserEmail):
        #taz xpath table://*[@id="id_box_51246"]/span/table/tbody
        #taz paid jobs table: //*[@id="id_box_59968"]/span/table/tbody
        # ultimaker xpath table: //*[@id="id_box_51247"]/span/table/tbody
        #ultimaker paid jobs table: //*[@id="id_box_59967"]/span/table/tbody
        queueTable = driver.find_elements_by_xpath(xpath)
        allTableElements = queueTable[0].find_elements_by_xpath(".//tr[contains(@id,'job_box')]")
        #print (tazTable[0].text)
        for element in allTableElements:
            #add an if not in statement here to filter 
            if fullUserEmail not in element.text: 
                #####print(f"element: {element.text} not removed from page")
                #print (f"{element.text} removed from page")
                driver.execute_script(
                    "arguments[0].remove();", element
                )
        return driver
        

if __name__ == "__main__":
    #get user Credentials:
    #set in dict

    while True:
        userCredentials = {
        "username" : input("Username (WPI Email): "),
        "password" : getpass.getpass()
        }   
        if user_auth_check(userCredentials) == True :
            print("user Credentials Correct")
            break
        else:
            print("user Credentials incorrect, try again")


    #instantiate the driver handler class (creates self)
    driverHandler = driver_handler()

    #opens the instance of chrome on startup. Initializes the global variable so every function talks to the same chrome client
    driver = driverHandler.initializeListener()
    #instantiate the main class
    main = main() 
    #read the admin keys file (will be replaced with a login prompt in the future)
    with open("app\keys.json", "r") as read_file:
        adminKeys = json.load(read_file)
    main.admin_login(driver, adminKeys)
    #taz xpath table://*[@id="id_box_51246"]/span/table/tbody
    #taz paid jobs table: //*[@id="id_box_59968"]/span/table/tbody
    #ultimaker xpath table: //*[@id="id_box_51247"]/span/table/tbody
    #ultimaker paid jobs table: //*[@id="id_box_59967"]/span/table/tbody


    # new
    # taz table //*[@id="id_box_51246"]/span/table/tbody
    
    #clean Admin view
    driver.execute_script(
    "arguments[0].remove();", driver.find_element_by_xpath('//*[@id="header"]/div')
    )

    #clear tables

    main.table_filter(driver, '//*[@id="id_box_51246"]/span/table/tbody',userCredentials["username"])
    main.table_filter(driver, '//*[@id="id_box_59968"]/span/table/tbody',userCredentials["username"])
    main.table_filter(driver, '//*[@id="id_box_51247"]/span/table/tbody',userCredentials["username"])
    main.table_filter(driver, '//*[@id="id_box_59967"]/span/table/tbody',userCredentials["username"])
    driver.fullscreen_window()
    time.sleep(300)
    
    
    #driver.maximize_window()
