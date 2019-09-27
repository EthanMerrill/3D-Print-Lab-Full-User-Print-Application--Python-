    
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
import json
import getpass
import time
import threading
# native python library
import ctypes
# non-native library

# import globals

# ##Will put chrome driver in the path automatically in the future
# if getattr(sys, 'frozen', False) :
#     # running in a bundle
#     chromedriver_path = os.path.join(sys._MEIPASS, 'chromedriver')


def user_auth_check(driver, customText):
    
    # Opens 3dpos login page, checks for login success, scrapes and returns username
        
    # goto the 3dprinteros page
    driver.get('https://cloud.3dprinteros.com/printing/')
    # insert a the passed label into the page so the user knows that this is the user or admin login
    # get the logo element
    try :
        logoElement = driver.find_element_by_xpath("//*[@id='wrapper']/a/h1")
    except:
        logoElement = driver.find_element_by_xpath("//*[@id='menuitem_user']/a")
    else: print("logo not found")
    # executes javascript which modifies the page to place the passed label on the login page
    driver.execute_script (
        """
        arguments[0].setAttribute('class','label');
        arguments[0].setAttribute('style', 'font: 50px arial');
        arguments[0].innerHTML = arguments[1];""", logoElement, customText
    )
    # a loop which checks to see if the user has logged and and been directed to the prints page
    # if so, scrape the userID from the page
    while True:
        if driver.current_url == 'https://cloud.3dprinteros.com/myfiles/#':
            usernameElement = driver.find_element_by_xpath("//*[@id='menuitem_user']/a")
            username = usernameElement.get_attribute('innerText')
            #driver.quit
            usernameAndDriver = [driver, username]
            return usernameAndDriver

            
# set default value of load photos to false
def initializeListener(loadPhotos = True):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    # disables most logging
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--remote-debugging-port=9222") #http://localhost:9222

    # if specified, do not load images
    if loadPhotos == False:
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.setPageLoadStrategy(PageLoadStrategy.NONE)
    driver = webdriver.Chrome(options=chrome_options)
    driver.minimize_window()
    # these might be useful for inserting into an sql table later
    # tazTable = driver.find_element(By.XPATH, "//*[@id='id_box_51246']/span/table")
    # ultiTable = driver.find_element(By.XPATH, "//*[@id='id_box_51247']/span/table")
    # print("Taz 6 Queue" +tazTable.text +"/n Ultimaker Table /n" +ultiTable.text)
    return driver


def admin_login():
    # this is another thread which runs in parallel
    adminDriver = initializeListener(False)
    
    adminUsername = "GR-FISPROTOTYPINGLAB@WPI.EDU"
    # loop to ensure login can continue after another user accidentally logs in
    while True:
        usernameAndDriver = user_auth_check(adminDriver, "Admin Login")
        if adminUsername == usernameAndDriver[1]:
            usernameAndDriver[0].minimize_window
            return usernameAndDriver[0]
        else:
            print("failed admin Login. Please login with the {} account, not {}", adminUsername, usernameAndDriver[1])
            #driver.refresh()


def user_login():
    userDriver = initializeListener(False)
    #set window positioning
    userDriver.set_window_size(300,1080)
    userDriver.set_window_position(0,0)
    usernameAndDriver = user_auth_check(userDriver, "Student Login")
    #usernameAndDriver[0].quit()
    return usernameAndDriver[1]

def clear_all_tables(driver, fullUserEmail):
    
    driver.get("https://cloud.3dprinteros.com/printing/")
    element = driver.find_element_by_xpath("//*[@id='header']")
    driver.execute_script(
                "arguments[0].remove();", element
            )
    table_filter(driver, '//*[@id="id_box_45971"]/span/table/tbody', fullUserEmail)
    table_filter(driver, '//*[@id="id_box_51246"]/span/table/tbody', fullUserEmail)
    table_filter(driver, '//*[@id="id_box_59968"]/span/table/tbody', fullUserEmail)
    table_filter(driver, '//*[@id="id_box_51247"]/span/table/tbody', fullUserEmail)
    driver.fullscreen_window()
    driver = table_filter(driver, '//*[@id="id_box_59967"]/span/table/tbody', fullUserEmail)
    driver.fullscreen_window()
    return driver 

