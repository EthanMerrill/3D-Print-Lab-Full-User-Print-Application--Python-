    
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
import json
import getpass
import time
import threading
import sys


def user_auth_check(driver, customText, credentialsArray = []):
    
    #Opens 3dpos login page, checks for login success, scrapes and returns username 
    
    #goto the 3dprinteros page
    driver.get('https://cloud.3dprinteros.com/printing/')
    #insert a the passed label into the page so the user knows that this is the user or admin login
    #get the logo element
    try :
        logoElement = driver.find_element_by_xpath("//*[@id='wrapper']/a/h1")
    except: 
        logoElement = driver.find_element_by_xpath("//*[@id='menuitem_user']/a") 
    else: print("logo not found")
    #executes javascript which modifies the page to place the passed label on the login page
    driver.execute_script (
        """
        arguments[0].setAttribute('class','label');
        arguments[0].setAttribute('style', 'font: 50px arial');
        arguments[0].innerHTML = arguments[1];""", logoElement, customText
    )
    #automate field filling for testing purposes
    try:
        driver.find_element_by_id('signinUsername').send_keys(credentialsArray["username"])
    except:
        print("username not passed")
        pass
    try:
        driver.find_element_by_id('signinPassword').send_keys(credentialsArray["password"])
    except:
        print("password not passed")
        pass
    #call the helper function
    return check_for_username(driver)


def check_for_username(driver):
    #a loop which checks to see if the user has logged and and been directed to the prints page
    #if so, scrape the userID from the page
    while True:
        if driver.current_url == 'https://cloud.3dprinteros.com/myfiles/#':
            usernameElement = driver.find_element_by_xpath("//*[@id='menuitem_user']/a")
            username = usernameElement.get_attribute('innerText')
            usernameAndDriver = [driver, username]
            return usernameAndDriver


def await_logout(driver):
    #function which monitors the user window until the url has changed to the login window, then continues. 
    while True:
        if driver.current_url == 'https://cloud.3dprinteros.com/':
            return driver


def initialize_user_window():
    try: 
        userDriver = initialize_driver()
        #size and position the window appropriately
        userDriver.set_window_size(300,1030)
        userDriver.set_window_position(0,0)
        return userDriver
    except Exception as e:
            print(f"Exception:{e} occured, unable to initialize user window")
            pass

def initialize_admin_window():
    try:
        adminDriver = initialize_driver()
        #size and position the window appropriately
        adminDriver.set_window_size(1420,1030)
        adminDriver.set_window_position(501,0)
        return adminDriver
    except Exception as e:
        print(f"Exception:{e} occured, unable to initialize admin window")
        #input("press enter to exit")
        pass

def initialize_driver():
    try:
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        #may fix odd crashing bug
        chrome_options.add_argument("--no-sandbox")
        #disables most logging
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--allow-running-insecure-content")
        #chrome_options.add_argument("--remote-debugging-port=9222") #http://localhost:9222
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        #chrome_options.setPageLoadStrategy(PageLoadStrategy.NONE)
        driver = webdriver.Chrome(executable_path="chromedriver.exe",options=chrome_options)
        return driver

    except Exception as e:
        print(f"Exception:{e} occured, unable to initialize chrome")
        #input("press enter to exit")
        pass

def user_window_to_logout(driver):
    #function modifies the user page to add a large logout button
    driver.execute_script( 
        """
var newDiv = document.createElement('div');
//set the id and content
newDiv.id = "button";
newDiv.onclick = () => { window.location = "https://cloud.3dprinteros.com/logout/" }
newDiv.innerHTML = '<button class="btn">Log Out</button>';
//newDiv.setAttribute = 
//newDiv.appendChild(newContent)

//var sp2 = document.getElementById("main-block");
//let a = document.getElementsByTagName("script")[0]
//console.log(a);
document.body.innerHTML = "";
document.body.appendChild(newDiv);
        """
    )
    return driver

def clear_all_tables(driver, fullUserEmail):
    #wipes any previous changes to the page.
    driver.get("https://cloud.3dprinteros.com/printing/")
    #make a list of elements to remove from the page (headers)
    oneTimeRemoveElements = [
        "//*[@id='host_id_18233']", 
        "//*[@id='id_box_49258']", 
        '//*[@id="id_box_45971"]',
        "//*[@id='host_id_22576']", 
        "//*[@id='header']", 
        "//*[@id='cookieMess']", 
        "//*[@id='noChromeMess']"] 
    #iterate through the list and remove each element sequentially
    #wait for the page to load for a sec
    time.sleep(1.5)
    for xpath in oneTimeRemoveElements:
        try:
            element = driver.find_element_by_xpath(xpath)
            driver.execute_script(
                        "arguments[0].remove();", element
                    )
        #handles element not found and every other type of error
        except Exception as e:
            print(f"unable to remove {xpath} because {e}")
            #input("press enter to exit")
            pass


    # uses helper function to clear each queue table     
    # table_filter(driver, '//*[@id="id_box_45971"]/span/table/tbody', fullUserEmail)
    # table_filter(driver, '//*[@id="id_box_51246"]/span/table/tbody', fullUserEmail)
    # table_filter(driver, '//*[@id="id_box_59968"]/span/table/tbody', fullUserEmail)
    # table_filter(driver, '//*[@id="id_box_51247"]/span/table/tbody', fullUserEmail) 

    # driver = table_filter(driver, '//*[@id="id_box_59967"]/span/table/tbody', fullUserEmail)

    #EXPIREMENTAL:
    driver = page_filter(driver, fullUserEmail)

    return driver 

# A new way to clear all tables. Searches every div that looks like a table and clears everything except the username which is passed
def page_filter(driver, fullUserEmail): 
    try:
        # tableContainer = driver.find_elements_by_xpath('//*[@id="printingActiveContainer"]')
        allQueueTables = driver.find_elements_by_xpath(".//div[contains(@id,'host_id')]")
        for element in allQueueTables:
            table_filter(driver, fullUserEmail,"", element)
        return driver     
    except Exception as e:
        print(f"error in function page_filter: {e}")
        return driver        

def table_filter(driver, fullUserEmail, xpath = "", element = ""):
    #taz xpath table://*[@id="id_box_51246"]/span/table/tbody
    #taz paid jobs table: //*[@id="id_box_59968"]/span/table/tbody
    #ultimaker xpath table: //*[@id="id_box_51247"]/span/table/tbody
    #ultimaker paid jobs table: //*[@id="id_box_59967"]/span/table/tbody
    if element == "":
        queueTable = driver.find_elements_by_xpath(xpath)
    elif xpath == "":
        queueTable = element

    try:
        allTableElements = queueTable.find_elements_by_xpath(".//tr[contains(@id,'job_box')]")
    except:
        print(f"table '{xpath}' Not Found")
        return driver
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

def wipe_page(driver):
    try:
        driver.execute_script(
            '''
            document.getElementById("main-block").remove();
            '''
        )
    except Exception as e:
        print(f"unable to wipe page for driver: {driver} error:{e} ")

#optional key arguments for testing
def main(adminkeys = {"username":"gr-fisprototypinglab@wpi.edu"}, studentKeys = []):
    print("welcome to the Full User Print Application V2.2")
    adminDriver = initialize_admin_window()
    userDriver = initialize_user_window()
    #navigate to the prints page in the admin window
    adminDriver.get("https://cloud.3dprinteros.com/printing/")
    #wait for user authentication
    adminUsernameandDriver = user_auth_check(adminDriver, "Admin Login",adminkeys)    
    #breakout a get username Function Here
    #input("press enter to exit")
    while True:
        try:
            usernameandDriver = user_auth_check(userDriver, "Student Login", studentKeys)
            clear_all_tables(adminUsernameandDriver[0], usernameandDriver[1])
            #setup a function that alters the student screen to emphasize the logout function
            usernameandDriver = check_for_username(usernameandDriver[0])
            user_window_to_logout(usernameandDriver[0])
            #Wait for the user to logout
            usernameandDriver[0] = await_logout(usernameandDriver[0])
            wipe_page(adminUsernameandDriver[0])
        except: 
            print("chrome window closed. Please restart the program")
            #input("press enter to exit")
            sys.exit(0)
    #input("press enter to exit")

if __name__ == "__main__":
    main()