def table_filter( driver, xpath, fullUserEmail):
    #taz xpath table://*[@id="id_box_51246"]/span/table/tbody
    #taz paid jobs table: //*[@id="id_box_59968"]/span/table/tbody
    # ultimaker xpath table: //*[@id="id_box_51247"]/span/table/tbody
    #ultimaker paid jobs table: //*[@id="id_box_59967"]/span/table/tbody
    queueTable = driver.find_elements_by_xpath(xpath)
    try:
        allTableElements = queueTable[0].find_elements_by_xpath(".//tr[contains(@id,'job_box')]")
    except:
        print("table Not Found")
        return driver
    # print (tazTable[0].text)
    for element in allTableElements:
        #add an if not in statement here to filter 
        if fullUserEmail not in element.text: 
            ##### print(f"element: {element.text} not removed from page")
            # print (f"{element.text} removed from page")
            driver.execute_script(
                "arguments[0].remove();", element
            )
    return driver
    
def persistent_alert():
    while True:
        return pymsgbox.alert(text='',title='', button='Quit')
        
def main_function(adminDriver):
     while True:
        userName = user_login()
        clear_all_tables(adminDriver, userName)
        # if  persistent_alert() =='Quit':
        #     adminDriver.minimize_window
        #     adminDriver.refresh()

if __name__ == "__main__":
    #create the driver class
    #driverHandler = driver_handler()
    #start two parallel threads on initial start: admin login, Userlogin. 
    # t1 = threading.Thread(target=admin_login())
    # t2 = threading.Thread(target=user_login())
    
    # #start thread1
    # t1.start()
    # #start thread2
    # t2.start()
    # #at this point the admin has logged in. 
    # #minimize the admin driver to reveal the user login driver
    
    # t1.join
    # t2.join

    adminDriver = admin_login()

    while True:
        try:
            main_function(adminDriver)
        except:
            adminDriver = admin_login()
            #main_function(admin_login)

    

    #get user Credentials:
    #set in dict

    # while True:
    #     userCredentials = {
    #     "username" : input("Username (WPI Email): "),
    #     "password" : getpass.getpass()
    #     }   
    #     if user_auth_check(userCredentials) == True :
    #         print("user Credentials Correct")
    #         break
    #     else:
    #         print("user Credentials incorrect, try again")


    # #instantiate the driver handler class (creates self)
    # driverHandler = driver_handler()

    # #opens the instance of chrome on startup. Initializes the global variable so every function talks to the same chrome client
    # driver = driverHandler.initializeListener()
    # #instantiate the main class
    # main = main() 
    # #read the admin keys file (will be replaced with a login prompt in the future)
    # with open("app\keys.json", "r") as read_file:
    #     adminKeys = json.load(read_file)
    # main.admin_login(driver, adminKeys)
    # #taz xpath table://*[@id="id_box_51246"]/span/table/tbody
    # #taz paid jobs table: //*[@id="id_box_59968"]/span/table/tbody
    # #ultimaker xpath table: //*[@id="id_box_51247"]/span/table/tbody
    # #ultimaker paid jobs table: //*[@id="id_box_59967"]/span/table/tbody


    # # new
    # # taz table //*[@id="id_box_51246"]/span/table/tbody
    
    # #clean Admin view
    # driver.execute_script(
    # "arguments[0].remove();", driver.find_element_by_xpath('//*[@id="header"]/div')
    # )

    # #clear tables

    # main.table_filter(driver, '//*[@id="id_box_51246"]/span/table/tbody',userCredentials["username"])
    # main.table_filter(driver, '//*[@id="id_box_59968"]/span/table/tbody',userCredentials["username"])
    # main.table_filter(driver, '//*[@id="id_box_51247"]/span/table/tbody',userCredentials["username"])
    # main.table_filter(driver, '//*[@id="id_box_59967"]/span/table/tbody',userCredentials["username"])
    # driver.fullscreen_window()
    # time.sleep(300)
    
    
    #driver.maximize_window()
